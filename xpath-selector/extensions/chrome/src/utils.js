export const getIdx = (sib, localName) => {
    if (sib) {
        return getIdx(sib.previousElementSibling, localName || sib.localName) + (sib.localName == localName);
    }
    return 1;
};

export const getXpathArray = elm => {
    // nodetype===1 -> ElementNode like <p>, <div>
    let xpathSegs;
    if (!elm || elm.nodeType !== 1) {
        xpathSegs = [''];
    } else {
        if (elm.id && document.getElementById(elm.id) === elm) {
            xpathSegs = [`id("${elm.id}")`];
        } else {
            xpathSegs = [
                ...getXpathArray(elm.parentNode),
                `${elm.localName.toLowerCase()}[${getIdx(elm)}]`,
            ];
        }
    }
    return xpathSegs;
};

export const getXPathForElement = element => {
    return getXpathArray(element).join('/');
};

export const getElementByXPath = path => {
    return (new XPathEvaluator())
        .evaluate(path, document.documentElement, null,
            XPathResult.FIRST_ORDERED_NODE_TYPE, null)
        .singleNodeValue;
};

export const isDescendant = (parent, child) => {
     let node = child.parentNode;
     if (!node || (node.nodeType === 1 && !node.parentNode)) {
         return true;
     }
     while (node != null) {
         if (node == parent) {
             return true;
         }
         node = node.parentNode;
     }
     return false;
};