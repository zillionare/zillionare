/**
 * @license resizeToFit 0.2.0-devel - Resize text until it fits to its container.
 * ©2019  Mathias Nater, Zürich (mathiasnater at gmail dot com)
 * https://github.com/mnater/resizeToFit
 *
 * Released under the MIT license
 * http://mnater.github.io/resizeToFit/LICENSE
 */

window.resizeToFit = (function makeResizeToFit() {
    "use strict";

    // Storage for elements to be fitted
    const collection = new Map();

    // The cssHandler-object, created by init()
    let cssHandler = null;

    /**
     * Factory for a CSS handling object
     * @param {CSSStyleSheet} styleSheet - An existing CSSOM styleSheet
     */
    function makeCSSHandler(styleSheet) {
        // Map selectors to rule-IDs
        const sel2Id = new Map();

        /**
         * Creates or changes a CSS rule.
         * @param {string} selector - The selector, where the properties are added to
         * @param {array} properties - Array of properties. e.g. ["color: red", "font-size: 12px"]
         */
        function setProp(selector, properties) {
            if (sel2Id.has(selector)) {
                // Add to existing rule
                const idx = sel2Id.get(selector);
                properties.forEach(function eachProp(prop) {
                    const propNameValue = prop.split(":");
                    const propName = propNameValue[0].trim();
                    const propValue = propNameValue[1].trim();
                    styleSheet.cssRules.item(idx).style.setProperty(
                        propName,
                        propValue
                    );
                });
            } else {
                // Create new rule
                let propString = "";
                properties.forEach(function eachProp(prop) {
                    propString += prop + "; ";
                });
                const idx = styleSheet.insertRule(
                    selector + "{" + propString + "}",
                    styleSheet.cssRules.length
                );
                sel2Id.set(selector, idx);
            }
        }

        /**
         * Delete properties for a specified selector
         * @param {string} selector - The selector, whose properties are deleted
         * @param {array} properties - Array of properties. e.g. ["color", "font-size"]
         */
        function deleteProp(selector, properties) {
            const idx = sel2Id.get(selector);
            properties.forEach(function eachProp(prop) {
                styleSheet.cssRules.item(idx).style.removeProperty(prop);
            });
        }

        return {
            deleteProp,
            setProp
        };
    }

    /**
     * Resize font-size of the element
     * @param {DOMElement} el - The element whose text is to be resized
     * @param {string} selector - The selector that found this element
     * @returns {undefined}
     */
    function calculateFontSize(elObj, selector) {
        // Previously calculated font-size for the same selector are stored in the `resizedSelectors`-Map.
        const currentFontSize =
            collection.get(selector).get("resizedFontSize") ||
            elObj.originalFontSize;

        /*
         * Calculate the font-size proportionally to clientWidth and scrollWidth
         * but don't grow bigger than originalFontSize or currentFontSize
         */
        const el = elObj.element;
        const newFontSize = Math.min(
            el.clientWidth / el.scrollWidth * elObj.originalFontSize,
            elObj.originalFontSize,
            currentFontSize
        );

        // Store font-size for this selector
        collection.get(selector).set("resizedFontSize", newFontSize);
    }

    /**
     * Resize each element previously collected by init
     * @returns {undefined}
     */
    function resize() {
        // Call calculateFontSize() for each element in collection
        collection.forEach(function eachSelectorC(selector) {
            // Restart from scratch
            selector.set("resizedFontSize", 0);

            // Set properties to get accurate results for clientWidth and scrollWidth
            cssHandler.setProp(
                selector.get("name"),
                ["overflow: hidden", "display: block", "font-size: " + selector.get("originalFontSize") + "px"]
            );

            // Calculate FontSize for each element
            selector.get("elements").forEach(function eachElement(elObj) {
                calculateFontSize(elObj, selector.get("name"));
            });

            // Remove properties needed for calculation, restoring original values
            cssHandler.deleteProp(selector.get("name"), ["overflow", "display"]);
        });

        // Repaint
        collection.forEach(function eachSelectorP(selector) {
            if (selector.get("originalFontSize") !== selector.get("resizedFontSize")) {
                cssHandler.setProp(
                    selector.get("name"),
                    ["font-size: " + selector.get("resizedFontSize") + "px"]
                );
            }
        });
    }

    /**
     * Create a styleSheet and collect all elements. Then call resize().
     * @param {array} selectors - An array of selectors that need to be resized
     * @returns {undefined}
     */
    function init(selectors) {
        // Let's create a new style sheet where we put the styles
        const styleEl = document.createElement("style");
        styleEl.id = "resizeToFit_Styles";
        styleEl.type = "text/css";
        document.head.appendChild(styleEl);

        // Create cssHandler to easily manipulate the style sheet
        cssHandler = makeCSSHandler(styleEl.sheet);

        // Find all elements according to user provided selectors
        selectors.forEach(function eachSelector(selector) {
            const nodeList = document.querySelectorAll(selector);
            const selectorData = new Map();
            let originalSelectorFontSize = 0;
            selectorData.set("name", selector);
            selectorData.set("elements", []);
            selectorData.set("resizedFontSize", 0);
            nodeList.forEach(function eachElement(element) {
                // Save original font-size to each element object
                const computedStyles = window.getComputedStyle(element);
                const originalElementFontSize = parseFloat(
                    computedStyles.fontSize
                );
                const elObj = Object.create(null);
                elObj.element = element;
                elObj.originalFontSize = originalElementFontSize;
                originalSelectorFontSize = Math.max(
                    originalSelectorFontSize,
                    originalElementFontSize
                );
                selectorData.get("elements").push(elObj);
            });
            selectorData.set("originalFontSize", originalSelectorFontSize);
            collection.set(selector, selectorData);
        });
        resize();
    }

    return {
        init,
        resize
    };
}());
