// Service worker. Its only job today is opening the side panel: the panel
// talks to the content script directly via chrome.tabs.sendMessage, so there
// is no message relaying to do here. Kept deliberately thin — no reasoning
// lives in the client (docs/ARCHITECTURE.md, "dependency rule").

chrome.runtime.onInstalled.addListener(() => {
  // With this behaviour set, clicking the toolbar icon opens the panel
  // directly; registering an action.onClicked listener as well would be dead
  // code, because the listener does not fire while this is enabled.
  chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
});
