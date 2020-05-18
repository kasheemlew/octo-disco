'use strict';

import uuidv4 from 'uuidv4';
import XpathContainer from './xpathContainer';

export default class MainContainer {
    constructor() {
        this.switcherSize = '30px';
        this.switcher = this.createSwitcher();
        this.submitBtn = this.createSubmit();
        this.elm = this.createElement();
        this.createHeader();
        // this.createInputArea();
        this.createXpathContainer();
    }
    getId() {
        return this.elm.id;
    }
    createElement() {
        let elm = document.createElement('div');
        elm.style.position = 'fixed';
        elm.style.background = 'rgba(0, 0, 0, 0.5)';
        elm.style.zIndex = '9999';
        elm.style.width = '30%';
        elm.style.height = '30%';
        elm.style.top = '0';
        elm.style.right = this.switcherSize;
        elm.style.display = 'none';
        elm.style.padding = '5px';
        elm.style.overflowY = 'scroll';
        elm.id = uuidv4();
        return elm;
    }
    createSwitcher() {
        let switcher = document.createElement('div');
        switcher.id = uuidv4();
        switcher.style.zIndex = '9999';
        switcher.style.position = 'fixed';
        switcher.style.display = 'none';
        switcher.style.background = 'black';
        switcher.style.color = 'white';
        switcher.style.width = this.switcherSize;
        switcher.style.height = this.switcherSize;
        switcher.style.top = '0';
        switcher.style.right = '0';
        switcher.textContent = '-';
        switcher.addEventListener('click', () => {
            if (this.elm.style.display == 'block') {
                this.elm.style.display = 'none';
                switcher.textContent = '+';
            } else if (this.elm.style.display == 'none') {
                this.elm.style.display = 'block';
                switcher.textContent = '-';
            }
        });
        return switcher;
    }
    createSubmit() {
        let submitBtn = document.createElement('div')
        submitBtn.id = uuidv4();
        submitBtn.style.zIndex = '9999';
        submitBtn.style.position = 'fixed';
        submitBtn.style.display = 'none';
        submitBtn.style.background = 'black';
        submitBtn.style.color = 'white';
        submitBtn.style.width = this.switcherSize;
        submitBtn.style.height = this.switcherSize;
        submitBtn.style.top = parseInt(this.switcherSize)+2+'px';
        submitBtn.style.right = '0';
        submitBtn.textContent = 'Sub';
        submitBtn.addEventListener('click', () => {
            fetch('http://localhost:5000/xpaths', {
                method: 'POST',
                body: JSON.stringify({
                    url: window.location.href,
                    xpaths: this.xpathContainer.getXpaths()
                })
            }).then(res => {
                alert(JSON.stringify(res.json()))
            });
        });
        return submitBtn;
    }
    getElement() {
        return this.elm;
    }
    getSwitcher() {
        return this.switcher;
    }
    getSubmit() {
        return this.submitBtn;
    }
    createHeader() {
        let header = document.createElement('h3');
        header.textContent = 'Xpath: ';
        header.style.color = 'white';
        header.style.width = '30%';
        this.elm.appendChild(header);
    }
    createInputArea() {
        let inputArea = document.createElement('input');
        inputArea.style.width = '100%';
        inputArea.type = 'text';
        inputArea.id = 'xpathInputArea';
        this.elm.appendChild(inputArea);
    }
    createXpathContainer() {
        this.xpathContainer = new XpathContainer();
        this.elm.appendChild(this.xpathContainer.getElement());
    }
    showElements() {
        this.switcher.style.display = 'block';
        this.switcher.textContent = '-';
        this.elm.style.display = 'block';
        this.submitBtn.style.display = 'block';

        this.xpathContainer.showAll();
    }
    hideElements() {
        this.switcher.style.display = 'none';
        this.elm.style.display = 'none';
        this.submitBtn.style.display = 'none';

        this.xpathContainer.hideAll();
    }
}