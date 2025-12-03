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

### Permanent Installation (Unsigned)

Firefox requires extensions to be signed by Mozilla for permanent installation. For personal use:

1. Open Firefox and navigate to `about:config`
2. Search for `xpinstall.signatures.required`
3. Set it to `false` (Note: This disables signature verification for all extensions)
4. Package the extension: `cd tabgrab-firefox && zip -r ../tabgrab-firefox.xpi *`
5. Open `about:addons` and click the gear icon
6. Select "Install Add-on From File..." and choose the `.xpi` file

Alternatively, use Firefox Developer Edition or Nightly which allow unsigned extensions more easily.

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
