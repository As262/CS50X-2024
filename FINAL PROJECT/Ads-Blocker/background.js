chrome.runtime.onInstalled.addListener(() => {
  console.log("Service Worker: Installed");

  // Set default blocking status if not already set
  chrome.storage.local.get(['blocking'], function(result) {
    if (result.blocking === undefined) {
      chrome.storage.local.set({ blocking: true });
    }
  });
});

// Listen for messages from the popup or other parts of the extension
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.blocking !== undefined) {
    // Update the ad blocking rules based on the new status
    updateBlockingRules(message.blocking);
    sendResponse({ status: 'success' });
  }
});

// Function to update ad blocking rules
function updateBlockingRules(isBlocking) {
  if (isBlocking) {
    // Enable blocking rules
    chrome.declarativeNetRequest.updateDynamicRules({
      addRules: [
        {
          id: 1,
          priority: 1,
          action: { type: "block" },
          condition: {
            urlFilter: "*://*.doubleclick.net/*",
            resourceTypes: ["main_frame", "sub_frame", "script", "xmlhttprequest"]
          }
        },
        {
          id: 2,
          priority: 1,
          action: { type: "block" },
          condition: {
            urlFilter: "*://*.googlesyndication.com/*",
            resourceTypes: ["main_frame", "sub_frame", "script", "xmlhttprequest"]
          }
        }
      ],
      removeRuleIds: [1, 2]
    }, () => {
      if (chrome.runtime.lastError) {
        console.error('Error updating blocking rules:', chrome.runtime.lastError);
      } else {
        console.log('Blocking rules updated.');
      }
    });
  } else {
    // Disable blocking rules by removing them
    chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: [1, 2]
    }, () => {
      if (chrome.runtime.lastError) {
        console.error('Error removing blocking rules:', chrome.runtime.lastError);
      } else {
        console.log('Blocking rules removed.');
      }
    });
  }
}
