'use strict';

import uuidv4 from 'uuidv4';

export default class XpathContainer {
    constructor() {
        this.elm = document.createElement('ul');
        this.elm.id = uuidv4();
        this.children = new Map();
    }
    getElement() {
        return this.elm;
    }
    hasChild(key) {
        return this.children.has(key);
    }
    getHoverboxsIds(elm) {
        let ids = [];
        this.children.forEach(child => {
            ids.push(child.hoverBox.getId());
        });
        return ids;
    }
    getXpaths() {
        let res = [];
        this.children.forEach(child => {
            res.push(child.getXpath());
        });
        return res;

    }
    appendChild(newXpathItem) {
        this.children.set(newXpathItem.getElement().textContent, newXpathItem);
        this.elm.appendChild(newXpathItem.getElement());
    }
    removeChild(childXpath) {
        let toremove = this.children.get(childXpath);
        if (toremove) {
            toremove.remove();
            this.children.delete(childXpath);
        }
    }
    hideAll() {
        this.children.forEach(xpathItem => {
            xpathItem.hide();
        });
    }
    showAll() {
        this.children.forEach(xpathItem => {
            xpathItem.show();
        });
    }
}