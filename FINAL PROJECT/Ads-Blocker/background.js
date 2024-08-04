chrome.runtime.onInstalled.addListener(() => {
  console.log("Service Worker: Installed");

  // Set default blocking status if not already set
  chrome.storage.local.get(['blocking'], function(result) {
    if (result.blocking === undefined) {
      chrome.storage.local.set({ blocking: true }, () => {
        updateBlockingRules(true); // Enable blocking by default
      });
    } else {
      updateBlockingRules(result.blocking); // Apply the stored status
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
      removeRuleIds: [] // Clear any existing rules to prevent duplicates
    }, () => {
      if (chrome.runtime.lastError) {
        console.error('Error enabling blocking rules:', chrome.runtime.lastError);
      } else {
        console.log('Blocking rules enabled.');
      }
    });
  } else {
    // Disable blocking rules by removing all dynamic rules
    chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: [], // An empty array clears all rules
    }, () => {
      if (chrome.runtime.lastError) {
        console.error('Error disabling blocking rules:', chrome.runtime.lastError);
      } else {
        console.log('Blocking rules disabled.');
      }
    });
  }
}
