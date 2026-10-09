import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, u as unescapeHTML, d as addAttribute, m as maybeRenderHead } from '../../../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../../../chunks/Base_DZRQqO12.mjs';
import { y as topicName, x as listMetaByTopic, n as getLevelFor, T as TOPICS } from '../../../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../../../renderers.mjs';

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
  const { id } = Astro2.params;
  const name = topicName(id, "en");
  const arts = listMetaByTopic(id, "en");
  const LEVEL_EN = { "\u5165\u95E8": "Beginner", "\u8FDB\u9636": "Intermediate", "\u5B9E\u6218": "Practitioner" };
  const byLevel = { "\u5165\u95E8": [], "\u8FDB\u9636": [], "\u5B9E\u6218": [] };
  for (const a of arts) {
    const lv = getLevelFor(a.source, a.slug) || "\u8FDB\u9636";
    (byLevel[lv] || byLevel["\u8FDB\u9636"]).push(a);
  }
  const theme = Astro2.url.searchParams.get("theme") || "material";
  const jsonld = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: `${name} \u2014 Topic`,
    description: `Quantide English articles on ${name}.`,
    url: `https://www.quantide.cn/en/topics/${id}/`,
    inLanguage: "en",
    isPartOf: { "@type": "WebSite", name: "Quantide", url: "https://www.quantide.cn" }
  };
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": `${name}: Selected Articles | Quantide`, "description": `English editions of Quantide articles on ${name}.`, "theme": theme, "activeTab": "topics", "pathname": `/en/topics/${id}/`, "lang": "en", "alternateUrl": `/topics/${id}/`, "altZh": `/topics/${id}/` }, { "default": ($$result2) => renderTemplate(_a || (_a = __template([" ", '<div class="cards-wrap"> <h1>', '</h1> <p class="sub" style="color:var(--text-light); margin-top:18px;">', " articles \xB7 grouped by level</p> ", ' <p class="sub"><a href="/en/topics/">\u2190 All topics</a> \xB7 <a href="/en/tags/">Tag cloud</a> \xB7 <a', '>\u4E2D\u6587\u4E13\u9898</a></p> <script type="application/ld+json">', "<\/script> </div> "])), maybeRenderHead(), name, arts.length, ["\u5165\u95E8", "\u8FDB\u9636", "\u5B9E\u6218"].map((lv) => byLevel[lv].length ? renderTemplate`<section> <h2 style="font-size:16px; margin:18px 0 8px;">${LEVEL_EN[lv] || lv} (${byLevel[lv].length})</h2> <ul class="hub-list"> ${byLevel[lv].map((a) => renderTemplate`<li> <a${addAttribute(a.url, "href")}>${a.title}</a> <span class="hub-date">${a.date || ""}</span> </li>`)} </ul> </section>` : null), addAttribute(`/topics/${id}/`, "href"), unescapeHTML(JSON.stringify(jsonld))) })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/en/topics/[id].astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/en/topics/[id].astro";
const $$url = "/en/topics/[id]/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$id,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
