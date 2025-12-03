# TabGrab for Firefox

A Firefox extension that collects tabs from all windows and formats them as a markdown list of links.

This is the Firefox/Linux equivalent of the macOS `tabgrab` script.

## Features

- Collects all tabs from all Firefox windows
- Formats as markdown links
- Groups tabs by window (first tab is parent, rest are indented)
- Marks current tab with ☆
- Marks minimized windows with ▽
- One-click copy to clipboard
- Optional preview mode

## Installation

### Development/Testing (Temporary)

1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on..."
3. Navigate to this directory and select `manifest.json`
4. The extension will be loaded until you restart Firefox

### Permanent Installation (Signed)

Firefox requires extensions to be signed by Mozilla. For personal use, use self-distribution:

1. **Create Mozilla account**: Sign up at https://addons.mozilla.org/developers/

2. **Package the extension**:
   ```bash
   cd tabgrab-firefox
   zip -r -FS ../tabgrab-firefox.zip * --exclude '*.git*'
   ```

3. **Submit for signing**:
   - Go to https://addons.mozilla.org/developers/addon/submit/distribution
   - Choose "On your own" (self-distribution - not listed publicly on AMO)
   - Upload `tabgrab-firefox.zip`
   - Fill out basic metadata (name, description, category)
   - Simple extensions are usually auto-approved within minutes

4. **Download and install**:
   - Once approved, download the signed `.xpi` file
   - In Firefox, go to `about:addons`
   - Click the gear icon → "Install Add-on From File..."
   - Select the signed `.xpi` file

#### Alternative: Using web-ext CLI

1. **Generate API credentials**:
   - Go to https://addons.mozilla.org/developers/addon/api/key/
   - Generate an API key (JWT issuer and secret)

```bash
npm install -g web-ext
cd tabgrab-firefox
web-ext sign --api-key=YOUR_JWT_ISSUER --api-secret=YOUR_JWT_SECRET
```

The signed `.xpi` will be automatically downloaded to `web-ext-artifacts/` directory.

## Usage

### Method 1: Keyboard Shortcut
Press `Ctrl+Alt+G` to grab tabs and copy to clipboard

### Method 2: Toolbar Button
1. Click the TabGrab icon in the toolbar
2. Click "Grab Tabs & Copy to Clipboard"
3. The tab list is now in your clipboard

### Method 3: Preview Mode
1. Click the TabGrab icon
2. Click "Preview Tabs"
3. Review/edit the markdown in the text area
4. Copy manually if desired

## Output Format

```markdown
- [First Tab Title](https://url1.com) ☆
    - [Second Tab Title](https://url2.com)
    - [Third Tab Title](https://url3.com)

- ▽ [Minimized Window First Tab](https://url4.com)
    - [Another Tab](https://url5.com)
```

## Comparison to Original macOS Script

| Feature | macOS `tabgrab` | Firefox Extension |
|---------|----------------|-------------------|
| Platform | macOS only | Linux, macOS, Windows |
| Browser Support | Safari, Chrome | Firefox only |
| Installation | Copy script | Install extension |
| Invocation | CLI command | Keyboard shortcut or toolbar |
| Output | stdout or clipboard | Clipboard or preview |

## License

MIT License (same as original `tabgrab` script)
