import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute } from '../../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../../chunks/Base_DZRQqO12.mjs';
import { v as getAllMeta } from '../../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Express = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Express;
  const items = getAllMeta("en").filter((m) => m.source === "articles" && m.slug.startsWith("express/")).map((m) => {
    const parts = m.slug.split("/");
    let label = m.date || "";
    const tail = parts[parts.length - 1];
    const mm = parts.length >= 4 ? parts[2] : "";
    const yy = parts.length >= 4 ? parts[0] + parts[1] : "";
    if (/^\d{4}$/.test(tail) && /^\d{2}$/.test(mm) && /^\d{2}$/.test(yy)) {
      label = label || `20${yy}-${mm}-${tail.slice(2)}`;
    }
    return { ...m, label };
  }).sort((a, b) => b.label < a.label ? -1 : 1);
  const theme = Astro2.url.searchParams.get("theme") || "material";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Quant Daily News Archive | Quantide", "description": "English editions of Quantide's daily quant news and research digests.", "theme": theme, "activeTab": "express", "pathname": "/en/express/", "lang": "en", "alternateUrl": "/express/", "altZh": "/express/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="cards-wrap"> <h1>News</h1> <p class="sub">Daily quant news and research digests — ${items.length} issues in English.</p> <ul> ${items.map((d, i) => renderTemplate`<li>${i === 0 ? renderTemplate`<strong><a${addAttribute(d.url, "href")}>${d.title}</a>（Latest）</strong>` : renderTemplate`<a${addAttribute(d.url, "href")}>${d.title}</a>`}${d.label && renderTemplate`<span style="color: var(--muted); font-size: 0.85em;">（${d.label}）</span>`}</li>`)} </ul> <p class="sub"><a href="/express/">← 中文资讯</a></p> </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/en/express.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/en/express.astro";
const $$url = "/en/express/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Express,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
