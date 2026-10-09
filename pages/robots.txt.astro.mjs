export { renderers } from '../renderers.mjs';

const SITE = "https://www.quantide.cn";
const GET = () => new Response(
  `User-agent: *
Allow: /

Sitemap: ${SITE}/sitemap-index.xml
`,
  { headers: { "Content-Type": "text/plain; charset=utf-8" } }
);

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  GET
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
