import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute, s as spreadAttributes } from '../chunks/astro/server_CTn7mrR8.mjs';
import { z as homeCards, t as enAttrs } from '../chunks/docs_DzpopuIG.mjs';
import { $ as $$Base } from '../chunks/Base_DZRQqO12.mjs';
export { renderers } from '../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Index = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Index;
  const cards = homeCards();
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "\u5321\u918D\u91CF\u5316|\u5927\u5BCC\u7FC1\u91CF\u5316 - \u91CF\u5316\u6295\u8D44\u7814\u7A76\u4E0E\u4EA4\u6613\u7CFB\u7EDF", "theme": theme, "activeTab": "home", "altEn": "/en/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap"> <h1 data-i18n="latest">最新文章</h1> <p class="sub">专注量化投资研究与 Python 量化交易实战。</p> <div class="card-columns" data-reveal-batch="12"> ${cards.map((c) => renderTemplate`<div class="card"> <a class="card-link"${addAttribute(c.url, "href")}${spreadAttributes(enAttrs(c.url))}> <img class="card-img"${addAttribute(c.cover, "src")}${addAttribute(c.title, "alt")} loading="lazy"> <div class="card-body"> <h4 class="card-title">${c.title}</h4> <p class="card-text">${c.excerpt}</p> <p class="card-meta"> <span>📅 ${c.date}</span> </p> </div> </a> </div>`)} </div> </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/index.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/index.astro";
const $$url = "";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
