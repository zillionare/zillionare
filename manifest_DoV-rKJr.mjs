import '@astrojs/internal-helpers/path';
import '@astrojs/internal-helpers/remote';
import 'piccolore';
import { N as NOOP_MIDDLEWARE_HEADER, g as decodeKey } from './chunks/astro/server_CTn7mrR8.mjs';
import 'clsx';
import 'es-module-lexer';
import 'html-escaper';

const NOOP_MIDDLEWARE_FN = async (_ctx, next) => {
  const response = await next();
  response.headers.set(NOOP_MIDDLEWARE_HEADER, "true");
  return response;
};

const codeToStatusMap = {
  // Implemented from IANA HTTP Status Code Registry
  // https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  PAYMENT_REQUIRED: 402,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  METHOD_NOT_ALLOWED: 405,
  NOT_ACCEPTABLE: 406,
  PROXY_AUTHENTICATION_REQUIRED: 407,
  REQUEST_TIMEOUT: 408,
  CONFLICT: 409,
  GONE: 410,
  LENGTH_REQUIRED: 411,
  PRECONDITION_FAILED: 412,
  CONTENT_TOO_LARGE: 413,
  URI_TOO_LONG: 414,
  UNSUPPORTED_MEDIA_TYPE: 415,
  RANGE_NOT_SATISFIABLE: 416,
  EXPECTATION_FAILED: 417,
  MISDIRECTED_REQUEST: 421,
  UNPROCESSABLE_CONTENT: 422,
  LOCKED: 423,
  FAILED_DEPENDENCY: 424,
  TOO_EARLY: 425,
  UPGRADE_REQUIRED: 426,
  PRECONDITION_REQUIRED: 428,
  TOO_MANY_REQUESTS: 429,
  REQUEST_HEADER_FIELDS_TOO_LARGE: 431,
  UNAVAILABLE_FOR_LEGAL_REASONS: 451,
  INTERNAL_SERVER_ERROR: 500,
  NOT_IMPLEMENTED: 501,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504,
  HTTP_VERSION_NOT_SUPPORTED: 505,
  VARIANT_ALSO_NEGOTIATES: 506,
  INSUFFICIENT_STORAGE: 507,
  LOOP_DETECTED: 508,
  NETWORK_AUTHENTICATION_REQUIRED: 511
};
Object.entries(codeToStatusMap).reduce(
  // reverse the key-value pairs
  (acc, [key, value]) => ({ ...acc, [value]: key }),
  {}
);

function sanitizeParams(params) {
  return Object.fromEntries(
    Object.entries(params).map(([key, value]) => {
      if (typeof value === "string") {
        return [key, value.normalize().replace(/#/g, "%23").replace(/\?/g, "%3F")];
      }
      return [key, value];
    })
  );
}
function getParameter(part, params) {
  if (part.spread) {
    return params[part.content.slice(3)] || "";
  }
  if (part.dynamic) {
    if (!params[part.content]) {
      throw new TypeError(`Missing parameter: ${part.content}`);
    }
    return params[part.content];
  }
  return part.content.normalize().replace(/\?/g, "%3F").replace(/#/g, "%23").replace(/%5B/g, "[").replace(/%5D/g, "]");
}
function getSegment(segment, params) {
  const segmentPath = segment.map((part) => getParameter(part, params)).join("");
  return segmentPath ? "/" + segmentPath : "";
}
function getRouteGenerator(segments, addTrailingSlash) {
  return (params) => {
    const sanitizedParams = sanitizeParams(params);
    let trailing = "";
    if (addTrailingSlash === "always" && segments.length) {
      trailing = "/";
    }
    const path = segments.map((segment) => getSegment(segment, sanitizedParams)).join("") + trailing;
    return path || "/";
  };
}

function deserializeRouteData(rawRouteData) {
  return {
    route: rawRouteData.route,
    type: rawRouteData.type,
    pattern: new RegExp(rawRouteData.pattern),
    params: rawRouteData.params,
    component: rawRouteData.component,
    generate: getRouteGenerator(rawRouteData.segments, rawRouteData._meta.trailingSlash),
    pathname: rawRouteData.pathname || void 0,
    segments: rawRouteData.segments,
    prerender: rawRouteData.prerender,
    redirect: rawRouteData.redirect,
    redirectRoute: rawRouteData.redirectRoute ? deserializeRouteData(rawRouteData.redirectRoute) : void 0,
    fallbackRoutes: rawRouteData.fallbackRoutes.map((fallback) => {
      return deserializeRouteData(fallback);
    }),
    isIndex: rawRouteData.isIndex,
    origin: rawRouteData.origin
  };
}

function deserializeManifest(serializedManifest) {
  const routes = [];
  for (const serializedRoute of serializedManifest.routes) {
    routes.push({
      ...serializedRoute,
      routeData: deserializeRouteData(serializedRoute.routeData)
    });
    const route = serializedRoute;
    route.routeData = deserializeRouteData(serializedRoute.routeData);
  }
  const assets = new Set(serializedManifest.assets);
  const componentMetadata = new Map(serializedManifest.componentMetadata);
  const inlinedScripts = new Map(serializedManifest.inlinedScripts);
  const clientDirectives = new Map(serializedManifest.clientDirectives);
  const serverIslandNameMap = new Map(serializedManifest.serverIslandNameMap);
  const key = decodeKey(serializedManifest.key);
  return {
    // in case user middleware exists, this no-op middleware will be reassigned (see plugin-ssr.ts)
    middleware() {
      return { onRequest: NOOP_MIDDLEWARE_FN };
    },
    ...serializedManifest,
    assets,
    componentMetadata,
    inlinedScripts,
    clientDirectives,
    routes,
    serverIslandNameMap,
    key
  };
}

const manifest = deserializeManifest({"hrefRoot":"file:///Users/quantide/apps/content-factory/blog/","cacheDir":"file:///Users/quantide/apps/content-factory/blog/node_modules/.astro/","outDir":"file:///Users/quantide/apps/content-factory/blog/dist/","srcDir":"file:///Users/quantide/apps/content-factory/blog/src/","publicDir":"file:///Users/quantide/apps/content-factory/blog/public/","buildClientDir":"file:///Users/quantide/apps/content-factory/blog/dist/client/","buildServerDir":"file:///Users/quantide/apps/content-factory/blog/dist/server/","adapterName":"","routes":[{"file":"file:///Users/quantide/apps/content-factory/blog/dist/contact/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/contact","isIndex":false,"type":"page","pattern":"^\\/contact\\/$","segments":[[{"content":"contact","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/contact.astro","pathname":"/contact","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/en/contact/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/en/contact","isIndex":false,"type":"page","pattern":"^\\/en\\/contact\\/$","segments":[[{"content":"en","dynamic":false,"spread":false}],[{"content":"contact","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/en/contact.astro","pathname":"/en/contact","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/en/express/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/en/express","isIndex":false,"type":"page","pattern":"^\\/en\\/express\\/$","segments":[[{"content":"en","dynamic":false,"spread":false}],[{"content":"express","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/en/express.astro","pathname":"/en/express","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/en/tags/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/en/tags","isIndex":false,"type":"page","pattern":"^\\/en\\/tags\\/$","segments":[[{"content":"en","dynamic":false,"spread":false}],[{"content":"tags","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/en/tags.astro","pathname":"/en/tags","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/en/topics/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/en/topics","isIndex":true,"type":"page","pattern":"^\\/en\\/topics\\/$","segments":[[{"content":"en","dynamic":false,"spread":false}],[{"content":"topics","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/en/topics/index.astro","pathname":"/en/topics","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/en/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/en","isIndex":true,"type":"page","pattern":"^\\/en\\/$","segments":[[{"content":"en","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/en/index.astro","pathname":"/en","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/express/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/express","isIndex":false,"type":"page","pattern":"^\\/express\\/$","segments":[[{"content":"express","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/express.astro","pathname":"/express","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/llms.txt","links":[],"scripts":[],"styles":[],"routeData":{"route":"/llms.txt","isIndex":false,"type":"endpoint","pattern":"^\\/llms\\.txt\\/?$","segments":[[{"content":"llms.txt","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/llms.txt.ts","pathname":"/llms.txt","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/robots.txt","links":[],"scripts":[],"styles":[],"routeData":{"route":"/robots.txt","isIndex":false,"type":"endpoint","pattern":"^\\/robots\\.txt\\/?$","segments":[[{"content":"robots.txt","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/robots.txt.ts","pathname":"/robots.txt","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/rss.xml","links":[],"scripts":[],"styles":[],"routeData":{"route":"/rss.xml","isIndex":false,"type":"endpoint","pattern":"^\\/rss\\.xml\\/?$","segments":[[{"content":"rss.xml","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/rss.xml.js","pathname":"/rss.xml","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/tags/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/tags","isIndex":false,"type":"page","pattern":"^\\/tags\\/$","segments":[[{"content":"tags","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/tags.astro","pathname":"/tags","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/topics/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/topics","isIndex":true,"type":"page","pattern":"^\\/topics\\/$","segments":[[{"content":"topics","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/topics/index.astro","pathname":"/topics","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}},{"file":"file:///Users/quantide/apps/content-factory/blog/dist/index.html","links":[],"scripts":[],"styles":[],"routeData":{"route":"/","isIndex":true,"type":"page","pattern":"^\\/$","segments":[],"params":[],"component":"src/pages/index.astro","pathname":"/","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"always"}}}],"site":"https://www.quantide.cn","base":"/","trailingSlash":"always","compressHTML":true,"componentMetadata":[["/Users/quantide/apps/content-factory/blog/src/pages/blog/posts/[...slug].astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/[source]/[...slug].astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/contact.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/en/contact.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/en/express.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/en/index.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/en/tags.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/en/topics/[id].astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/en/topics/index.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/express.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/index.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/tags.astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/topics/[id].astro",{"propagation":"none","containsHead":true}],["/Users/quantide/apps/content-factory/blog/src/pages/topics/index.astro",{"propagation":"none","containsHead":true}]],"renderers":[],"clientDirectives":[["idle","(()=>{var l=(n,t)=>{let i=async()=>{await(await n())()},e=typeof t.value==\"object\"?t.value:void 0,s={timeout:e==null?void 0:e.timeout};\"requestIdleCallback\"in window?window.requestIdleCallback(i,s):setTimeout(i,s.timeout||200)};(self.Astro||(self.Astro={})).idle=l;window.dispatchEvent(new Event(\"astro:idle\"));})();"],["load","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).load=e;window.dispatchEvent(new Event(\"astro:load\"));})();"],["media","(()=>{var n=(a,t)=>{let i=async()=>{await(await a())()};if(t.value){let e=matchMedia(t.value);e.matches?i():e.addEventListener(\"change\",i,{once:!0})}};(self.Astro||(self.Astro={})).media=n;window.dispatchEvent(new Event(\"astro:media\"));})();"],["only","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).only=e;window.dispatchEvent(new Event(\"astro:only\"));})();"],["visible","(()=>{var a=(s,i,o)=>{let r=async()=>{await(await s())()},t=typeof i.value==\"object\"?i.value:void 0,c={rootMargin:t==null?void 0:t.rootMargin},n=new IntersectionObserver(e=>{for(let l of e)if(l.isIntersecting){n.disconnect(),r();break}},c);for(let e of o.children)n.observe(e)};(self.Astro||(self.Astro={})).visible=a;window.dispatchEvent(new Event(\"astro:visible\"));})();"]],"entryModules":{"\u0000@astro-page:src/pages/[source]/[...slug]@_@astro":"pages/_source_/_---slug_.astro.mjs","\u0000@astro-page:src/pages/blog/posts/[...slug]@_@astro":"pages/blog/posts/_---slug_.astro.mjs","\u0000@astro-page:src/pages/contact@_@astro":"pages/contact.astro.mjs","\u0000@astro-page:src/pages/en/contact@_@astro":"pages/en/contact.astro.mjs","\u0000@astro-page:src/pages/en/express@_@astro":"pages/en/express.astro.mjs","\u0000@astro-page:src/pages/en/index@_@astro":"pages/en.astro.mjs","\u0000@astro-page:src/pages/en/tags@_@astro":"pages/en/tags.astro.mjs","\u0000@astro-page:src/pages/en/topics/[id]@_@astro":"pages/en/topics/_id_.astro.mjs","\u0000@astro-page:src/pages/en/topics/index@_@astro":"pages/en/topics.astro.mjs","\u0000@astro-page:src/pages/express@_@astro":"pages/express.astro.mjs","\u0000@astro-page:src/pages/index@_@astro":"pages/index.astro.mjs","\u0000@astro-page:src/pages/llms.txt@_@ts":"pages/llms.txt.astro.mjs","\u0000@astro-page:src/pages/robots.txt@_@ts":"pages/robots.txt.astro.mjs","\u0000@astro-page:src/pages/rss.xml@_@js":"pages/rss.xml.astro.mjs","\u0000@astro-page:src/pages/tags@_@astro":"pages/tags.astro.mjs","\u0000@astro-page:src/pages/topics/[id]@_@astro":"pages/topics/_id_.astro.mjs","\u0000@astro-page:src/pages/topics/index@_@astro":"pages/topics.astro.mjs","\u0000@astro-renderers":"renderers.mjs","\u0000noop-middleware":"_noop-middleware.mjs","\u0000virtual:astro:actions/noop-entrypoint":"noop-entrypoint.mjs","\u0000@astrojs-manifest":"manifest_DoV-rKJr.mjs","astro:scripts/before-hydration.js":""},"inlinedScripts":[],"assets":["/file:///Users/quantide/apps/content-factory/blog/dist/contact/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/en/contact/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/en/express/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/en/tags/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/en/topics/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/en/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/express/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/llms.txt","/file:///Users/quantide/apps/content-factory/blog/dist/robots.txt","/file:///Users/quantide/apps/content-factory/blog/dist/rss.xml","/file:///Users/quantide/apps/content-factory/blog/dist/tags/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/topics/index.html","/file:///Users/quantide/apps/content-factory/blog/dist/index.html"],"buildFormat":"directory","checkOrigin":false,"allowedDomains":[],"actionBodySizeLimit":1048576,"serverIslandNameMap":[],"key":"g4avCZHPpjRs10GaMIzRThOBkYeEeQj3OIti0UWuoqg="});
if (manifest.sessionConfig) manifest.sessionConfig.driverModule = null;

export { manifest };
