import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute } from '../../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../../chunks/Base_DZRQqO12.mjs';
import { T as TOPICS, x as listMetaByTopic, y as topicName } from '../../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Index = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Index;
  const topics = Object.keys(TOPICS).map((id) => ({
    id,
    name: topicName(id, "en"),
    count: listMetaByTopic(id, "en").length
  })).sort((a, b) => b.count - a.count);
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Topics | Quantide", "description": "Browse Quantide's English articles by topic: factor investing, machine learning, Python for quant and more.", "theme": theme, "activeTab": "topics", "pathname": "/en/topics/", "lang": "en", "alternateUrl": "/topics/", "altZh": "/topics/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap topics-list"> <h1>Topics</h1> <p class="sub">Reading hubs by topic — counts reflect available English editions. Also browse the <a href="/en/tags/">tag cloud</a>.</p> ${topics.map((t) => renderTemplate`<section class="topic-section"> <h2 class="topic-title"> <a${addAttribute(`/en/topics/${t.id}/`, "href")}>${t.name}</a> <span class="topic-count">${t.count} articles</span> </h2> </section>`)} </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/en/topics/index.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/en/topics/index.astro";
const $$url = "/en/topics/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
