import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, d as addAttribute, s as spreadAttributes, u as unescapeHTML, m as maybeRenderHead } from '../../chunks/astro/server_CTn7mrR8.mjs';
import fs from 'node:fs';
import { marked } from 'marked';
import { $ as $$Base } from '../../chunks/Base_DZRQqO12.mjs';
import { a as applyHighlight, d as docPathByKey, b as docPath, p as parseFrontmatter, m as makeCover, s as stripAutoCover, r as renderWithToc, c as admonitions, e as stripRawScripts, g as getSectionTree, f as getTopicsFor, h as makeExcerpt, i as getAlternateUrl, j as getRelated, k as getSeriesNav, l as getConvertLink, n as getLevelFor, o as getReadingPath, q as listDocs, t as enAttrs, T as TOPICS } from '../../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../../renderers.mjs';

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(cooked.slice()) }));
var _a, _b, _c;
const $$Astro = createAstro("https://www.quantide.cn");
async function getStaticPaths() {
  return listDocs().map((d) => ({
    params: d.lang === "en" ? { source: "en", slug: `${d.source}/${d.slug}` } : { source: d.source, slug: d.slug }
  }));
}
const $$ = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$;
  applyHighlight(marked);
  const params = Astro2.params;
  let lang = "zh";
  let source = params.source;
  let slug = params.slug;
  if (source === "en") {
    lang = "en";
    const parts = (slug || "").split("/");
    source = parts.shift();
    slug = parts.join("/");
  }
  const key = lang === "en" ? `en/${source}/${slug}` : `${source}/${slug}`;
  const full = docPathByKey(key) || docPath(source, slug);
  const raw = fs.readFileSync(full, "utf-8");
  const { meta, body } = parseFrontmatter(raw);
  const coverInfo = makeCover(meta, body);
  const cover = coverInfo.src;
  const renderBody = coverInfo.auto ? stripAutoCover(body, cover) : body;
  const { html, toc } = renderWithToc(marked, admonitions(stripRawScripts(renderBody)));
  const title = meta.title || slug.split("/").pop();
  const theme = Astro2.url.searchParams.get("theme") || "material";
  const section = getSectionTree(source, slug, lang);
  const navTree = section.tree;
  const SECTION_I18N = {
    "\u91CF\u5316\u8BFE\u7A0B": "sec_course",
    "\u514D\u8D39\u6559\u7A0B": "sec_free",
    "\u91CF\u5316\u4EA7\u54C1": "sec_products",
    "\u535A\u5BA2\u76EE\u5F55": "sec_blog",
    "\u8D44\u8BAF\u76EE\u5F55": "sec_express",
    "\u6295\u8D44\u76EE\u5F55": "sec_invest"
  };
  const SECTION_EN = {
    sec_course: "Courses",
    sec_free: "Free Tutorials",
    sec_products: "Products",
    sec_blog: "Blog",
    sec_express: "News",
    sec_invest: "Investments"
  };
  const sectionKey = SECTION_I18N[section.label];
  const sectionText = lang === "en" && SECTION_EN[sectionKey] ? SECTION_EN[sectionKey] : section.label;
  const topicIds = lang === "en" ? [] : getTopicsFor(source, slug);
  const curUrl = lang === "en" ? `/en/${source}/${slug}/` : `/${source}/${slug}/`;
  const pageDesc = makeExcerpt(meta, renderBody || "");
  const alternateUrl = getAlternateUrl(key);
  const related = lang === "en" ? [] : getRelated(source, slug, 4);
  const series = getSeriesNav(source, slug, lang);
  const convert = lang === "en" ? null : getConvertLink(topicIds);
  const level = lang === "en" ? "" : getLevelFor(source, slug);
  const path = lang === "en" ? [] : getReadingPath(source, slug, topicIds);
  const isExpress = source === "articles" && slug.startsWith("express/");
  const expressEntries = isExpress ? [...html.matchAll(/<h3 id="([^"]+)"[^>]*>([\s\S]*?)<\/h3>/g)].map((m, i) => ({
    "@type": "ListItem",
    position: i + 1,
    name: m[2].replace(/<[^>]+>/g, "").trim(),
    url: `https://www.quantide.cn${curUrl}#${m[1]}`
  })).filter((x) => x.name) : [];
  const jsonldList = expressEntries.length ? {
    "@context": "https://schema.org",
    "@type": "ItemList",
    numberOfItems: expressEntries.length,
    itemListElement: expressEntries,
    mainEntityOfPage: `https://www.quantide.cn${curUrl}`
  } : null;
  function extractFaq(html2) {
    const m = html2.match(/<h2 id="[^"]*">常见问题<\/h2>/);
    if (!m) return [];
    const rest = html2.slice(m.index + m[0].length);
    const endIdx = rest.search(/<h2 id="/);
    const seg = endIdx >= 0 ? rest.slice(0, endIdx) : rest;
    const out = [];
    for (const part of seg.split(/<h3 id="[^"]*">/).slice(1)) {
      const qm = part.match(/^([\s\S]*?)<\/h3>/);
      if (!qm) continue;
      const q = qm[1].replace(/<[^>]+>/g, "").trim();
      const a = part.slice(qm[0].length).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
      if (q && a) out.push({ q, a: a.slice(0, 700) });
    }
    return out;
  }
  const faqItems = extractFaq(html);
  const jsonldFaq = faqItems.length >= 2 ? {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqItems.map(({ q, a }) => ({
      "@type": "Question",
      name: q,
      acceptedAnswer: { "@type": "Answer", text: a }
    }))
  } : null;
  let dateModified = "";
  try {
    dateModified = fs.statSync(full).mtime.toISOString();
  } catch {
  }
  const jsonldArticle = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: title,
    description: pageDesc,
    image: cover.startsWith("http") ? cover : `https://www.quantide.cn${cover}`,
    datePublished: meta.date || void 0,
    dateModified: dateModified || meta.date || void 0,
    keywords: (meta.tags || "").replace(/[\[\]"]/g, "").split(",").map((s) => s.trim()).filter(Boolean),
    inLanguage: lang === "en" ? "en" : "zh-CN",
    author: { "@id": "https://www.quantide.cn/#organization" },
    publisher: { "@id": "https://www.quantide.cn/#organization" },
    mainEntityOfPage: { "@type": "WebPage", "@id": `https://www.quantide.cn${curUrl}` }
  };
  const crumbs = [{ name: lang === "en" ? "Home" : "\u9996\u9875", item: "https://www.quantide.cn/" }, { name: title, item: `https://www.quantide.cn${curUrl}` }];
  const jsonldCrumb = { "@context": "https://schema.org", "@type": "BreadcrumbList", itemListElement: crumbs.map((c, i) => ({ "@type": "ListItem", position: i + 1, name: c.name, item: c.item })) };
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": `${title} | \u5321\u918D\u91CF\u5316`, "description": pageDesc, "image": cover.startsWith("http") ? new URL(cover).pathname : cover, "theme": theme, "pathname": curUrl, "lang": lang, "alternateUrl": alternateUrl || "", "altEn": lang === "en" ? "" : alternateUrl || "", "altZh": lang === "en" ? alternateUrl || "" : "" }, { "default": ($$result2) => renderTemplate(_c || (_c = __template([' <script type="application/ld+json">', '<\/script> <script type="application/ld+json">', "<\/script> ", "", "", '<div class="doc-layout"> <aside class="doc-nav" aria-label="\u6587\u6863\u76EE\u5F55"> <div> <p class="nav-group"', "", ">", "</p> ", " </div> </aside> <article", '> <h1 data-pagefind-meta="title">', '</h1> <p class="meta"> ', " ", " ", " ", ' <span>\u{1F441} <span data-i18n="views" data-i18n-zh="\u672C\u6708\u9605\u8BFB">', "</span> <span data-page-pv>\u2014</span></span> </p> ", ' <div class="md-body" data-pagefind-body>', '</div> <aside class="article-cta" aria-label="\u5173\u6CE8\u516C\u4F17\u53F7"> <img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gzh_512.jpg" alt="Quantide \u516C\u4F17\u53F7\u4E8C\u7EF4\u7801" loading="lazy"> <div> <strong>', "</strong> <p>", "</p> </div> </aside> ", " ", " ", " ", ' </article> <aside class="doc-toc" aria-label="\u672C\u9875\u76EE\u5F55"> <p class="toc-title" data-i18n="toc" data-i18n-zh="\u76EE\u5F55">', "</p> <ul> ", " </ul> </aside> </div> "])), unescapeHTML(JSON.stringify(jsonldArticle)), unescapeHTML(JSON.stringify(jsonldCrumb)), jsonldList && renderTemplate(_a || (_a = __template(['<script type="application/ld+json">', "<\/script>"])), unescapeHTML(JSON.stringify(jsonldList))), jsonldFaq && renderTemplate(_b || (_b = __template(['<script type="application/ld+json">', "<\/script>"])), unescapeHTML(JSON.stringify(jsonldFaq))), maybeRenderHead(), addAttribute(sectionKey, "data-i18n"), addAttribute(section.label, "data-i18n-zh"), sectionText, navTree.map((g) => renderTemplate`<details class="nav-tree"${addAttribute(g.open, "open")}> <summary class="nav-dir"><span class="nav-label">${g.dir}</span><span class="nav-toggle" aria-hidden="true"></span></summary> <ul> ${g.children.map((c) => c.isDir ? renderTemplate`<li> <details class="nav-tree nav-sub"${addAttribute(c.open, "open")}> <summary class="nav-dir"><span class="nav-label">${c.name}</span><span class="nav-toggle" aria-hidden="true"></span></summary> <ul> ${c.kids.map((k) => renderTemplate`<li><a${addAttribute(k.url, "href")}${addAttribute(k.current ? "current" : "", "class")}${addAttribute(k.title, "title")}${spreadAttributes(enAttrs(k.url))}>${k.title}</a></li>`)} </ul> </details> </li>` : renderTemplate`<li><a${addAttribute(c.url, "href")}${addAttribute(c.current ? "current" : "", "class")}${addAttribute(c.title, "title")}${spreadAttributes(enAttrs(c.url))}>${c.title}</a></li>`)} </ul> </details>`), addAttribute(isExpress ? "doc-main is-express" : "doc-main", "class"), title, alternateUrl && renderTemplate`<a class="lang-switch"${addAttribute(alternateUrl, "href")}>${lang === "en" ? "\u4E2D\u6587" : "English"}</a>`, meta.date && renderTemplate`<span>📅 ${meta.date}</span>`, topicIds.length > 0 && renderTemplate`<span class="topic-badges"> ${topicIds.map((id) => renderTemplate`<a class="topic-badge"${addAttribute(`/topics/${id}/`, "href")}>${TOPICS[id].name}</a>`)} </span>`, level && renderTemplate`<span class="level-badge"${addAttribute(level, "data-lv")}${addAttribute(`level_${level}`, "data-i18n")}>${level}</span>`, lang === "en" ? "views this month" : "\u672C\u6708\u9605\u8BFB", false, unescapeHTML(html), lang === "en" ? "Follow us on WeChat: Quantide" : "\u5173\u6CE8\u516C\u4F17\u53F7\uFF1AQuantide", lang === "en" ? "Daily quant insights, strategy research and tool tutorials." : "\u6BCF\u65E5\u91CF\u5316\u5E72\u8D27\u3001\u7B56\u7565\u7814\u7A76\u4E0E\u5DE5\u5177\u6559\u7A0B\uFF0C\u626B\u7801\u4E0D\u9519\u8FC7\u66F4\u65B0\u3002", series.total >= 2 && renderTemplate`<nav class="series-nav" aria-label="本系列"> <div class="series-links"> ${series.prev ? renderTemplate`<a class="series-prev"${addAttribute(series.prev.url, "href")}${spreadAttributes(enAttrs(series.prev.url))}>← <span data-i18n="series_prev" data-i18n-zh="上一篇">${lang === "en" ? "Previous" : "\u4E0A\u4E00\u7BC7"}</span>：${series.prev.title}</a>` : renderTemplate`<span></span>`} ${series.next ? renderTemplate`<a class="series-next"${addAttribute(series.next.url, "href")}${spreadAttributes(enAttrs(series.next.url))}><span data-i18n="series_next" data-i18n-zh="下一篇">${lang === "en" ? "Next" : "\u4E0B\u4E00\u7BC7"}</span>：${series.next.title} →</a>` : renderTemplate`<span></span>`} </div> </nav>`, path.total >= 3 && path.pos > 0 && renderTemplate`<nav class="reading-path" aria-label="阅读路径"> <span>📖 本篇是「${path.topicName}」路径第 ${path.pos}/${path.total} 篇</span> <span class="reading-path-links"> ${path.prev && renderTemplate`<a${addAttribute(path.prev.url, "href")}${spreadAttributes(enAttrs(path.prev.url))}>← ${path.prev.title.slice(0, 18)}</a>`} ${path.next && renderTemplate`<a${addAttribute(path.next.url, "href")}${spreadAttributes(enAttrs(path.next.url))}>${path.next.title.slice(0, 18)} →</a>`} </span> </nav>`, convert && renderTemplate`<aside class="article-convert" aria-label="继续学习"> <a${addAttribute(convert.href, "href")}><strong>👉 ${convert.label}</strong></a> </aside>`, related.length > 0 && renderTemplate`<nav class="related" aria-label="相关阅读"> <h2 data-i18n="related">相关阅读</h2> <ul> ${related.map((r) => renderTemplate`<li> <a${addAttribute(r.url, "href")}${spreadAttributes(enAttrs(r.url))}>${r.title}</a> ${r.excerpt && renderTemplate`<p>${r.excerpt.slice(0, 90)}</p>`} </li>`)} </ul> </nav>`, lang === "en" ? "Contents" : "\u76EE\u5F55", toc.map((t) => renderTemplate`<li${addAttribute(t.level === 3 ? "lv3" : "", "class")}> <a${addAttribute(`#${t.id}`, "href")}${addAttribute(t.text, "title")}>${t.text}</a> </li>`)) })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/[source]/[...slug].astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/[source]/[...slug].astro";
const $$url = "/[source]/[...slug]/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
