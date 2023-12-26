// fit-to-width.js

/* 

Fits text to the width of its DOM container using various methods.

The core function is ftw_fit(), to which you pass a DOM element or an array of DOM elements. This applies various width adjustment methods, until either succeeding or giving up. Default (which is easily configurable) is to first try CSS font-stretch, then CSS letter-spacing, then finally CSS transform.

*/

// set up defaults for each method
const ftw_methods = {
	"font-stretch": {min: 0.00001, max: 0x8000 - 1/0x10000, bsFunction: ftw_setFontStretch},
	"font-variation-settings:wdth": {min: -0x8000, max: 0x8000 - 1/0x10000, bsFunction: ftw_setFontVariationSettingsWdth},
	"letter-spacing": {min: -0.05, max: 1, bsFunction: ftw_setLetterSpacing},
	"word-spacing": {min: -0.2, max: 20, bsFunction: ftw_setWordSpacing},
	"transform": {},
	"ligatures": {}
};

// function to check if iterable
const ftw_ArgIsIterable = object => object != null && typeof object[Symbol.iterator] === 'function';

function ftw_setFontStretch (el, val, operation) {
	el.style.fontStretch = val + "%";
}

function ftw_setFontVariationSettingsWdth (el, val, operation) {
	let fvsString = "'wdth' " + val;
	if (operation.axes)
		fvsString += "," + operation.axes;
	el.style.fontVariationSettings = fvsString;
}

function ftw_setLetterSpacing (el, val) {
	el.style.letterSpacing = val + "em";
}

function ftw_setWordSpacing (el, val) {
	el.style.wordSpacing = val + "em";
}

function ftw_Operation (method, min, max, maxDiff, maxIterations, axes) {
	if (ftw_methods[method]) {
		this.method = method;
		this.min = min === undefined ? ftw_methods[method].min : min;
		this.max = min === undefined ? ftw_methods[method].max : max;
		this.bsFunction = ftw_methods[method].bsFunction;
		this.maxDiff = maxDiff === undefined ? 1 : maxDiff; // allows 0
		this.maxIterations = maxIterations === undefined ? 50 : maxIterations;
		this.axes = axes;
	}
	else
		this.method = null;
}

// main function
function ftw_fit (elements, ftwOperations, targetWidth) {

	let startTime = performance.now();
	let config = {
		operations: ftwOperations || ["font-variation-settings:wdth", "transform"]
	};
	let els;

	// get all elements selected by the string elements
	if (typeof elements === "string")
		els = document.querySelectorAll(elements);
	// is elements already a NodeList or array of elements? if so, fine; otherwise make it an array
	else if (ftw_ArgIsIterable(elements))
		els = elements;
	else
		els = [elements]; // convert to an array

	// user config?
	if (!Array.isArray(config.operations)) {
		if (!config.operations)
			config.operations = ["font-stretch"];
		else if (typeof config.operations === "string" || typeof config.operations === "object")
			config.operations = [config.operations];
	}

	// for each element supplied by the user
	for (let el of els)
	{
		let success = false;
		config.targetWidth = targetWidth || el.clientWidth;
		el.style.whiteSpace = "nowrap";
		el.style.width = "max-content";
		el.style.transform = "none";

		// for each operation specified by the user
		for (let op of config.operations) {
			let operation;
			if (typeof op === "string")
				operation = new ftw_Operation(op);
			else
				operation = new ftw_Operation(op.method, op.min, op.max, op.maxDiff, op.maxIterations, op.axes);

			switch (operation.method) {
				case "transform": ftw_fit_transform (el, config); break;
				case "ligatures": ftw_fit_ligatures (el, config); break;
				case "font-stretch":
				case "font-variation-settings:wdth":
				case "letter-spacing":
				case "word-spacing":
					success = ftw_fit_binary_search (el, operation, config.targetWidth);
					break;
				// ignore unrecognized methods
			}

			if (success)
			{
				console.log (operation.method);
				break;
			}
		}

		// reset element width
		el.style.width = config.targetWidth+"px"; // TODO: revert it to its original getComputedStyle() width, e.g. "10em"?
	}

	config.elapsedTime = performance.now() - startTime;
	return config;
}

function ftw_fit_binary_search (el, operation, targetWidth) {

	let iterations = 0;
	let min = operation.min, max = operation.max;
	let minClientWidth, maxClientWidth;
	let done = false;
	let success = false;

	// checks before binary search
	if (min > max)
		done = true;
	else {
		operation.bsFunction(el, min, operation); // above the min?
		if ((minClientWidth=el.clientWidth) >= targetWidth) {
			done = true;
			if (minClientWidth == targetWidth)
				success = true;
		}
		else {
			operation.bsFunction(el, max, operation); // below the max?
			if ((maxClientWidth=el.clientWidth) < targetWidth) {
				done = true;
				if (maxClientWidth == targetWidth)
					success = true;
			}
			else if (minClientWidth >= maxClientWidth) {// check width at min != width at max
				done = true;
			}
		}
	}

	// the binary search
	while (!done) {

		let val = 0.5 * (min+max);
		operation.bsFunction(el, val, operation); // set the CSS
		let diff = el.clientWidth - targetWidth; // are we under or over?
		if (diff <= 0) {
			if (diff > -operation.maxDiff) { // SUCCESS: <maxDiff
				console.log ("success, diff="+diff);
				success = true;
				done = true;
			}
			else
				min = val; // we guessed too low
		}
		else
			max = val; // we guessed too high

		// next iteration
		iterations++;
		if (iterations >= operation.maxIterations) { // FAIL: wght did not converge
			done = true;
			if (diff>0) // better to leave the element at minWdth rather than > targetWidth
				operation.bsFunction(el, min, operation);
		}
	}

	return success;
}


function ftw_fit_transform (el, config) {
	el.style.transformOrigin = "left";
	el.style.transform = "scale(" + (config.targetWidth / el.clientWidth) + ",1)";
}


function ftw_fit_ligatures (el, config) {
	el.style.fontFeatureSettings = "'liga' 1, 'dlig' 1";
	// EXPERIMENTAL
	// * to reduce width, should turn on ligatures
	// * to increase width, should turn off ligatures
	// * for both, should check the effect on width
	// * should really add these to any existing settings using getComputedStyle
	// Good candidate string: "VAMPIRE HELL" set in Skia
}

