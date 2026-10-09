import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute } from '../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../chunks/Base_DZRQqO12.mjs';
import { v as getAllMeta } from '../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Index = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Index;
  const posts = getAllMeta("en").sort((a, b) => {
    const da = a.date || "";
    const db = b.date || "";
    if (da !== db) return da < db ? 1 : -1;
    return a.key < b.key ? -1 : 1;
  });
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Quantide \u2014 Quantitative Research & Trading in Practice", "description": "English editions of Quantide articles: factor investing, machine-learning strategies, Python for quant, and China A-share market research.", "theme": theme, "pathname": "/en/", "lang": "en", "altZh": "/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap"> <h1>English Articles</h1> <p class="sub">Machine-translated and localized editions of Quantide's quantitative research articles.</p> <div class="card-columns" data-reveal-batch="12"> ${posts.map((c) => renderTemplate`<div class="card"> <a class="card-link"${addAttribute(c.url, "href")}> <img class="card-img"${addAttribute(c.cover || "/img/logo.jpg", "src")}${addAttribute(c.title, "alt")} loading="lazy"> <div class="card-body"> <h4 class="card-title">${c.title}</h4> <p class="card-text">${c.excerpt}</p> ${c.date && renderTemplate`<p class="card-meta"><span>📅 ${c.date}</span></p>`} </div> </a> </div>`)} </div> </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/en/index.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/en/index.astro";
const $$url = "/en/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
