'use strict';

import uuidv4 from 'uuidv4';
import HoverBox from './hoverBox';
import { getXPathForElement } from './utils';

export default class XpathItem {
    constructor(target) {
        this.elm = document.createElement('li');
        this.elm.textContent = getXPathForElement(target);
        this.elm.style.color = 'white';
        this.elm.id = uuidv4();

        this.hoverBox = new HoverBox();
        this.hoverBox.setSize(target);
        this.hoverBox.setPosition(target);
    }
    hide() {
        this.hoverBox.hide();
    }
    show() {
        this.hoverBox.show();
    }
    getId() {
        return this.elm.id;
    }
    getElement() {
        return this.elm;
    }
    getXpath() {
        return this.elm.textContent;
    }
    remove() {
        this.hoverBox.remove();
        this.getElement().remove();
    }
}