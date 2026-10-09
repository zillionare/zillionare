import { a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute } from '../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../chunks/Base_DZRQqO12.mjs';
import { T as TOPICS, x as listMetaByTopic, A as getTopicIntro } from '../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../renderers.mjs';

const $$Index = createComponent(($$result, $$props, $$slots) => {
  const topics = Object.keys(TOPICS).map((id) => ({
    id,
    name: TOPICS[id].name,
    intro: getTopicIntro(id),
    count: listMetaByTopic(id).length
  })).sort((a, b) => b.count - a.count);
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "\u6309\u4E3B\u9898\u6574\u7406\u7684\u5168\u90E8\u4E13\u9898 | \u5321\u918D\u91CF\u5316", "activeTab": "topics", "pathname": "/topics/", "alternateUrl": "/en/topics/", "altEn": "/en/topics/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap topics-list"> <h1>专题</h1> <p class="sub">按主题整理的阅读入口：每个专题按「入门 → 进阶 → 实战」排序，也可从<a href="/tags/">标签页</a>浏览全部。</p> ${topics.map((t) => renderTemplate`<section class="topic-section"> <h2 class="topic-title"> <a${addAttribute(`/topics/${t.id}/`, "href")}>${t.name}</a> <span class="topic-count">${t.count} 篇</span> </h2> <p class="topic-intro">${t.intro}</p> </section>`)} </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/topics/index.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/topics/index.astro";
const $$url = "/topics/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
