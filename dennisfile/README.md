Dennis File
===========

A Python tool that crawls directory trees and builds a SQLite database of file paths, sizes, and content hashes. Use it to query space usage and find duplicate files.

## Features

- Recursively scan directories and index all files
- Calculate SHA-256 hashes of file contents
- Store metadata in SQLite database with indexing
- Find duplicate files across your filesystem
- Analyze space usage and identify largest files
- Incremental scanning (skip unchanged files)

## Usage

### Scan a directory

```bash
./dennisfile.py scan /path/to/directory
```

### Find duplicates

```bash
./dennisfile.py duplicates
# Or filter by minimum file size
./dennisfile.py duplicates --min-size 1048576  # Only files >= 1MB
```

### Show space usage

```bash
./dennisfile.py usage
# Or filter by path
./dennisfile.py usage --path /home/user/documents
```

### Show database statistics

```bash
./dennisfile.py stats
```

### Use a custom database file

```bash
./dennisfile.py --db myindex.db scan /path/to/directory
./dennisfile.py --db myindex.db duplicates
```

## Requirements

- Python 3.6+
- SQLite3 (included with Python)

## How it works

1. **Scanning**: Walks the directory tree and reads each file
2. **Hashing**: Calculates SHA-256 hash of file contents (in chunks for memory efficiency)
3. **Indexing**: Stores path, size, hash, and modification time in SQLite
4. **Optimization**: Skips files that haven't changed since last scan (based on mtime)
5. **Querying**: Uses SQL indexes for fast duplicate detection and analysis
