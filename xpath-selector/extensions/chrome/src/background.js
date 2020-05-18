'use strict';

import './storage'

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ color: '#3aa757' }, () => {
        console.log("Installed.");
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [
                new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: { urlMatches: '(.*).com' }
                })
            ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});

chrome.browserAction.onClicked.addListener(tab => {
    let enabled;
    chrome.storage.promise.local.get(['enabled']).then(result => {
        if (!result.enabled) {
            enabled = true;
        } else {
            enabled = !result.enabled;
        }
        return chrome.storage.promise.local.set({ enabled: enabled });
    }).then(() => {
        chrome.tabs.query({active: true, currentWindow: true}, tabs => {
            chrome.tabs.sendMessage(tabs[0].id, {enabled: enabled}, response => {
            });
        });
    });
});
