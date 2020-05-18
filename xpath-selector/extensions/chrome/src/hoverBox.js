'use strict';

import uuidv4 from 'uuidv4';

export default class HoverBox {
    constructor() {
        this.elm = document.createElement("div");
        this.elm.style.position = 'absolute';
        this.elm.style.background = 'rgba(112, 255, 255, 0.77)';
        this.elm.style.zIndex = '0';
        this.elm.style.display = 'block';
        this.elm.id = uuidv4();
        this.boxBorder = 4;
    }
    setPosition(target) {
        const targetOffset = target.getBoundingClientRect();
        this.elm.style.top = targetOffset.top + window.scrollY - this.boxBorder + "px";
        this.elm.style.left = targetOffset.left + window.scrollX - this.boxBorder + "px";
    }
    setSize(target) {
        const targetOffset = target.getBoundingClientRect();
        const targetHeight = targetOffset.height;
        const targetWidth = targetOffset.width;
        this.elm.style.width = targetWidth + this.boxBorder * 2 + "px";
        this.elm.style.height = targetHeight + this.boxBorder * 2 + "px";
    }
    hide() {
        this.elm.style.display = 'none';
    }
    show() {
        this.elm.style.display = 'block';
    }
    getId() {
        return this.elm.id;
    }
    getElement() {
        return this.elm;
    }
    remove() {
        this.elm.remove();
    }
}