#!/usr/bin/env python3
"""
Dennis File - A file indexing and duplicate finding utility
"""

import argparse
import hashlib
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


class DennisFile:
    def __init__(self, db_path="dennisfile.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database with required schema"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                size INTEGER NOT NULL,
                hash TEXT NOT NULL,
                mtime REAL NOT NULL,
                scan_time TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hash ON files(hash)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_size ON files(size)
        """)

        self.conn.commit()

    def calculate_hash(self, file_path, chunk_size=8192):
        """Calculate SHA-256 hash of a file"""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (PermissionError, OSError) as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            return None

    def scan_directory(self, root_path, update=False):
        """Scan directory tree and index all files"""
        root_path = Path(root_path).resolve()

        if not root_path.exists():
            print(f"Error: Path does not exist: {root_path}", file=sys.stderr)
            return

        cursor = self.conn.cursor()
        scan_time = datetime.now().isoformat()
        files_processed = 0
        files_updated = 0
        files_added = 0

        print(f"Scanning: {root_path}")

        for entry in root_path.rglob('*'):
            if entry.is_file():
                try:
                    file_path = str(entry)
                    file_size = entry.stat().st_size
                    file_mtime = entry.stat().st_mtime

                    # Check if file already exists in database
                    cursor.execute("SELECT mtime, hash FROM files WHERE path = ?", (file_path,))
                    existing = cursor.fetchone()

                    # Skip if file hasn't changed
                    if existing and not update:
                        if existing[0] == file_mtime:
                            files_processed += 1
                            if files_processed % 100 == 0:
                                print(f"Processed {files_processed} files...", end='\r')
                            continue

                    # Calculate hash
                    file_hash = self.calculate_hash(file_path)
                    if file_hash is None:
                        continue

                    # Insert or update
                    if existing:
                        cursor.execute("""
                            UPDATE files
                            SET size = ?, hash = ?, mtime = ?, scan_time = ?
                            WHERE path = ?
                        """, (file_size, file_hash, file_mtime, scan_time, file_path))
                        files_updated += 1
                    else:
                        cursor.execute("""
                            INSERT INTO files (path, size, hash, mtime, scan_time)
                            VALUES (?, ?, ?, ?, ?)
                        """, (file_path, file_size, file_hash, file_mtime, scan_time))
                        files_added += 1

                    files_processed += 1

                    if files_processed % 100 == 0:
                        print(f"Processed {files_processed} files...", end='\r')
                        self.conn.commit()

                except (PermissionError, OSError) as e:
                    print(f"\nWarning: Could not process {entry}: {e}", file=sys.stderr)
                    continue

        self.conn.commit()
        print(f"\nScan complete: {files_processed} files processed")
        print(f"  Added: {files_added}, Updated: {files_updated}")

    def find_duplicates(self, min_size=0):
        """Find duplicate files based on hash"""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT hash, COUNT(*) as count, SUM(size) as total_size
            FROM files
            WHERE size >= ?
            GROUP BY hash
            HAVING count > 1
            ORDER BY total_size DESC
        """, (min_size,))

        duplicates = cursor.fetchall()

        if not duplicates:
            print("No duplicates found.")
            return

        total_wasted = 0
        print(f"\nFound {len(duplicates)} sets of duplicate files:\n")

        for file_hash, count, total_size in duplicates:
            wasted_space = total_size - (total_size // count)
            total_wasted += wasted_space

            print(f"Hash: {file_hash[:16]}... ({count} copies, {self.format_size(total_size)} total, {self.format_size(wasted_space)} wasted)")

            cursor.execute("SELECT path, size FROM files WHERE hash = ?", (file_hash,))
            for path, size in cursor.fetchall():
                print(f"  - {path} ({self.format_size(size)})")
            print()

        print(f"Total wasted space: {self.format_size(total_wasted)}")

    def show_usage(self, path_prefix=None):
        """Show space usage statistics"""
        cursor = self.conn.cursor()

        if path_prefix:
            cursor.execute("""
                SELECT COUNT(*), SUM(size)
                FROM files
                WHERE path LIKE ?
            """, (f"{path_prefix}%",))
        else:
            cursor.execute("SELECT COUNT(*), SUM(size) FROM files")

        count, total_size = cursor.fetchone()

        if count == 0:
            print("No files found.")
            return

        print(f"\nTotal files: {count:,}")
        print(f"Total size: {self.format_size(total_size or 0)}")

        # Show largest files
        print("\nLargest files:")
        cursor.execute("""
            SELECT path, size
            FROM files
            ORDER BY size DESC
            LIMIT 10
        """)

        for i, (path, size) in enumerate(cursor.fetchall(), 1):
            print(f"  {i}. {self.format_size(size):>10} - {path}")

    def show_stats(self):
        """Show database statistics"""
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*), SUM(size) FROM files")
        count, total_size = cursor.fetchone()

        cursor.execute("SELECT COUNT(DISTINCT hash) FROM files")
        unique_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT hash FROM files GROUP BY hash HAVING COUNT(*) > 1
            )
        """)
        duplicate_sets = cursor.fetchone()[0]

        print(f"\nDatabase: {self.db_path}")
        print(f"Total files indexed: {count:,}")
        print(f"Unique files: {unique_count:,}")
        print(f"Duplicate sets: {duplicate_sets:,}")
        print(f"Total size: {self.format_size(total_size or 0)}")

    @staticmethod
    def format_size(size):
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Dennis File - Index files and find duplicates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scan /path/to/directory
  %(prog)s duplicates
  %(prog)s usage
  %(prog)s stats
        """
    )

    parser.add_argument(
        '--db',
        default='dennisfile.db',
        help='Database file path (default: dennisfile.db)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan a directory tree')
    scan_parser.add_argument('path', help='Directory path to scan')
    scan_parser.add_argument(
        '--update',
        action='store_true',
        help='Force update of all files even if unchanged'
    )

    # Duplicates command
    dup_parser = subparsers.add_parser('duplicates', help='Find duplicate files')
    dup_parser.add_argument(
        '--min-size',
        type=int,
        default=0,
        help='Minimum file size in bytes (default: 0)'
    )

    # Usage command
    usage_parser = subparsers.add_parser('usage', help='Show space usage')
    usage_parser.add_argument(
        '--path',
        help='Filter by path prefix'
    )

    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    df = DennisFile(args.db)

    try:
        if args.command == 'scan':
            df.scan_directory(args.path, update=args.update)
        elif args.command == 'duplicates':
            df.find_duplicates(min_size=args.min_size)
        elif args.command == 'usage':
            df.show_usage(path_prefix=args.path)
        elif args.command == 'stats':
            df.show_stats()
    finally:
        df.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
