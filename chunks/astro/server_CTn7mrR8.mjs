import 'piccolore';
import { clsx } from 'clsx';
import { escape } from 'html-escaper';
import { encodeBase64, encodeHexUpperCase, decodeBase64 } from '@oslojs/encoding';
import { z } from 'zod';
import 'cssesc';

function normalizeLF(code) {
  return code.replace(/\r\n|\r(?!\n)|\n/g, "\n");
}

function codeFrame(src, loc) {
  if (!loc || loc.line === void 0 || loc.column === void 0) {
    return "";
  }
  const lines = normalizeLF(src).split("\n").map((ln) => ln.replace(/\t/g, "  "));
  const visibleLines = [];
  for (let n = -2; n <= 2; n++) {
    if (lines[loc.line + n]) visibleLines.push(loc.line + n);
  }
  let gutterWidth = 0;
  for (const lineNo of visibleLines) {
    let w = `> ${lineNo}`;
    if (w.length > gutterWidth) gutterWidth = w.length;
  }
  let output = "";
  for (const lineNo of visibleLines) {
    const isFocusedLine = lineNo === loc.line - 1;
    output += isFocusedLine ? "> " : "  ";
    output += `${lineNo + 1} | ${lines[lineNo]}
`;
    if (isFocusedLine)
      output += `${Array.from({ length: gutterWidth }).join(" ")}  | ${Array.from({
        length: loc.column
      }).join(" ")}^
`;
  }
  return output;
}

class AstroError extends Error {
  loc;
  title;
  hint;
  frame;
  type = "AstroError";
  constructor(props, options) {
    const { name, title, message, stack, location, hint, frame } = props;
    super(message, options);
    this.title = title;
    this.name = name;
    if (message) this.message = message;
    this.stack = stack ? stack : this.stack;
    this.loc = location;
    this.hint = hint;
    this.frame = frame;
  }
  setLocation(location) {
    this.loc = location;
  }
  setName(name) {
    this.name = name;
  }
  setMessage(message) {
    this.message = message;
  }
  setHint(hint) {
    this.hint = hint;
  }
  setFrame(source, location) {
    this.frame = codeFrame(source, location);
  }
  static is(err) {
    return err?.type === "AstroError";
  }
}

const MissingMediaQueryDirective = {
  name: "MissingMediaQueryDirective",
  title: "Missing value for `client:media` directive.",
  message: 'Media query not provided for `client:media` directive. A media query similar to `client:media="(max-width: 600px)"` must be provided'
};
const NoMatchingRenderer = {
  name: "NoMatchingRenderer",
  title: "No matching renderer found.",
  message: (componentName, componentExtension, plural, validRenderersCount) => `Unable to render \`${componentName}\`.

${validRenderersCount > 0 ? `There ${plural ? "are" : "is"} ${validRenderersCount} renderer${plural ? "s" : ""} configured in your \`astro.config.mjs\` file,
but ${plural ? "none were" : "it was not"} able to server-side render \`${componentName}\`.` : `No valid renderer was found ${componentExtension ? `for the \`.${componentExtension}\` file extension.` : `for this file extension.`}`}`,
  hint: (probableRenderers) => `Did you mean to enable the ${probableRenderers} integration?

See https://docs.astro.build/en/guides/framework-components/ for more information on how to install and configure integrations.`
};
const NoClientOnlyHint = {
  name: "NoClientOnlyHint",
  title: "Missing hint on client:only directive.",
  message: (componentName) => `Unable to render \`${componentName}\`. When using the \`client:only\` hydration strategy, Astro needs a hint to use the correct renderer.`,
  hint: (probableRenderers) => `Did you mean to pass \`client:only="${probableRenderers}"\`? See https://docs.astro.build/en/reference/directives-reference/#clientonly for more information on client:only`
};
const NoMatchingImport = {
  name: "NoMatchingImport",
  title: "No import found for component.",
  message: (componentName) => `Could not render \`${componentName}\`. No matching import has been found for \`${componentName}\`.`,
  hint: "Please make sure the component is properly imported."
};
const InvalidComponentArgs = {
  name: "InvalidComponentArgs",
  title: "Invalid component arguments.",
  message: (name) => `Invalid arguments passed to${name ? ` <${name}>` : ""} component.`,
  hint: "Astro components cannot be rendered directly via function call, such as `Component()` or `{items.map(Component)}`."
};
const AstroGlobUsedOutside = {
  name: "AstroGlobUsedOutside",
  title: "Astro.glob() used outside of an Astro file.",
  message: (globStr) => `\`Astro.glob(${globStr})\` can only be used in \`.astro\` files. \`import.meta.glob(${globStr})\` can be used instead to achieve a similar result.`,
  hint: "See Vite's documentation on `import.meta.glob` for more information: https://vite.dev/guide/features.html#glob-import"
};
const AstroGlobNoMatch = {
  name: "AstroGlobNoMatch",
  title: "Astro.glob() did not match any files.",
  message: (globStr) => `\`Astro.glob(${globStr})\` did not return any matching files.`,
  hint: "Check the pattern for typos."
};

function validateArgs(args) {
  if (args.length !== 3) return false;
  if (!args[0] || typeof args[0] !== "object") return false;
  return true;
}
function baseCreateComponent(cb, moduleId, propagation) {
  const name = moduleId?.split("/").pop()?.replace(".astro", "") ?? "";
  const fn = (...args) => {
    if (!validateArgs(args)) {
      throw new AstroError({
        ...InvalidComponentArgs,
        message: InvalidComponentArgs.message(name)
      });
    }
    return cb(...args);
  };
  Object.defineProperty(fn, "name", { value: name, writable: false });
  fn.isAstroComponentFactory = true;
  fn.moduleId = moduleId;
  fn.propagation = propagation;
  return fn;
}
function createComponentWithOptions(opts) {
  const cb = baseCreateComponent(opts.factory, opts.moduleId, opts.propagation);
  return cb;
}
function createComponent(arg1, moduleId, propagation) {
  if (typeof arg1 === "function") {
    return baseCreateComponent(arg1, moduleId, propagation);
  } else {
    return createComponentWithOptions(arg1);
  }
}

const ASTRO_VERSION = "5.18.2";
const NOOP_MIDDLEWARE_HEADER = "X-Astro-Noop";

function createAstroGlobFn() {
  const globHandler = (importMetaGlobResult) => {
    console.warn(`Astro.glob is deprecated and will be removed in a future major version of Astro.
Use import.meta.glob instead: https://vitejs.dev/guide/features.html#glob-import`);
    if (typeof importMetaGlobResult === "string") {
      throw new AstroError({
        ...AstroGlobUsedOutside,
        message: AstroGlobUsedOutside.message(JSON.stringify(importMetaGlobResult))
      });
    }
    let allEntries = [...Object.values(importMetaGlobResult)];
    if (allEntries.length === 0) {
      throw new AstroError({
        ...AstroGlobNoMatch,
        message: AstroGlobNoMatch.message(JSON.stringify(importMetaGlobResult))
      });
    }
    return Promise.all(allEntries.map((fn) => fn()));
  };
  return globHandler;
}
function createAstro(site) {
  return {
    site: new URL(site) ,
    generator: `Astro v${ASTRO_VERSION}`,
    glob: createAstroGlobFn()
  };
}

function isPromise(value) {
  return !!value && typeof value === "object" && "then" in value && typeof value.then === "function";
}
async function* streamAsyncIterator(stream) {
  const reader = stream.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) return;
      yield value;
    }
  } finally {
    reader.releaseLock();
  }
}

const escapeHTML = escape;
class HTMLBytes extends Uint8Array {
}
Object.defineProperty(HTMLBytes.prototype, Symbol.toStringTag, {
  get() {
    return "HTMLBytes";
  }
});
class HTMLString extends String {
  get [Symbol.toStringTag]() {
    return "HTMLString";
  }
}
const markHTMLString = (value) => {
  if (value instanceof HTMLString) {
    return value;
  }
  if (typeof value === "string") {
    return new HTMLString(value);
  }
  return value;
};
function isHTMLString(value) {
  return Object.prototype.toString.call(value) === "[object HTMLString]";
}
function markHTMLBytes(bytes) {
  return new HTMLBytes(bytes);
}
function hasGetReader(obj) {
  return typeof obj.getReader === "function";
}
async function* unescapeChunksAsync(iterable) {
  if (hasGetReader(iterable)) {
    for await (const chunk of streamAsyncIterator(iterable)) {
      yield unescapeHTML(chunk);
    }
  } else {
    for await (const chunk of iterable) {
      yield unescapeHTML(chunk);
    }
  }
}
function* unescapeChunks(iterable) {
  for (const chunk of iterable) {
    yield unescapeHTML(chunk);
  }
}
function unescapeHTML(str) {
  if (!!str && typeof str === "object") {
    if (str instanceof Uint8Array) {
      return markHTMLBytes(str);
    } else if (str instanceof Response && str.body) {
      const body = str.body;
      return unescapeChunksAsync(body);
    } else if (typeof str.then === "function") {
      return Promise.resolve(str).then((value) => {
        return unescapeHTML(value);
      });
    } else if (str[Symbol.for("astro:slot-string")]) {
      return str;
    } else if (Symbol.iterator in str) {
      return unescapeChunks(str);
    } else if (Symbol.asyncIterator in str || hasGetReader(str)) {
      return unescapeChunksAsync(str);
    }
  }
  return markHTMLString(str);
}

function isAstroComponentFactory(obj) {
  return obj == null ? false : obj.isAstroComponentFactory === true;
}
function isAPropagatingComponent(result, factory) {
  const hint = getPropagationHint(result, factory);
  return hint === "in-tree" || hint === "self";
}
function getPropagationHint(result, factory) {
  let hint = factory.propagation || "none";
  if (factory.moduleId && result.componentMetadata.has(factory.moduleId) && hint === "none") {
    hint = result.componentMetadata.get(factory.moduleId).propagation;
  }
  return hint;
}

const PROP_TYPE = {
  Value: 0,
  JSON: 1,
  // Actually means Array
  RegExp: 2,
  Date: 3,
  Map: 4,
  Set: 5,
  BigInt: 6,
  URL: 7,
  Uint8Array: 8,
  Uint16Array: 9,
  Uint32Array: 10,
  Infinity: 11
};
function serializeArray(value, metadata = {}, parents = /* @__PURE__ */ new WeakSet()) {
  if (parents.has(value)) {
    throw new Error(`Cyclic reference detected while serializing props for <${metadata.displayName} client:${metadata.hydrate}>!

Cyclic references cannot be safely serialized for client-side usage. Please remove the cyclic reference.`);
  }
  parents.add(value);
  const serialized = value.map((v) => {
    return convertToSerializedForm(v, metadata, parents);
  });
  parents.delete(value);
  return serialized;
}
function serializeObject(value, metadata = {}, parents = /* @__PURE__ */ new WeakSet()) {
  if (parents.has(value)) {
    throw new Error(`Cyclic reference detected while serializing props for <${metadata.displayName} client:${metadata.hydrate}>!

Cyclic references cannot be safely serialized for client-side usage. Please remove the cyclic reference.`);
  }
  parents.add(value);
  const serialized = Object.fromEntries(
    Object.entries(value).map(([k, v]) => {
      return [k, convertToSerializedForm(v, metadata, parents)];
    })
  );
  parents.delete(value);
  return serialized;
}
function convertToSerializedForm(value, metadata = {}, parents = /* @__PURE__ */ new WeakSet()) {
  const tag = Object.prototype.toString.call(value);
  switch (tag) {
    case "[object Date]": {
      return [PROP_TYPE.Date, value.toISOString()];
    }
    case "[object RegExp]": {
      return [PROP_TYPE.RegExp, value.source];
    }
    case "[object Map]": {
      return [PROP_TYPE.Map, serializeArray(Array.from(value), metadata, parents)];
    }
    case "[object Set]": {
      return [PROP_TYPE.Set, serializeArray(Array.from(value), metadata, parents)];
    }
    case "[object BigInt]": {
      return [PROP_TYPE.BigInt, value.toString()];
    }
    case "[object URL]": {
      return [PROP_TYPE.URL, value.toString()];
    }
    case "[object Array]": {
      return [PROP_TYPE.JSON, serializeArray(value, metadata, parents)];
    }
    case "[object Uint8Array]": {
      return [PROP_TYPE.Uint8Array, Array.from(value)];
    }
    case "[object Uint16Array]": {
      return [PROP_TYPE.Uint16Array, Array.from(value)];
    }
    case "[object Uint32Array]": {
      return [PROP_TYPE.Uint32Array, Array.from(value)];
    }
    default: {
      if (value !== null && typeof value === "object") {
        return [PROP_TYPE.Value, serializeObject(value, metadata, parents)];
      }
      if (value === Infinity) {
        return [PROP_TYPE.Infinity, 1];
      }
      if (value === -Infinity) {
        return [PROP_TYPE.Infinity, -1];
      }
      if (value === void 0) {
        return [PROP_TYPE.Value];
      }
      return [PROP_TYPE.Value, value];
    }
  }
}
function serializeProps(props, metadata) {
  const serialized = JSON.stringify(serializeObject(props, metadata));
  return serialized;
}

const transitionDirectivesToCopyOnIsland = Object.freeze([
  "data-astro-transition-scope",
  "data-astro-transition-persist",
  "data-astro-transition-persist-props"
]);
function extractDirectives(inputProps, clientDirectives) {
  let extracted = {
    isPage: false,
    hydration: null,
    props: {},
    propsWithoutTransitionAttributes: {}
  };
  for (const [key, value] of Object.entries(inputProps)) {
    if (key.startsWith("server:")) {
      if (key === "server:root") {
        extracted.isPage = true;
      }
    }
    if (key.startsWith("client:")) {
      if (!extracted.hydration) {
        extracted.hydration = {
          directive: "",
          value: "",
          componentUrl: "",
          componentExport: { value: "" }
        };
      }
      switch (key) {
        case "client:component-path": {
          extracted.hydration.componentUrl = value;
          break;
        }
        case "client:component-export": {
          extracted.hydration.componentExport.value = value;
          break;
        }
        // This is a special prop added to prove that the client hydration method
        // was added statically.
        case "client:component-hydration": {
          break;
        }
        case "client:display-name": {
          break;
        }
        default: {
          extracted.hydration.directive = key.split(":")[1];
          extracted.hydration.value = value;
          if (!clientDirectives.has(extracted.hydration.directive)) {
            const hydrationMethods = Array.from(clientDirectives.keys()).map((d) => `client:${d}`).join(", ");
            throw new Error(
              `Error: invalid hydration directive "${key}". Supported hydration methods: ${hydrationMethods}`
            );
          }
          if (extracted.hydration.directive === "media" && typeof extracted.hydration.value !== "string") {
            throw new AstroError(MissingMediaQueryDirective);
          }
          break;
        }
      }
    } else {
      extracted.props[key] = value;
      if (!transitionDirectivesToCopyOnIsland.includes(key)) {
        extracted.propsWithoutTransitionAttributes[key] = value;
      }
    }
  }
  for (const sym of Object.getOwnPropertySymbols(inputProps)) {
    extracted.props[sym] = inputProps[sym];
    extracted.propsWithoutTransitionAttributes[sym] = inputProps[sym];
  }
  return extracted;
}
async function generateHydrateScript(scriptOptions, metadata) {
  const { renderer, result, astroId, props, attrs } = scriptOptions;
  const { hydrate, componentUrl, componentExport } = metadata;
  if (!componentExport.value) {
    throw new AstroError({
      ...NoMatchingImport,
      message: NoMatchingImport.message(metadata.displayName)
    });
  }
  const island = {
    children: "",
    props: {
      // This is for HMR, probably can avoid it in prod
      uid: astroId
    }
  };
  if (attrs) {
    for (const [key, value] of Object.entries(attrs)) {
      island.props[key] = escapeHTML(value);
    }
  }
  island.props["component-url"] = await result.resolve(decodeURI(componentUrl));
  if (renderer.clientEntrypoint) {
    island.props["component-export"] = componentExport.value;
    island.props["renderer-url"] = await result.resolve(
      decodeURI(renderer.clientEntrypoint.toString())
    );
    island.props["props"] = escapeHTML(serializeProps(props, metadata));
  }
  island.props["ssr"] = "";
  island.props["client"] = hydrate;
  let beforeHydrationUrl = await result.resolve("astro:scripts/before-hydration.js");
  if (beforeHydrationUrl.length) {
    island.props["before-hydration-url"] = beforeHydrationUrl;
  }
  island.props["opts"] = escapeHTML(
    JSON.stringify({
      name: metadata.displayName,
      value: metadata.hydrateArgs || ""
    })
  );
  transitionDirectivesToCopyOnIsland.forEach((name) => {
    if (typeof props[name] !== "undefined") {
      island.props[name] = props[name];
    }
  });
  return island;
}

/**
 * shortdash - https://github.com/bibig/node-shorthash
 *
 * @license
 *
 * (The MIT License)
 *
 * Copyright (c) 2013 Bibig <bibig@me.com>
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */
const dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY";
const binary = dictionary.length;
function bitwise(str) {
  let hash = 0;
  if (str.length === 0) return hash;
  for (let i = 0; i < str.length; i++) {
    const ch = str.charCodeAt(i);
    hash = (hash << 5) - hash + ch;
    hash = hash & hash;
  }
  return hash;
}
function shorthash(text) {
  let num;
  let result = "";
  let integer = bitwise(text);
  const sign = integer < 0 ? "Z" : "";
  integer = Math.abs(integer);
  while (integer >= binary) {
    num = integer % binary;
    integer = Math.floor(integer / binary);
    result = dictionary[num] + result;
  }
  if (integer > 0) {
    result = dictionary[integer] + result;
  }
  return sign + result;
}

const headAndContentSym = Symbol.for("astro.headAndContent");
function isHeadAndContent(obj) {
  return typeof obj === "object" && obj !== null && !!obj[headAndContentSym];
}
function createThinHead() {
  return {
    [headAndContentSym]: true
  };
}

var astro_island_prebuilt_default = `(()=>{var A=Object.defineProperty;var g=(i,o,a)=>o in i?A(i,o,{enumerable:!0,configurable:!0,writable:!0,value:a}):i[o]=a;var d=(i,o,a)=>g(i,typeof o!="symbol"?o+"":o,a);{let i={0:t=>m(t),1:t=>a(t),2:t=>new RegExp(t),3:t=>new Date(t),4:t=>new Map(a(t)),5:t=>new Set(a(t)),6:t=>BigInt(t),7:t=>new URL(t),8:t=>new Uint8Array(t),9:t=>new Uint16Array(t),10:t=>new Uint32Array(t),11:t=>1/0*t},o=t=>{let[l,e]=t;return l in i?i[l](e):void 0},a=t=>t.map(o),m=t=>typeof t!="object"||t===null?t:Object.fromEntries(Object.entries(t).map(([l,e])=>[l,o(e)]));class y extends HTMLElement{constructor(){super(...arguments);d(this,"Component");d(this,"hydrator");d(this,"hydrate",async()=>{var b;if(!this.hydrator||!this.isConnected)return;let e=(b=this.parentElement)==null?void 0:b.closest("astro-island[ssr]");if(e){e.addEventListener("astro:hydrate",this.hydrate,{once:!0});return}let c=this.querySelectorAll("astro-slot"),n={},h=this.querySelectorAll("template[data-astro-template]");for(let r of h){let s=r.closest(this.tagName);s!=null&&s.isSameNode(this)&&(n[r.getAttribute("data-astro-template")||"default"]=r.innerHTML,r.remove())}for(let r of c){let s=r.closest(this.tagName);s!=null&&s.isSameNode(this)&&(n[r.getAttribute("name")||"default"]=r.innerHTML)}let p;try{p=this.hasAttribute("props")?m(JSON.parse(this.getAttribute("props"))):{}}catch(r){let s=this.getAttribute("component-url")||"<unknown>",v=this.getAttribute("component-export");throw v&&(s+=\` (export \${v})\`),console.error(\`[hydrate] Error parsing props for component \${s}\`,this.getAttribute("props"),r),r}let u;await this.hydrator(this)(this.Component,p,n,{client:this.getAttribute("client")}),this.removeAttribute("ssr"),this.dispatchEvent(new CustomEvent("astro:hydrate"))});d(this,"unmount",()=>{this.isConnected||this.dispatchEvent(new CustomEvent("astro:unmount"))})}disconnectedCallback(){document.removeEventListener("astro:after-swap",this.unmount),document.addEventListener("astro:after-swap",this.unmount,{once:!0})}connectedCallback(){if(!this.hasAttribute("await-children")||document.readyState==="interactive"||document.readyState==="complete")this.childrenConnectedCallback();else{let e=()=>{document.removeEventListener("DOMContentLoaded",e),c.disconnect(),this.childrenConnectedCallback()},c=new MutationObserver(()=>{var n;((n=this.lastChild)==null?void 0:n.nodeType)===Node.COMMENT_NODE&&this.lastChild.nodeValue==="astro:end"&&(this.lastChild.remove(),e())});c.observe(this,{childList:!0}),document.addEventListener("DOMContentLoaded",e)}}async childrenConnectedCallback(){let e=this.getAttribute("before-hydration-url");e&&await import(e),this.start()}async start(){let e=JSON.parse(this.getAttribute("opts")),c=this.getAttribute("client");if(Astro[c]===void 0){window.addEventListener(\`astro:\${c}\`,()=>this.start(),{once:!0});return}try{await Astro[c](async()=>{let n=this.getAttribute("renderer-url"),[h,{default:p}]=await Promise.all([import(this.getAttribute("component-url")),n?import(n):()=>()=>{}]),u=this.getAttribute("component-export")||"default";if(!u.includes("."))this.Component=h[u];else{this.Component=h;for(let f of u.split("."))this.Component=this.Component[f]}return this.hydrator=p,this.hydrate},e,this)}catch(n){console.error(\`[astro-island] Error hydrating \${this.getAttribute("component-url")}\`,n)}}attributeChangedCallback(){this.hydrate()}}d(y,"observedAttributes",["props"]),customElements.get("astro-island")||customElements.define("astro-island",y)}})();`;

var astro_island_prebuilt_dev_default = `(()=>{var A=Object.defineProperty;var g=(i,o,a)=>o in i?A(i,o,{enumerable:!0,configurable:!0,writable:!0,value:a}):i[o]=a;var l=(i,o,a)=>g(i,typeof o!="symbol"?o+"":o,a);{let i={0:t=>y(t),1:t=>a(t),2:t=>new RegExp(t),3:t=>new Date(t),4:t=>new Map(a(t)),5:t=>new Set(a(t)),6:t=>BigInt(t),7:t=>new URL(t),8:t=>new Uint8Array(t),9:t=>new Uint16Array(t),10:t=>new Uint32Array(t),11:t=>1/0*t},o=t=>{let[h,e]=t;return h in i?i[h](e):void 0},a=t=>t.map(o),y=t=>typeof t!="object"||t===null?t:Object.fromEntries(Object.entries(t).map(([h,e])=>[h,o(e)]));class f extends HTMLElement{constructor(){super(...arguments);l(this,"Component");l(this,"hydrator");l(this,"hydrate",async()=>{var b;if(!this.hydrator||!this.isConnected)return;let e=(b=this.parentElement)==null?void 0:b.closest("astro-island[ssr]");if(e){e.addEventListener("astro:hydrate",this.hydrate,{once:!0});return}let c=this.querySelectorAll("astro-slot"),n={},p=this.querySelectorAll("template[data-astro-template]");for(let r of p){let s=r.closest(this.tagName);s!=null&&s.isSameNode(this)&&(n[r.getAttribute("data-astro-template")||"default"]=r.innerHTML,r.remove())}for(let r of c){let s=r.closest(this.tagName);s!=null&&s.isSameNode(this)&&(n[r.getAttribute("name")||"default"]=r.innerHTML)}let u;try{u=this.hasAttribute("props")?y(JSON.parse(this.getAttribute("props"))):{}}catch(r){let s=this.getAttribute("component-url")||"<unknown>",v=this.getAttribute("component-export");throw v&&(s+=\` (export \${v})\`),console.error(\`[hydrate] Error parsing props for component \${s}\`,this.getAttribute("props"),r),r}let d,m=this.hydrator(this);d=performance.now(),await m(this.Component,u,n,{client:this.getAttribute("client")}),d&&this.setAttribute("client-render-time",(performance.now()-d).toString()),this.removeAttribute("ssr"),this.dispatchEvent(new CustomEvent("astro:hydrate"))});l(this,"unmount",()=>{this.isConnected||this.dispatchEvent(new CustomEvent("astro:unmount"))})}disconnectedCallback(){document.removeEventListener("astro:after-swap",this.unmount),document.addEventListener("astro:after-swap",this.unmount,{once:!0})}connectedCallback(){if(!this.hasAttribute("await-children")||document.readyState==="interactive"||document.readyState==="complete")this.childrenConnectedCallback();else{let e=()=>{document.removeEventListener("DOMContentLoaded",e),c.disconnect(),this.childrenConnectedCallback()},c=new MutationObserver(()=>{var n;((n=this.lastChild)==null?void 0:n.nodeType)===Node.COMMENT_NODE&&this.lastChild.nodeValue==="astro:end"&&(this.lastChild.remove(),e())});c.observe(this,{childList:!0}),document.addEventListener("DOMContentLoaded",e)}}async childrenConnectedCallback(){let e=this.getAttribute("before-hydration-url");e&&await import(e),this.start()}async start(){let e=JSON.parse(this.getAttribute("opts")),c=this.getAttribute("client");if(Astro[c]===void 0){window.addEventListener(\`astro:\${c}\`,()=>this.start(),{once:!0});return}try{await Astro[c](async()=>{let n=this.getAttribute("renderer-url"),[p,{default:u}]=await Promise.all([import(this.getAttribute("component-url")),n?import(n):()=>()=>{}]),d=this.getAttribute("component-export")||"default";if(!d.includes("."))this.Component=p[d];else{this.Component=p;for(let m of d.split("."))this.Component=this.Component[m]}return this.hydrator=u,this.hydrate},e,this)}catch(n){console.error(\`[astro-island] Error hydrating \${this.getAttribute("component-url")}\`,n)}}attributeChangedCallback(){this.hydrate()}}l(f,"observedAttributes",["props"]),customElements.get("astro-island")||customElements.define("astro-island",f)}})();`;

const ISLAND_STYLES = "astro-island,astro-slot,astro-static-slot{display:contents}";

function determineIfNeedsHydrationScript(result) {
  if (result._metadata.hasHydrationScript) {
    return false;
  }
  return result._metadata.hasHydrationScript = true;
}
function determinesIfNeedsDirectiveScript(result, directive) {
  if (result._metadata.hasDirectives.has(directive)) {
    return false;
  }
  result._metadata.hasDirectives.add(directive);
  return true;
}
function getDirectiveScriptText(result, directive) {
  const clientDirectives = result.clientDirectives;
  const clientDirective = clientDirectives.get(directive);
  if (!clientDirective) {
    throw new Error(`Unknown directive: ${directive}`);
  }
  return clientDirective;
}
function getPrescripts(result, type, directive) {
  switch (type) {
    case "both":
      return `<style>${ISLAND_STYLES}</style><script>${getDirectiveScriptText(result, directive)}</script><script>${process.env.NODE_ENV === "development" ? astro_island_prebuilt_dev_default : astro_island_prebuilt_default}</script>`;
    case "directive":
      return `<script>${getDirectiveScriptText(result, directive)}</script>`;
  }
}

function renderCspContent(result) {
  const finalScriptHashes = /* @__PURE__ */ new Set();
  const finalStyleHashes = /* @__PURE__ */ new Set();
  for (const scriptHash of result.scriptHashes) {
    finalScriptHashes.add(`'${scriptHash}'`);
  }
  for (const styleHash of result.styleHashes) {
    finalStyleHashes.add(`'${styleHash}'`);
  }
  for (const styleHash of result._metadata.extraStyleHashes) {
    finalStyleHashes.add(`'${styleHash}'`);
  }
  for (const scriptHash of result._metadata.extraScriptHashes) {
    finalScriptHashes.add(`'${scriptHash}'`);
  }
  let directives;
  if (result.directives.length > 0) {
    directives = result.directives.join(";") + ";";
  }
  let scriptResources = "'self'";
  if (result.scriptResources.length > 0) {
    scriptResources = result.scriptResources.map((r) => `${r}`).join(" ");
  }
  let styleResources = "'self'";
  if (result.styleResources.length > 0) {
    styleResources = result.styleResources.map((r) => `${r}`).join(" ");
  }
  const strictDynamic = result.isStrictDynamic ? ` 'strict-dynamic'` : "";
  const scriptSrc = `script-src ${scriptResources} ${Array.from(finalScriptHashes).join(" ")}${strictDynamic};`;
  const styleSrc = `style-src ${styleResources} ${Array.from(finalStyleHashes).join(" ")};`;
  return [directives, scriptSrc, styleSrc].filter(Boolean).join(" ");
}

const RenderInstructionSymbol = Symbol.for("astro:render");
function createRenderInstruction(instruction) {
  return Object.defineProperty(instruction, RenderInstructionSymbol, {
    value: true
  });
}
function isRenderInstruction(chunk) {
  return chunk && typeof chunk === "object" && chunk[RenderInstructionSymbol];
}

const voidElementNames = /^(area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|source|track|wbr)$/i;
const htmlBooleanAttributes = /^(?:allowfullscreen|async|autofocus|autoplay|checked|controls|default|defer|disabled|disablepictureinpicture|disableremoteplayback|formnovalidate|hidden|inert|loop|muted|nomodule|novalidate|open|playsinline|readonly|required|reversed|scoped|seamless|selected|itemscope)$/i;
const AMPERSAND_REGEX = /&/g;
const DOUBLE_QUOTE_REGEX = /"/g;
const STATIC_DIRECTIVES = /* @__PURE__ */ new Set(["set:html", "set:text"]);
const toIdent = (k) => k.trim().replace(/(?!^)\b\w|\s+|\W+/g, (match, index) => {
  if (/\W/.test(match)) return "";
  return index === 0 ? match : match.toUpperCase();
});
const toAttributeString = (value, shouldEscape = true) => shouldEscape ? String(value).replace(AMPERSAND_REGEX, "&#38;").replace(DOUBLE_QUOTE_REGEX, "&#34;") : value;
const kebab = (k) => k.toLowerCase() === k ? k : k.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`);
const toStyleString = (obj) => Object.entries(obj).filter(([_, v]) => typeof v === "string" && v.trim() || typeof v === "number").map(([k, v]) => {
  if (k[0] !== "-" && k[1] !== "-") return `${kebab(k)}:${v}`;
  return `${k}:${v}`;
}).join(";");
function defineScriptVars(vars) {
  let output = "";
  for (const [key, value] of Object.entries(vars)) {
    output += `const ${toIdent(key)} = ${JSON.stringify(value)?.replace(
      /<\/script>/g,
      "\\x3C/script>"
    )};
`;
  }
  return markHTMLString(output);
}
function formatList(values) {
  if (values.length === 1) {
    return values[0];
  }
  return `${values.slice(0, -1).join(", ")} or ${values[values.length - 1]}`;
}
function isCustomElement(tagName) {
  return tagName.includes("-");
}
function handleBooleanAttribute(key, value, shouldEscape, tagName) {
  if (tagName && isCustomElement(tagName)) {
    return markHTMLString(` ${key}="${toAttributeString(value, shouldEscape)}"`);
  }
  return markHTMLString(value ? ` ${key}` : "");
}
function addAttribute(value, key, shouldEscape = true, tagName = "") {
  if (value == null) {
    return "";
  }
  if (STATIC_DIRECTIVES.has(key)) {
    console.warn(`[astro] The "${key}" directive cannot be applied dynamically at runtime. It will not be rendered as an attribute.

Make sure to use the static attribute syntax (\`${key}={value}\`) instead of the dynamic spread syntax (\`{...{ "${key}": value }}\`).`);
    return "";
  }
  if (key === "class:list") {
    const listValue = toAttributeString(clsx(value), shouldEscape);
    if (listValue === "") {
      return "";
    }
    return markHTMLString(` ${key.slice(0, -5)}="${listValue}"`);
  }
  if (key === "style" && !(value instanceof HTMLString)) {
    if (Array.isArray(value) && value.length === 2) {
      return markHTMLString(
        ` ${key}="${toAttributeString(`${toStyleString(value[0])};${value[1]}`, shouldEscape)}"`
      );
    }
    if (typeof value === "object") {
      return markHTMLString(` ${key}="${toAttributeString(toStyleString(value), shouldEscape)}"`);
    }
  }
  if (key === "className") {
    return markHTMLString(` class="${toAttributeString(value, shouldEscape)}"`);
  }
  if (typeof value === "string" && value.includes("&") && isHttpUrl(value)) {
    return markHTMLString(` ${key}="${toAttributeString(value, false)}"`);
  }
  if (htmlBooleanAttributes.test(key)) {
    return handleBooleanAttribute(key, value, shouldEscape, tagName);
  }
  if (value === "") {
    return markHTMLString(` ${key}`);
  }
  if (key === "popover" && typeof value === "boolean") {
    return handleBooleanAttribute(key, value, shouldEscape, tagName);
  }
  if (key === "download" && typeof value === "boolean") {
    return handleBooleanAttribute(key, value, shouldEscape, tagName);
  }
  return markHTMLString(` ${key}="${toAttributeString(value, shouldEscape)}"`);
}
function internalSpreadAttributes(values, shouldEscape = true, tagName) {
  let output = "";
  for (const [key, value] of Object.entries(values)) {
    output += addAttribute(value, key, shouldEscape, tagName);
  }
  return markHTMLString(output);
}
function renderElement(name, { props: _props, children = "" }, shouldEscape = true) {
  const { lang: _, "data-astro-id": astroId, "define:vars": defineVars, ...props } = _props;
  if (defineVars) {
    if (name === "style") {
      delete props["is:global"];
      delete props["is:scoped"];
    }
    if (name === "script") {
      delete props.hoist;
      children = defineScriptVars(defineVars) + "\n" + children;
    }
  }
  if ((children == null || children == "") && voidElementNames.test(name)) {
    return `<${name}${internalSpreadAttributes(props, shouldEscape, name)}>`;
  }
  return `<${name}${internalSpreadAttributes(props, shouldEscape, name)}>${children}</${name}>`;
}
const noop = () => {
};
class BufferedRenderer {
  chunks = [];
  renderPromise;
  destination;
  /**
   * Determines whether buffer has been flushed
   * to the final destination.
   */
  flushed = false;
  constructor(destination, renderFunction) {
    this.destination = destination;
    this.renderPromise = renderFunction(this);
    if (isPromise(this.renderPromise)) {
      Promise.resolve(this.renderPromise).catch(noop);
    }
  }
  write(chunk) {
    if (this.flushed) {
      this.destination.write(chunk);
    } else {
      this.chunks.push(chunk);
    }
  }
  flush() {
    if (this.flushed) {
      throw new Error("The render buffer has already been flushed.");
    }
    this.flushed = true;
    for (const chunk of this.chunks) {
      this.destination.write(chunk);
    }
    return this.renderPromise;
  }
}
function createBufferedRenderer(destination, renderFunction) {
  return new BufferedRenderer(destination, renderFunction);
}
typeof process !== "undefined" && Object.prototype.toString.call(process) === "[object process]";
const VALID_PROTOCOLS = ["http:", "https:"];
function isHttpUrl(url) {
  try {
    const parsedUrl = new URL(url);
    return VALID_PROTOCOLS.includes(parsedUrl.protocol);
  } catch {
    return false;
  }
}

const uniqueElements = (item, index, all) => {
  const props = JSON.stringify(item.props);
  const children = item.children;
  return index === all.findIndex((i) => JSON.stringify(i.props) === props && i.children == children);
};
function renderAllHeadContent(result) {
  result._metadata.hasRenderedHead = true;
  let content = "";
  if (result.shouldInjectCspMetaTags && result.cspDestination === "meta") {
    content += renderElement(
      "meta",
      {
        props: {
          "http-equiv": "content-security-policy",
          content: renderCspContent(result)
        },
        children: ""
      },
      false
    );
  }
  const styles = Array.from(result.styles).filter(uniqueElements).map(
    (style) => style.props.rel === "stylesheet" ? renderElement("link", style) : renderElement("style", style)
  );
  result.styles.clear();
  const scripts = Array.from(result.scripts).filter(uniqueElements).map((script) => {
    if (result.userAssetsBase) {
      script.props.src = (result.base === "/" ? "" : result.base) + result.userAssetsBase + script.props.src;
    }
    return renderElement("script", script, false);
  });
  const links = Array.from(result.links).filter(uniqueElements).map((link) => renderElement("link", link, false));
  content += styles.join("\n") + links.join("\n") + scripts.join("\n");
  if (result._metadata.extraHead.length > 0) {
    for (const part of result._metadata.extraHead) {
      content += part;
    }
  }
  return markHTMLString(content);
}
function renderHead() {
  return createRenderInstruction({ type: "head" });
}
function maybeRenderHead() {
  return createRenderInstruction({ type: "maybe-head" });
}

const ALGORITHMS = {
  "SHA-256": "sha256-",
  "SHA-384": "sha384-",
  "SHA-512": "sha512-"
};
const ALGORITHM_VALUES = Object.values(ALGORITHMS);
z.enum(Object.keys(ALGORITHMS)).optional().default("SHA-256");
z.custom((value) => {
  if (typeof value !== "string") {
    return false;
  }
  return ALGORITHM_VALUES.some((allowedValue) => {
    return value.startsWith(allowedValue);
  });
});
const ALLOWED_DIRECTIVES = [
  "base-uri",
  "child-src",
  "connect-src",
  "default-src",
  "fenced-frame-src",
  "font-src",
  "form-action",
  "frame-ancestors",
  "frame-src",
  "img-src",
  "manifest-src",
  "media-src",
  "object-src",
  "referrer",
  "report-to",
  "report-uri",
  "require-trusted-types-for",
  "sandbox",
  "trusted-types",
  "upgrade-insecure-requests",
  "worker-src"
];
z.custom((value) => {
  if (typeof value !== "string") {
    return false;
  }
  return ALLOWED_DIRECTIVES.some((allowedValue) => {
    return value.startsWith(allowedValue);
  });
});

const ALGORITHM = "AES-GCM";
async function decodeKey(encoded) {
  const bytes = decodeBase64(encoded);
  return crypto.subtle.importKey("raw", bytes.buffer, ALGORITHM, true, [
    "encrypt",
    "decrypt"
  ]);
}
const encoder = new TextEncoder();
new TextDecoder();
const IV_LENGTH = 24;
async function encryptString(key, raw) {
  const iv = crypto.getRandomValues(new Uint8Array(IV_LENGTH / 2));
  const data = encoder.encode(raw);
  const buffer = await crypto.subtle.encrypt(
    {
      name: ALGORITHM,
      iv
    },
    key,
    data
  );
  return encodeHexUpperCase(iv) + encodeBase64(new Uint8Array(buffer));
}
async function generateCspDigest(data, algorithm) {
  const hashBuffer = await crypto.subtle.digest(algorithm, encoder.encode(data));
  const hash = encodeBase64(new Uint8Array(hashBuffer));
  return `${ALGORITHMS[algorithm]}${hash}`;
}

const renderTemplateResultSym = Symbol.for("astro.renderTemplateResult");
class RenderTemplateResult {
  [renderTemplateResultSym] = true;
  htmlParts;
  expressions;
  error;
  constructor(htmlParts, expressions) {
    this.htmlParts = htmlParts;
    this.error = void 0;
    this.expressions = expressions.map((expression) => {
      if (isPromise(expression)) {
        return Promise.resolve(expression).catch((err) => {
          if (!this.error) {
            this.error = err;
            throw err;
          }
        });
      }
      return expression;
    });
  }
  render(destination) {
    const flushers = this.expressions.map((exp) => {
      return createBufferedRenderer(destination, (bufferDestination) => {
        if (exp || exp === 0) {
          return renderChild(bufferDestination, exp);
        }
      });
    });
    let i = 0;
    const iterate = () => {
      while (i < this.htmlParts.length) {
        const html = this.htmlParts[i];
        const flusher = flushers[i];
        i++;
        if (html) {
          destination.write(markHTMLString(html));
        }
        if (flusher) {
          const result = flusher.flush();
          if (isPromise(result)) {
            return result.then(iterate);
          }
        }
      }
    };
    return iterate();
  }
}
function isRenderTemplateResult(obj) {
  return typeof obj === "object" && obj !== null && !!obj[renderTemplateResultSym];
}
function renderTemplate(htmlParts, ...expressions) {
  return new RenderTemplateResult(htmlParts, expressions);
}

const slotString = Symbol.for("astro:slot-string");
class SlotString extends HTMLString {
  instructions;
  [slotString];
  constructor(content, instructions) {
    super(content);
    this.instructions = instructions;
    this[slotString] = true;
  }
}
function isSlotString(str) {
  return !!str[slotString];
}
function mergeSlotInstructions(target, source) {
  if (source.instructions?.length) {
    target ??= [];
    target.push(...source.instructions);
  }
  return target;
}
function renderSlot(result, slotted, fallback) {
  if (!slotted && fallback) {
    return renderSlot(result, fallback);
  }
  return {
    async render(destination) {
      await renderChild(destination, typeof slotted === "function" ? slotted(result) : slotted);
    }
  };
}
async function renderSlotToString(result, slotted, fallback) {
  let content = "";
  let instructions = null;
  const temporaryDestination = {
    write(chunk) {
      if (chunk instanceof SlotString) {
        content += chunk;
        instructions = mergeSlotInstructions(instructions, chunk);
      } else if (chunk instanceof Response) return;
      else if (typeof chunk === "object" && "type" in chunk && typeof chunk.type === "string") {
        if (instructions === null) {
          instructions = [];
        }
        instructions.push(chunk);
      } else {
        content += chunkToString(result, chunk);
      }
    }
  };
  const renderInstance = renderSlot(result, slotted, fallback);
  await renderInstance.render(temporaryDestination);
  return markHTMLString(new SlotString(content, instructions));
}
async function renderSlots(result, slots = {}) {
  let slotInstructions = null;
  let children = {};
  if (slots) {
    await Promise.all(
      Object.entries(slots).map(
        ([key, value]) => renderSlotToString(result, value).then((output) => {
          if (output.instructions) {
            if (slotInstructions === null) {
              slotInstructions = [];
            }
            slotInstructions.push(...output.instructions);
          }
          children[key] = output;
        })
      )
    );
  }
  return { slotInstructions, children };
}

const internalProps = /* @__PURE__ */ new Set([
  "server:component-path",
  "server:component-export",
  "server:component-directive",
  "server:defer"
]);
function containsServerDirective(props) {
  return "server:component-directive" in props;
}
const SCRIPT_RE = /<\/script/giu;
const COMMENT_RE = /<!--/gu;
const SCRIPT_REPLACER = "<\\/script";
const COMMENT_REPLACER = "\\u003C!--";
function safeJsonStringify(obj) {
  return JSON.stringify(obj).replace(SCRIPT_RE, SCRIPT_REPLACER).replace(COMMENT_RE, COMMENT_REPLACER);
}
function createSearchParams(encryptedComponentExport, encryptedProps, slots) {
  const params = new URLSearchParams();
  params.set("e", encryptedComponentExport);
  params.set("p", encryptedProps);
  params.set("s", slots);
  return params;
}
function isWithinURLLimit(pathname, params) {
  const url = pathname + "?" + params.toString();
  const chars = url.length;
  return chars < 2048;
}
class ServerIslandComponent {
  result;
  props;
  slots;
  displayName;
  hostId;
  islandContent;
  componentPath;
  componentExport;
  componentId;
  constructor(result, props, slots, displayName) {
    this.result = result;
    this.props = props;
    this.slots = slots;
    this.displayName = displayName;
  }
  async init() {
    const content = await this.getIslandContent();
    if (this.result.cspDestination) {
      this.result._metadata.extraScriptHashes.push(
        await generateCspDigest(SERVER_ISLAND_REPLACER, this.result.cspAlgorithm)
      );
      const contentDigest = await generateCspDigest(content, this.result.cspAlgorithm);
      this.result._metadata.extraScriptHashes.push(contentDigest);
    }
    return createThinHead();
  }
  async render(destination) {
    const hostId = await this.getHostId();
    const islandContent = await this.getIslandContent();
    destination.write(createRenderInstruction({ type: "server-island-runtime" }));
    destination.write("<!--[if astro]>server-island-start<![endif]-->");
    for (const name in this.slots) {
      if (name === "fallback") {
        await renderChild(destination, this.slots.fallback(this.result));
      }
    }
    destination.write(
      `<script type="module" data-astro-rerun data-island-id="${hostId}">${islandContent}</script>`
    );
  }
  getComponentPath() {
    if (this.componentPath) {
      return this.componentPath;
    }
    const componentPath = this.props["server:component-path"];
    if (!componentPath) {
      throw new Error(`Could not find server component path`);
    }
    this.componentPath = componentPath;
    return componentPath;
  }
  getComponentExport() {
    if (this.componentExport) {
      return this.componentExport;
    }
    const componentExport = this.props["server:component-export"];
    if (!componentExport) {
      throw new Error(`Could not find server component export`);
    }
    this.componentExport = componentExport;
    return componentExport;
  }
  async getHostId() {
    if (!this.hostId) {
      this.hostId = await crypto.randomUUID();
    }
    return this.hostId;
  }
  async getIslandContent() {
    if (this.islandContent) {
      return this.islandContent;
    }
    const componentPath = this.getComponentPath();
    const componentExport = this.getComponentExport();
    const componentId = this.result.serverIslandNameMap.get(componentPath);
    if (!componentId) {
      throw new Error(`Could not find server component name`);
    }
    for (const key2 of Object.keys(this.props)) {
      if (internalProps.has(key2)) {
        delete this.props[key2];
      }
    }
    const renderedSlots = {};
    for (const name in this.slots) {
      if (name !== "fallback") {
        const content = await renderSlotToString(this.result, this.slots[name]);
        renderedSlots[name] = content.toString();
      }
    }
    const key = await this.result.key;
    const componentExportEncrypted = await encryptString(key, componentExport);
    const propsEncrypted = Object.keys(this.props).length === 0 ? "" : await encryptString(key, JSON.stringify(this.props));
    const slotsEncrypted = Object.keys(renderedSlots).length === 0 ? "" : await encryptString(key, JSON.stringify(renderedSlots));
    const hostId = await this.getHostId();
    const slash = this.result.base.endsWith("/") ? "" : "/";
    let serverIslandUrl = `${this.result.base}${slash}_server-islands/${componentId}${this.result.trailingSlash === "always" ? "/" : ""}`;
    const potentialSearchParams = createSearchParams(
      componentExportEncrypted,
      propsEncrypted,
      slotsEncrypted
    );
    const useGETRequest = isWithinURLLimit(serverIslandUrl, potentialSearchParams);
    if (useGETRequest) {
      serverIslandUrl += "?" + potentialSearchParams.toString();
      this.result._metadata.extraHead.push(
        markHTMLString(
          `<link rel="preload" as="fetch" href="${serverIslandUrl}" crossorigin="anonymous">`
        )
      );
    }
    const adapterHeaders = this.result.internalFetchHeaders || {};
    const headersJson = safeJsonStringify(adapterHeaders);
    const method = useGETRequest ? (
      // GET request
      `const headers = new Headers(${headersJson});
let response = await fetch('${serverIslandUrl}', { headers });`
    ) : (
      // POST request
      `let data = {
	encryptedComponentExport: ${safeJsonStringify(componentExportEncrypted)},
	encryptedProps: ${safeJsonStringify(propsEncrypted)},
	encryptedSlots: ${safeJsonStringify(slotsEncrypted)},
};
const headers = new Headers({ 'Content-Type': 'application/json', ...${headersJson} });
let response = await fetch('${serverIslandUrl}', {
	method: 'POST',
	body: JSON.stringify(data),
	headers,
});`
    );
    this.islandContent = `${method}replaceServerIsland('${hostId}', response);`;
    return this.islandContent;
  }
}
const renderServerIslandRuntime = () => {
  return `<script>${SERVER_ISLAND_REPLACER}</script>`;
};
const SERVER_ISLAND_REPLACER = markHTMLString(
  `async function replaceServerIsland(id, r) {
	let s = document.querySelector(\`script[data-island-id="\${id}"]\`);
	// If there's no matching script, or the request fails then return
	if (!s || r.status !== 200 || r.headers.get('content-type')?.split(';')[0].trim() !== 'text/html') return;
	// Load the HTML before modifying the DOM in case of errors
	let html = await r.text();
	// Remove any placeholder content before the island script
	while (s.previousSibling && s.previousSibling.nodeType !== 8 && s.previousSibling.data !== '[if astro]>server-island-start<![endif]')
		s.previousSibling.remove();
	s.previousSibling?.remove();
	// Insert the new HTML
	s.before(document.createRange().createContextualFragment(html));
	// Remove the script. Prior to v5.4.2, this was the trick to force rerun of scripts.  Keeping it to minimize change to the existing behavior.
	s.remove();
}`.split("\n").map((line) => line.trim()).filter((line) => line && !line.startsWith("//")).join(" ")
);

const Fragment = Symbol.for("astro:fragment");
const Renderer = Symbol.for("astro:renderer");
new TextEncoder();
const decoder = new TextDecoder();
function stringifyChunk(result, chunk) {
  if (isRenderInstruction(chunk)) {
    const instruction = chunk;
    switch (instruction.type) {
      case "directive": {
        const { hydration } = instruction;
        let needsHydrationScript = hydration && determineIfNeedsHydrationScript(result);
        let needsDirectiveScript = hydration && determinesIfNeedsDirectiveScript(result, hydration.directive);
        if (needsHydrationScript) {
          let prescripts = getPrescripts(result, "both", hydration.directive);
          return markHTMLString(prescripts);
        } else if (needsDirectiveScript) {
          let prescripts = getPrescripts(result, "directive", hydration.directive);
          return markHTMLString(prescripts);
        } else {
          return "";
        }
      }
      case "head": {
        if (result._metadata.hasRenderedHead || result.partial) {
          return "";
        }
        return renderAllHeadContent(result);
      }
      case "maybe-head": {
        if (result._metadata.hasRenderedHead || result._metadata.headInTree || result.partial) {
          return "";
        }
        return renderAllHeadContent(result);
      }
      case "renderer-hydration-script": {
        const { rendererSpecificHydrationScripts } = result._metadata;
        const { rendererName } = instruction;
        if (!rendererSpecificHydrationScripts.has(rendererName)) {
          rendererSpecificHydrationScripts.add(rendererName);
          return instruction.render();
        }
        return "";
      }
      case "server-island-runtime": {
        if (result._metadata.hasRenderedServerIslandRuntime) {
          return "";
        }
        result._metadata.hasRenderedServerIslandRuntime = true;
        return renderServerIslandRuntime();
      }
      case "script": {
        const { id, content } = instruction;
        if (result._metadata.renderedScripts.has(id)) {
          return "";
        }
        result._metadata.renderedScripts.add(id);
        return content;
      }
      default: {
        throw new Error(`Unknown chunk type: ${chunk.type}`);
      }
    }
  } else if (chunk instanceof Response) {
    return "";
  } else if (isSlotString(chunk)) {
    let out = "";
    const c = chunk;
    if (c.instructions) {
      for (const instr of c.instructions) {
        out += stringifyChunk(result, instr);
      }
    }
    out += chunk.toString();
    return out;
  }
  return chunk.toString();
}
function chunkToString(result, chunk) {
  if (ArrayBuffer.isView(chunk)) {
    return decoder.decode(chunk);
  } else {
    return stringifyChunk(result, chunk);
  }
}
function isRenderInstance(obj) {
  return !!obj && typeof obj === "object" && "render" in obj && typeof obj.render === "function";
}

function renderChild(destination, child) {
  if (isPromise(child)) {
    return child.then((x) => renderChild(destination, x));
  }
  if (child instanceof SlotString) {
    destination.write(child);
    return;
  }
  if (isHTMLString(child)) {
    destination.write(child);
    return;
  }
  if (Array.isArray(child)) {
    return renderArray(destination, child);
  }
  if (typeof child === "function") {
    return renderChild(destination, child());
  }
  if (!child && child !== 0) {
    return;
  }
  if (typeof child === "string") {
    destination.write(markHTMLString(escapeHTML(child)));
    return;
  }
  if (isRenderInstance(child)) {
    return child.render(destination);
  }
  if (isRenderTemplateResult(child)) {
    return child.render(destination);
  }
  if (isAstroComponentInstance(child)) {
    return child.render(destination);
  }
  if (ArrayBuffer.isView(child)) {
    destination.write(child);
    return;
  }
  if (typeof child === "object" && (Symbol.asyncIterator in child || Symbol.iterator in child)) {
    if (Symbol.asyncIterator in child) {
      return renderAsyncIterable(destination, child);
    }
    return renderIterable(destination, child);
  }
  destination.write(child);
}
function renderArray(destination, children) {
  const flushers = children.map((c) => {
    return createBufferedRenderer(destination, (bufferDestination) => {
      return renderChild(bufferDestination, c);
    });
  });
  const iterator = flushers[Symbol.iterator]();
  const iterate = () => {
    for (; ; ) {
      const { value: flusher, done } = iterator.next();
      if (done) {
        break;
      }
      const result = flusher.flush();
      if (isPromise(result)) {
        return result.then(iterate);
      }
    }
  };
  return iterate();
}
function renderIterable(destination, children) {
  const iterator = children[Symbol.iterator]();
  const iterate = () => {
    for (; ; ) {
      const { value, done } = iterator.next();
      if (done) {
        break;
      }
      const result = renderChild(destination, value);
      if (isPromise(result)) {
        return result.then(iterate);
      }
    }
  };
  return iterate();
}
async function renderAsyncIterable(destination, children) {
  for await (const value of children) {
    await renderChild(destination, value);
  }
}

const astroComponentInstanceSym = Symbol.for("astro.componentInstance");
class AstroComponentInstance {
  [astroComponentInstanceSym] = true;
  result;
  props;
  slotValues;
  factory;
  returnValue;
  constructor(result, props, slots, factory) {
    this.result = result;
    this.props = props;
    this.factory = factory;
    this.slotValues = {};
    for (const name in slots) {
      let didRender = false;
      let value = slots[name](result);
      this.slotValues[name] = () => {
        if (!didRender) {
          didRender = true;
          return value;
        }
        return slots[name](result);
      };
    }
  }
  init(result) {
    if (this.returnValue !== void 0) {
      return this.returnValue;
    }
    this.returnValue = this.factory(result, this.props, this.slotValues);
    if (isPromise(this.returnValue)) {
      this.returnValue.then((resolved) => {
        this.returnValue = resolved;
      }).catch(() => {
      });
    }
    return this.returnValue;
  }
  render(destination) {
    const returnValue = this.init(this.result);
    if (isPromise(returnValue)) {
      return returnValue.then((x) => this.renderImpl(destination, x));
    }
    return this.renderImpl(destination, returnValue);
  }
  renderImpl(destination, returnValue) {
    if (isHeadAndContent(returnValue)) {
      return returnValue.content.render(destination);
    } else {
      return renderChild(destination, returnValue);
    }
  }
}
function validateComponentProps(props, clientDirectives, displayName) {
  if (props != null) {
    const directives = [...clientDirectives.keys()].map((directive) => `client:${directive}`);
    for (const prop of Object.keys(props)) {
      if (directives.includes(prop)) {
        console.warn(
          `You are attempting to render <${displayName} ${prop} />, but ${displayName} is an Astro component. Astro components do not render in the client and should not have a hydration directive. Please use a framework component for client rendering.`
        );
      }
    }
  }
}
function createAstroComponentInstance(result, displayName, factory, props, slots = {}) {
  validateComponentProps(props, result.clientDirectives, displayName);
  const instance = new AstroComponentInstance(result, props, slots, factory);
  if (isAPropagatingComponent(result, factory)) {
    result._metadata.propagators.add(instance);
  }
  return instance;
}
function isAstroComponentInstance(obj) {
  return typeof obj === "object" && obj !== null && !!obj[astroComponentInstanceSym];
}

function componentIsHTMLElement(Component) {
  return typeof HTMLElement !== "undefined" && HTMLElement.isPrototypeOf(Component);
}
async function renderHTMLElement(result, constructor, props, slots) {
  const name = getHTMLElementName(constructor);
  let attrHTML = "";
  for (const attr in props) {
    attrHTML += ` ${attr}="${toAttributeString(await props[attr])}"`;
  }
  return markHTMLString(
    `<${name}${attrHTML}>${await renderSlotToString(result, slots?.default)}</${name}>`
  );
}
function getHTMLElementName(constructor) {
  const definedName = customElements.getName(constructor);
  if (definedName) return definedName;
  const assignedName = constructor.name.replace(/^HTML|Element$/g, "").replace(/[A-Z]/g, "-$&").toLowerCase().replace(/^-/, "html-");
  return assignedName;
}

const rendererAliases = /* @__PURE__ */ new Map([["solid", "solid-js"]]);
const clientOnlyValues = /* @__PURE__ */ new Set(["solid-js", "react", "preact", "vue", "svelte"]);
function guessRenderers(componentUrl) {
  const extname = componentUrl?.split(".").pop();
  switch (extname) {
    case "svelte":
      return ["@astrojs/svelte"];
    case "vue":
      return ["@astrojs/vue"];
    case "jsx":
    case "tsx":
      return ["@astrojs/react", "@astrojs/preact", "@astrojs/solid-js", "@astrojs/vue (jsx)"];
    case void 0:
    default:
      return [
        "@astrojs/react",
        "@astrojs/preact",
        "@astrojs/solid-js",
        "@astrojs/vue",
        "@astrojs/svelte"
      ];
  }
}
function isFragmentComponent(Component) {
  return Component === Fragment;
}
function isHTMLComponent(Component) {
  return Component && Component["astro:html"] === true;
}
const ASTRO_SLOT_EXP = /<\/?astro-slot\b[^>]*>/g;
const ASTRO_STATIC_SLOT_EXP = /<\/?astro-static-slot\b[^>]*>/g;
function removeStaticAstroSlot(html, supportsAstroStaticSlot = true) {
  const exp = supportsAstroStaticSlot ? ASTRO_STATIC_SLOT_EXP : ASTRO_SLOT_EXP;
  return html.replace(exp, "");
}
async function renderFrameworkComponent(result, displayName, Component, _props, slots = {}) {
  if (!Component && "client:only" in _props === false) {
    throw new Error(
      `Unable to render ${displayName} because it is ${Component}!
Did you forget to import the component or is it possible there is a typo?`
    );
  }
  const { renderers, clientDirectives } = result;
  const metadata = {
    astroStaticSlot: true,
    displayName
  };
  const { hydration, isPage, props, propsWithoutTransitionAttributes } = extractDirectives(
    _props,
    clientDirectives
  );
  let html = "";
  let attrs = void 0;
  if (hydration) {
    metadata.hydrate = hydration.directive;
    metadata.hydrateArgs = hydration.value;
    metadata.componentExport = hydration.componentExport;
    metadata.componentUrl = hydration.componentUrl;
  }
  const probableRendererNames = guessRenderers(metadata.componentUrl);
  const validRenderers = renderers.filter((r) => r.name !== "astro:jsx");
  const { children, slotInstructions } = await renderSlots(result, slots);
  let renderer;
  if (metadata.hydrate !== "only") {
    let isTagged = false;
    try {
      isTagged = Component && Component[Renderer];
    } catch {
    }
    if (isTagged) {
      const rendererName = Component[Renderer];
      renderer = renderers.find(({ name }) => name === rendererName);
    }
    if (!renderer) {
      let error;
      for (const r of renderers) {
        try {
          if (await r.ssr.check.call({ result }, Component, props, children)) {
            renderer = r;
            break;
          }
        } catch (e) {
          error ??= e;
        }
      }
      if (!renderer && error) {
        throw error;
      }
    }
    if (!renderer && typeof HTMLElement === "function" && componentIsHTMLElement(Component)) {
      const output = await renderHTMLElement(
        result,
        Component,
        _props,
        slots
      );
      return {
        render(destination) {
          destination.write(output);
        }
      };
    }
  } else {
    if (metadata.hydrateArgs) {
      const rendererName = rendererAliases.has(metadata.hydrateArgs) ? rendererAliases.get(metadata.hydrateArgs) : metadata.hydrateArgs;
      if (clientOnlyValues.has(rendererName)) {
        renderer = renderers.find(
          ({ name }) => name === `@astrojs/${rendererName}` || name === rendererName
        );
      }
    }
    if (!renderer && validRenderers.length === 1) {
      renderer = validRenderers[0];
    }
    if (!renderer) {
      const extname = metadata.componentUrl?.split(".").pop();
      renderer = renderers.find(({ name }) => name === `@astrojs/${extname}` || name === extname);
    }
  }
  let componentServerRenderEndTime;
  if (!renderer) {
    if (metadata.hydrate === "only") {
      const rendererName = rendererAliases.has(metadata.hydrateArgs) ? rendererAliases.get(metadata.hydrateArgs) : metadata.hydrateArgs;
      if (clientOnlyValues.has(rendererName)) {
        const plural = validRenderers.length > 1;
        throw new AstroError({
          ...NoMatchingRenderer,
          message: NoMatchingRenderer.message(
            metadata.displayName,
            metadata?.componentUrl?.split(".").pop(),
            plural,
            validRenderers.length
          ),
          hint: NoMatchingRenderer.hint(
            formatList(probableRendererNames.map((r) => "`" + r + "`"))
          )
        });
      } else {
        throw new AstroError({
          ...NoClientOnlyHint,
          message: NoClientOnlyHint.message(metadata.displayName),
          hint: NoClientOnlyHint.hint(
            probableRendererNames.map((r) => r.replace("@astrojs/", "")).join("|")
          )
        });
      }
    } else if (typeof Component !== "string") {
      const matchingRenderers = validRenderers.filter(
        (r) => probableRendererNames.includes(r.name)
      );
      const plural = validRenderers.length > 1;
      if (matchingRenderers.length === 0) {
        throw new AstroError({
          ...NoMatchingRenderer,
          message: NoMatchingRenderer.message(
            metadata.displayName,
            metadata?.componentUrl?.split(".").pop(),
            plural,
            validRenderers.length
          ),
          hint: NoMatchingRenderer.hint(
            formatList(probableRendererNames.map((r) => "`" + r + "`"))
          )
        });
      } else if (matchingRenderers.length === 1) {
        renderer = matchingRenderers[0];
        ({ html, attrs } = await renderer.ssr.renderToStaticMarkup.call(
          { result },
          Component,
          propsWithoutTransitionAttributes,
          children,
          metadata
        ));
      } else {
        throw new Error(`Unable to render ${metadata.displayName}!

This component likely uses ${formatList(probableRendererNames)},
but Astro encountered an error during server-side rendering.

Please ensure that ${metadata.displayName}:
1. Does not unconditionally access browser-specific globals like \`window\` or \`document\`.
   If this is unavoidable, use the \`client:only\` hydration directive.
2. Does not conditionally return \`null\` or \`undefined\` when rendered on the server.

If you're still stuck, please open an issue on GitHub or join us at https://astro.build/chat.`);
      }
    }
  } else {
    if (metadata.hydrate === "only") {
      html = await renderSlotToString(result, slots?.fallback);
    } else {
      const componentRenderStartTime = performance.now();
      ({ html, attrs } = await renderer.ssr.renderToStaticMarkup.call(
        { result },
        Component,
        propsWithoutTransitionAttributes,
        children,
        metadata
      ));
      if (process.env.NODE_ENV === "development")
        componentServerRenderEndTime = performance.now() - componentRenderStartTime;
    }
  }
  if (!html && typeof Component === "string") {
    const Tag = sanitizeElementName(Component);
    const childSlots = Object.values(children).join("");
    const renderTemplateResult = renderTemplate`<${Tag}${internalSpreadAttributes(
      props,
      true,
      Tag
    )}${markHTMLString(
      childSlots === "" && voidElementNames.test(Tag) ? `/>` : `>${childSlots}</${Tag}>`
    )}`;
    html = "";
    const destination = {
      write(chunk) {
        if (chunk instanceof Response) return;
        html += chunkToString(result, chunk);
      }
    };
    await renderTemplateResult.render(destination);
  }
  if (!hydration) {
    return {
      render(destination) {
        if (slotInstructions) {
          for (const instruction of slotInstructions) {
            destination.write(instruction);
          }
        }
        if (isPage || renderer?.name === "astro:jsx") {
          destination.write(html);
        } else if (html && html.length > 0) {
          destination.write(
            markHTMLString(removeStaticAstroSlot(html, renderer?.ssr?.supportsAstroStaticSlot))
          );
        }
      }
    };
  }
  const astroId = shorthash(
    `<!--${metadata.componentExport.value}:${metadata.componentUrl}-->
${html}
${serializeProps(
      props,
      metadata
    )}`
  );
  const island = await generateHydrateScript(
    { renderer, result, astroId, props, attrs },
    metadata
  );
  if (componentServerRenderEndTime && process.env.NODE_ENV === "development")
    island.props["server-render-time"] = componentServerRenderEndTime;
  let unrenderedSlots = [];
  if (html) {
    if (Object.keys(children).length > 0) {
      for (const key of Object.keys(children)) {
        let tagName = renderer?.ssr?.supportsAstroStaticSlot ? !!metadata.hydrate ? "astro-slot" : "astro-static-slot" : "astro-slot";
        let expectedHTML = key === "default" ? `<${tagName}>` : `<${tagName} name="${key}">`;
        if (!html.includes(expectedHTML)) {
          unrenderedSlots.push(key);
        }
      }
    }
  } else {
    unrenderedSlots = Object.keys(children);
  }
  const template = unrenderedSlots.length > 0 ? unrenderedSlots.map(
    (key) => `<template data-astro-template${key !== "default" ? `="${key}"` : ""}>${children[key]}</template>`
  ).join("") : "";
  island.children = `${html ?? ""}${template}`;
  if (island.children) {
    island.props["await-children"] = "";
    island.children += `<!--astro:end-->`;
  }
  return {
    render(destination) {
      if (slotInstructions) {
        for (const instruction of slotInstructions) {
          destination.write(instruction);
        }
      }
      destination.write(createRenderInstruction({ type: "directive", hydration }));
      if (hydration.directive !== "only" && renderer?.ssr.renderHydrationScript) {
        destination.write(
          createRenderInstruction({
            type: "renderer-hydration-script",
            rendererName: renderer.name,
            render: renderer.ssr.renderHydrationScript
          })
        );
      }
      const renderedElement = renderElement("astro-island", island, false);
      destination.write(markHTMLString(renderedElement));
    }
  };
}
function sanitizeElementName(tag) {
  const unsafe = /[&<>'"\s]+/;
  if (!unsafe.test(tag)) return tag;
  return tag.trim().split(unsafe)[0].trim();
}
async function renderFragmentComponent(result, slots = {}) {
  const children = await renderSlotToString(result, slots?.default);
  return {
    render(destination) {
      if (children == null) return;
      destination.write(children);
    }
  };
}
async function renderHTMLComponent(result, Component, _props, slots = {}) {
  const { slotInstructions, children } = await renderSlots(result, slots);
  const html = Component({ slots: children });
  const hydrationHtml = slotInstructions ? slotInstructions.map((instr) => chunkToString(result, instr)).join("") : "";
  return {
    render(destination) {
      destination.write(markHTMLString(hydrationHtml + html));
    }
  };
}
function renderAstroComponent(result, displayName, Component, props, slots = {}) {
  if (containsServerDirective(props)) {
    const serverIslandComponent = new ServerIslandComponent(result, props, slots, displayName);
    result._metadata.propagators.add(serverIslandComponent);
    return serverIslandComponent;
  }
  const instance = createAstroComponentInstance(result, displayName, Component, props, slots);
  return {
    render(destination) {
      return instance.render(destination);
    }
  };
}
function renderComponent(result, displayName, Component, props, slots = {}) {
  if (isPromise(Component)) {
    return Component.catch(handleCancellation).then((x) => {
      return renderComponent(result, displayName, x, props, slots);
    });
  }
  if (isFragmentComponent(Component)) {
    return renderFragmentComponent(result, slots).catch(handleCancellation);
  }
  props = normalizeProps(props);
  if (isHTMLComponent(Component)) {
    return renderHTMLComponent(result, Component, props, slots).catch(handleCancellation);
  }
  if (isAstroComponentFactory(Component)) {
    return renderAstroComponent(result, displayName, Component, props, slots);
  }
  return renderFrameworkComponent(result, displayName, Component, props, slots).catch(
    handleCancellation
  );
  function handleCancellation(e) {
    if (result.cancelled)
      return {
        render() {
        }
      };
    throw e;
  }
}
function normalizeProps(props) {
  if (props["class:list"] !== void 0) {
    const value = props["class:list"];
    delete props["class:list"];
    props["class"] = clsx(props["class"], value);
    if (props["class"] === "") {
      delete props["class"];
    }
  }
  return props;
}

"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_".split("").reduce((v, c) => (v[c.charCodeAt(0)] = c, v), []);
"-0123456789_".split("").reduce((v, c) => (v[c.charCodeAt(0)] = c, v), []);

function spreadAttributes(values = {}, _name, { class: scopedClassName } = {}) {
  let output = "";
  if (scopedClassName) {
    if (typeof values.class !== "undefined") {
      values.class += ` ${scopedClassName}`;
    } else if (typeof values["class:list"] !== "undefined") {
      values["class:list"] = [values["class:list"], scopedClassName];
    } else {
      values.class = scopedClassName;
    }
  }
  for (const [key, value] of Object.entries(values)) {
    output += addAttribute(value, key, true, _name);
  }
  return markHTMLString(output);
}

export { NOOP_MIDDLEWARE_HEADER as N, createComponent as a, renderTemplate as b, createAstro as c, addAttribute as d, renderHead as e, renderSlot as f, decodeKey as g, maybeRenderHead as m, renderComponent as r, spreadAttributes as s, unescapeHTML as u };
