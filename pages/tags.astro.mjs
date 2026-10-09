import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute, s as spreadAttributes } from '../chunks/astro/server_CTn7mrR8.mjs';
import { T as TOPICS, v as getAllMeta, f as getTopicsFor, w as buildTopicsCloud, q as listDocs, t as enAttrs } from '../chunks/docs_DzpopuIG.mjs';
import { $ as $$Base } from '../chunks/Base_DZRQqO12.mjs';
export { renderers } from '../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Tags = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Tags;
  const topicDocs = new Map(Object.keys(TOPICS).map((id) => [id, []]));
  for (const m of getAllMeta()) {
    for (const id of getTopicsFor(m.source, m.slug)) {
      if (topicDocs.has(id)) topicDocs.get(id).push(m);
    }
  }
  const cloud = buildTopicsCloud();
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "\u5168\u90E8\u6587\u7AE0\u6807\u7B7E\u4E0E\u5206\u7C7B\u7D22\u5F15 | \u5321\u918D\u91CF\u5316", "theme": theme, "activeTab": "tags", "pathname": "/tags/", "alternateUrl": "/en/tags/", "altEn": "/en/tags/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap"> <h1 data-i18n="tags_title">文章分类</h1> <p class="sub">共 ${cloud.length} 个主题，${listDocs().length} 篇文档。</p> <div class="tag-cloud tag-cloud-center" data-cloud data-center> ${cloud.map((c) => renderTemplate`<a class="tag"${addAttribute(c.href, "href")}${addAttribute(`${c.tag}\uFF08${c.count} \u7BC7\uFF09`, "title")}> <span class="tag-name"${addAttribute(c.size, "data-size")}${addAttribute(c.color, "data-color")}${addAttribute(c.tag, "data-tag")}>${c.tag}</span> </a>`)} </div> ${cloud.map((c) => renderTemplate`<details class="admonition"${addAttribute(`topic-${c.id}`, "id")}> <summary class="admonition-title">${c.tag}（${c.count}）</summary> <ul> ${(topicDocs.get(c.id) || []).map((d) => renderTemplate`<li><a${addAttribute(d.url, "href")}${spreadAttributes(enAttrs(d.url))}>${d.title}</a>${d.date && renderTemplate`<span style="color: var(--muted); font-size: 0.85em;">（${d.date}）</span>`}</li>`)} </ul> </details>`)} </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/tags.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/tags.astro";
const $$url = "/tags/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Tags,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
