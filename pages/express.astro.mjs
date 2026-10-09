import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, d as addAttribute, m as maybeRenderHead } from '../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../chunks/Base_DZRQqO12.mjs';
import { v as getAllMeta } from '../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Express = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Express;
  const items = getAllMeta().filter((m) => m.source === "articles" && m.slug.startsWith("express/")).map((m) => {
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
  const latestUrl = items.length ? items[0].url : "";
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "\u6BCF\u65E5\u91CF\u5316\u8D44\u8BAF\u4E0E\u65E5\u62A5\u5F52\u6863 | \u5321\u918D\u91CF\u5316", "theme": theme, "activeTab": "express", "pathname": "/express/", "alternateUrl": "/en/express/", "altEn": "/en/express/" }, { "default": ($$result2) => renderTemplate`${latestUrl && !Astro2.url.searchParams.get("all") && renderTemplate`<meta http-equiv="refresh"${addAttribute(`0; url=${latestUrl}`, "content")}>`}${maybeRenderHead()}<div class="cards-wrap"> <h1>资讯</h1> <p class="sub">每日量化资讯，共 ${items.length} 期。</p> <ul> ${items.map((d, i) => renderTemplate`<li>${i === 0 ? renderTemplate`<strong><a${addAttribute(d.url, "href")}>${d.title}</a>（最新）</strong>` : renderTemplate`<a${addAttribute(d.url, "href")}>${d.title}</a>`}${d.label && renderTemplate`<span style="color: var(--muted); font-size: 0.85em;">（${d.label}）</span>`}</li>`)} </ul> </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/express.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/express.astro";
const $$url = "/express/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Express,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
