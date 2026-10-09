import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute } from '../../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../../chunks/Base_DZRQqO12.mjs';
import { w as buildTopicsCloud, x as listMetaByTopic } from '../../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Tags = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Tags;
  const cloud = buildTopicsCloud("en");
  const docsByTopic = new Map(cloud.map((c) => [c.id, listMetaByTopic(c.id, "en")]));
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Tags & Topics | Quantide", "description": "Browse all Quantide English articles by topic tag.", "theme": theme, "activeTab": "tags", "pathname": "/en/tags/", "lang": "en", "alternateUrl": "/tags/", "altZh": "/tags/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap"> <h1>Tags</h1> <p class="sub">${cloud.length} topics · English editions only. Also browse <a href="/en/topics/">topic hubs</a>.</p> <div class="tag-cloud tag-cloud-center" data-cloud data-center> ${cloud.map((c) => renderTemplate`<a class="tag"${addAttribute(c.href, "href")}${addAttribute(`${c.tag} (${c.count})`, "title")}> <span class="tag-name"${addAttribute(c.size, "data-size")}${addAttribute(c.color, "data-color")}${addAttribute(c.tag, "data-tag")}>${c.tag}</span> </a>`)} </div> ${cloud.map((c) => renderTemplate`<details class="admonition"${addAttribute(`topic-${c.id}`, "id")}> <summary class="admonition-title">${c.tag} (${c.count})</summary> <ul> ${(docsByTopic.get(c.id) || []).map((d) => renderTemplate`<li><a${addAttribute(d.url, "href")}>${d.title}</a>${d.date && renderTemplate`<span style="color: var(--muted); font-size: 0.85em;">（${d.date}）</span>`}</li>`)} </ul> </details>`)} </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/en/tags.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/en/tags.astro";
const $$url = "/en/tags/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Tags,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
