// Listen for messages from the popup
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "grabTabs") {
    grabTabs().then(sendResponse);
    return true; // Indicates we will send a response asynchronously
  }
});

async function grabTabs() {
  try {
    // Get all windows with their tabs
    const windows = await browser.windows.getAll({ populate: true });

    let markdown = "";

    for (const window of windows) {
      const tabs = window.tabs;
      // Note: window.state minimized detection is unreliable on Linux
      const isMinimized = window.state === "minimized";

      for (let i = 0; i < tabs.length; i++) {
        const tab = tabs[i];
        const isFirstTab = i === 0;
        const isCurrent = tab.active;

        // Build the markdown line
        let line = "";

        // Indent if not first tab
        if (!isFirstTab) {
          line += "    ";
        }

        line += "- ";

        // Add minimized mark only for first tab
        if (isFirstTab && isMinimized) {
          line += "▽ ";
        }

        // Add the link
        const title = tab.title || tab.url;
        line += `[${title}](${tab.url})`;

        // Add current mark
        if (isCurrent) {
          line += " ☆";
        }

        markdown += line + "\n";
      }

      // Add blank line between windows
      markdown += "\n";
    }

    return { success: true, markdown: markdown };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
