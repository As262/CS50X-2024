document.addEventListener('DOMContentLoaded', function() {
  let toggleButton = document.getElementById('toggle');

  // Retrieve the current status from storage
  chrome.storage.local.get(['blocking'], function(result) {
    if (result.blocking !== undefined) {
      toggleButton.textContent = result.blocking ? "Disable Ad Blocker" : "Enable Ad Blocker";
    } else {
      // Set default value if not set
      chrome.storage.local.set({ blocking: true });
      toggleButton.textContent = "Disable Ad Blocker";
    }
  });

  // Add click event listener to the button
  toggleButton.addEventListener('click', function() {
    chrome.storage.local.get(['blocking'], function(result) {
      let newStatus = !result.blocking;
      chrome.storage.local.set({ blocking: newStatus }, function() {
        toggleButton.textContent = newStatus ? "Disable Ad Blocker" : "Enable Ad Blocker";
        // Notify the background script of the change
        chrome.runtime.sendMessage({ blocking: newStatus });
      });
    });
  });
});
