chrome.storage.promise = {
    local: {
        get: keys => {
            return new Promise((resolve, reject) => {
                chrome.storage.local.get(keys, items => {
                    let err = chrome.runtime.lastError;
                    if (err) {
                        reject(err);
                    } else {
                        resolve(items);
                    }
                });
            });
        },
        set: items => {
            return new Promise((resolve, reject) => {
                chrome.storage.local.set(items, () => {
                    let err = chrome.runtime.lastError;
                    if (err) {
                        reject(err);
                    } else {
                        resolve(err);
                    }
                });
            });
        }
    }
}