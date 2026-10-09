import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, u as unescapeHTML } from '../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import fs from 'node:fs';
import { marked } from 'marked';
import { $ as $$Base } from '../chunks/Base_DZRQqO12.mjs';
import { a as applyHighlight, u as docsRoot, c as admonitions, e as stripRawScripts } from '../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Contact = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Contact;
  applyHighlight(marked);
  const contactPath = [`${docsRoot()}/pages/contact.md`, `${docsRoot()}/contact.md`].find((p) => fs.existsSync(p));
  const raw = fs.readFileSync(contactPath, "utf-8");
  const body = raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "");
  const html = marked.parse(admonitions(stripRawScripts(body)));
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "\u5173\u6CE8\u6211\u4EEC\u4E0E\u8054\u7CFB\u65B9\u5F0F\u6C47\u603B | \u5321\u918D\u91CF\u5316", "theme": theme, "activeTab": "follow", "pathname": "/contact/", "alternateUrl": "/en/contact/", "altEn": "/en/contact/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="doc-layout" style="grid-template-columns: minmax(0, 1fr);"> <article class="doc-main"> <h1>Follow Us</h1> <div class="md-body">${unescapeHTML(html)}</div> </article> </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/contact.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/contact.astro";
const $$url = "/contact/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Contact,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
