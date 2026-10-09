import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, u as unescapeHTML, d as addAttribute, s as spreadAttributes, m as maybeRenderHead } from '../../chunks/astro/server_CTn7mrR8.mjs';
import { a as applyHighlight, A as getTopicIntro, r as renderWithToc, c as admonitions, e as stripRawScripts, x as listMetaByTopic, l as getConvertLink, n as getLevelFor, T as TOPICS, t as enAttrs } from '../../chunks/docs_DzpopuIG.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';
import { $ as $$Base } from '../../chunks/Base_DZRQqO12.mjs';
export { renderers } from '../../renderers.mjs';

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(cooked.slice()) }));
var _a;
const $$Astro = createAstro("https://www.quantide.cn");
async function getStaticPaths() {
  return Object.keys(TOPICS).map((id) => ({ params: { id } }));
}
const $$id = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$id;
  applyHighlight(marked);
  const { id } = Astro2.params;
  const topic = TOPICS[id] || { name: id};
  const intro = getTopicIntro(id);
  let bodyHtml = "";
  try {
    const f = path.join(process.cwd(), "src", "data", "topic-pages", `${id}.md`);
    if (fs.existsSync(f)) {
      const md = fs.readFileSync(f, "utf-8");
      bodyHtml = renderWithToc(marked, admonitions(stripRawScripts(md))).html;
    }
  } catch {
    bodyHtml = "";
  }
  const arts = listMetaByTopic(id);
  const convert = getConvertLink([id]);
  const byLevel = { "\u5165\u95E8": [], "\u8FDB\u9636": [], "\u5B9E\u6218": [] };
  for (const a of arts) {
    const lv = getLevelFor(a.source, a.slug) || "\u8FDB\u9636";
    (byLevel[lv] || byLevel["\u8FDB\u9636"]).push(a);
  }
  const jsonld = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: `${topic.name}\u4E13\u9898`,
    description: intro.slice(0, 160),
    url: `https://www.quantide.cn/topics/${id}/`,
    isPartOf: { "@type": "WebSite", name: "\u5321\u918D\u91CF\u5316", url: "https://www.quantide.cn" }
  };
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": `${topic.name}\u4E13\u9898\uFF1A\u7CBE\u9009\u6587\u7AE0\u4E0E\u9605\u8BFB\u6307\u5F15 | \u5321\u918D\u91CF\u5316`, "activeTab": "topics", "pathname": `/topics/${id}/`, "alternateUrl": `/en/topics/${id}/`, "altEn": `/en/topics/${id}/` }, { "default": ($$result2) => renderTemplate(_a || (_a = __template([" ", '<div class="cards-wrap"> <h1>', '</h1> <p class="sub" style="line-height:1.9;">', "</p> ", ' <p class="sub" style="color:var(--text-light); margin-top:18px;">\u5171 ', " \u7BC7 \xB7 \u6309\u96BE\u5EA6\u5206\u7EC4</p> ", ' <aside class="article-convert" aria-label="\u7EE7\u7EED\u5B66\u4E60"> <a', "><strong>\u{1F449} ", '</strong></a> </aside> <p class="sub"><a href="/topics/">\u2190 \u5168\u90E8\u4E13\u9898</a> \xB7 <a href="/tags/">\u6807\u7B7E\u6D4F\u89C8</a></p> <script type="application/ld+json">', "<\/script> </div> "])), maybeRenderHead(), topic.name, intro, bodyHtml && renderTemplate`<div class="md-body hub-body" data-pagefind-body>${unescapeHTML(bodyHtml)}</div>`, arts.length, ["\u5165\u95E8", "\u8FDB\u9636", "\u5B9E\u6218"].map((lv) => byLevel[lv].length ? renderTemplate`<section> <h2 style="font-size:16px; margin:18px 0 8px;">${lv}（${byLevel[lv].length}）</h2> <ul class="hub-list"> ${byLevel[lv].map((a) => renderTemplate`<li> <a${addAttribute(a.url, "href")}${spreadAttributes(enAttrs(a.url))}>${a.title}</a> <span class="hub-date">${a.date || ""}</span> </li>`)} </ul> </section>` : null), addAttribute(convert.href, "href"), convert.label, unescapeHTML(JSON.stringify(jsonld))) })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/topics/[id].astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/topics/[id].astro";
const $$url = "/topics/[id]/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$id,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
