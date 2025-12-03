document.addEventListener("DOMContentLoaded", () => {
  const grabButton = document.getElementById("grabButton");
  const previewButton = document.getElementById("previewButton");
  const statusDiv = document.getElementById("status");
  const previewArea = document.getElementById("preview");

  grabButton.addEventListener("click", async () => {
    try {
      const response = await browser.runtime.sendMessage({ action: "grabTabs" });

      if (response.success) {
        // Copy to clipboard
        await navigator.clipboard.writeText(response.markdown);

        // Show success message
        showStatus("Tabs copied to clipboard!", "success");

        // Close popup after a brief delay
        setTimeout(() => window.close(), 800);
      } else {
        showStatus(`Error: ${response.error}`, "error");
      }
    } catch (error) {
      showStatus(`Error: ${error.message}`, "error");
    }
  });

  previewButton.addEventListener("click", async () => {
    try {
      const response = await browser.runtime.sendMessage({ action: "grabTabs" });

      if (response.success) {
        previewArea.value = response.markdown;
        previewArea.style.display = "block";
        showStatus("Preview loaded. You can edit before copying manually.", "success");
      } else {
        showStatus(`Error: ${response.error}`, "error");
      }
    } catch (error) {
      showStatus(`Error: ${error.message}`, "error");
    }
  });

  function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = type;
  }
});
