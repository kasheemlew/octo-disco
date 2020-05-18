'use strict';

import MainContainer from './mainContainer';
import HoverBox from './hoverBox';
import XpathItem from './xpathItem';
import { getIdx, getXpathArray, getXPathForElement, getElementByXPath, isDescendant } from './utils';

let mainContainer = new MainContainer();
document.body.appendChild(mainContainer.getElement());
document.body.appendChild(mainContainer.getSwitcher());
document.body.appendChild(mainContainer.getSubmit());


let hoverBox = new HoverBox();
document.body.appendChild(hoverBox.getElement());


let previousTarget;
let target;
let eventsManager = {
    mouseHoverEvent: e => {
        target = e.target;
        if (target === hoverBox.getElement()) {
            const hoveredElement = document.elementsFromPoint(e.clientX, e.clientY)[1];
            if (previousTarget === hoveredElement) {
                return;
            } else {
                target = hoveredElement;
            }
        } else {
            previousTarget = target;
        }
        hoverBox.setSize(target);
        hoverBox.setPosition(target);
    },
    elementClickEvent: e => {
        if (isDescendant(mainContainer.xpathContainer.getElement(), target)) {
            mainContainer.xpathContainer.removeChild(target.textContent);
        } else if (
            isDescendant(mainContainer.getElement(), target) || 
            (target.id == mainContainer.getId()) || 
            (target.id == mainContainer.getSwitcher().id) ||
            (target.id == mainContainer.getSubmit().id) ||
            (target.id == hoverBox.id) ||
            mainContainer.xpathContainer.getHoverboxsIds().includes(target.id)
        ) {
            console.log('do nothing');
        } else {
            if (mainContainer.xpathContainer.hasChild(getXPathForElement(target))) {
                return;
            }
            let newXpathItem = new XpathItem(target);
            mainContainer.xpathContainer.appendChild(newXpathItem);
            document.body.appendChild(newXpathItem.hoverBox.getElement());
            newXpathItem.getElement().addEventListener('click', eventsManager.elementClickEvent);
        }
    }
};


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('get enabled value: ' + request.enabled);
    if (request.enabled === true) {
        enable();
    } else {
        disable();
    }
    sendResponse({ msg: 'content get value:' + request.diable });
});

// Enable Extension
function enable() {
    console.log('enable extension!');
    document.addEventListener('mousemove', eventsManager.mouseHoverEvent);
    document.addEventListener('click', eventsManager.elementClickEvent);
    hoverBox.getElement().style.display = 'block';
    mainContainer.showElements();
}

// Disable Extension
function disable() {
    console.log('disable extension!');
    document.removeEventListener('mousemove', eventsManager.mouseHoverEvent);
    document.removeEventListener('click', eventsManager.elementClickEvet);
    hoverBox.getElement().style.display = 'none';
    mainContainer.hideElements();
}
