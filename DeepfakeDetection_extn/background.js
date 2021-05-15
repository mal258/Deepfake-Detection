
'use strict';

chrome.runtime.onInstalled.addListener(() => {
  console.log("from background");

  var cacheResults = {};

  chrome.storage.local.set(cacheResults);
});


