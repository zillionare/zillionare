import { c as createAstro, a as createComponent, m as maybeRenderHead, d as addAttribute, s as spreadAttributes, b as renderTemplate, f as renderSlot, r as renderComponent, e as renderHead, u as unescapeHTML } from './astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { t as enAttrs, B as encodeUrlPath, v as getAllMeta, g as getSectionTree, i as getAlternateUrl } from './docs_DzpopuIG.mjs';
import 'clsx';

const $$Astro$1 = createAstro("https://www.quantide.cn");
const $$DrawerTree = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro$1, $$props, $$slots);
  Astro2.self = $$DrawerTree;
  const { nodes = [] } = Astro2.props;
  return renderTemplate`${nodes.map((g) => renderTemplate`${maybeRenderHead()}<details class="nav-tree"><summary class="nav-dir"><span class="nav-label">${g.dir}</span><span class="nav-toggle" aria-hidden="true"></span></summary><ul>${g.children.map((c) => c.isDir ? renderTemplate`<li><details class="nav-tree nav-sub"><summary class="nav-dir"><span class="nav-label">${c.name}</span><span class="nav-toggle" aria-hidden="true"></span></summary><ul>${c.kids.map((k) => renderTemplate`<li><a${addAttribute(k.url, "href")}${addAttribute(k.title, "title")}${spreadAttributes(enAttrs(k.url))}>${k.title}</a></li>`)}</ul></details></li>` : renderTemplate`<li><a${addAttribute(c.url, "href")}${addAttribute(c.title, "title")}${spreadAttributes(enAttrs(c.url))}>${c.title}</a></li>`)}</ul></details>`)}`;
}, "/Users/quantide/apps/content-factory/blog/src/components/DrawerTree.astro", void 0);

var __freeze = Object.freeze;
var __defProp = Object.defineProperty;
var __template = (cooked, raw) => __freeze(__defProp(cooked, "raw", { value: __freeze(raw || cooked.slice()) }));
var _a;
const $$Astro = createAstro("https://www.quantide.cn");
const $$Base = createComponent(async ($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Base;
  function sectionTreeFor(source, prefix, lang2 = "zh") {
    try {
      const m = getAllMeta(lang2).find((x) => x.source === source && (!prefix || x.slug.startsWith(prefix)));
      if (!m) return [];
      return getSectionTree(source, m.slug, lang2).tree || [];
    } catch (e) {
      return [];
    }
  }
  const { title, description = "", image = "/img/logo.jpg", theme = "material", activeTab = "", pathname = "", lang = "zh", alternateUrl = "", altEn = "", altZh = "" } = Astro2.props;
  const SITE = "https://www.quantide.cn";
  const siteName = "\u5321\u918D\u91CF\u5316|\u5927\u5BCC\u7FC1\u91CF\u5316";
  const canonical = SITE + encodeUrlPath(pathname || Astro2.url.pathname);
  const ogDesc = description || "\u5321\u918D\u91CF\u5316\uFF08Quantide\uFF09\u6280\u672F\u535A\u5BA2\uFF1A\u4E13\u6CE8\u91CF\u5316\u6295\u8D44\u7814\u7A76\u3001Python \u91CF\u5316\u4EA4\u6613\u7CFB\u7EDF\u5927\u5BCC\u7FC1\u5B9E\u6218\u3001\u91CF\u5316\u8BFE\u7A0B\u4E0E\u514D\u8D39\u5B66\u4E60\u8D44\u6599\u3002";
  const jsonldOrg = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": `${SITE}/#organization`,
    name: siteName,
    alternateName: "Quantide",
    url: SITE,
    logo: { "@type": "ImageObject", url: `${SITE}/img/logo.jpg` },
    sameAs: [
      "https://www.zhihu.com/people/hbaaron",
      "https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c",
      "https://github.com/zillionare"
    ]
  };
  const jsonldSite = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteName,
    alternateName: "Quantide",
    url: SITE,
    publisher: { "@id": `${SITE}/#organization` }
  };
  const themes = [
    { id: "material", name: "Material" },
    { id: "github", name: "GitHub \u6D45\u8272" },
    { id: "dark", name: "\u6DF1\u8272" }
  ];
  const I18N_EN = {
    nav: "Navigation",
    theme: "Theme",
    search: "Search",
    tab_home: "Latest",
    tab_express: "News",
    tab_course: "Courses",
    tab_blog: "Blog",
    tab_products: "Products",
    tab_free: "Free Tutorials",
    tab_topics: "Topics",
    tab_tags: "Tags",
    tab_follow: "Follow Us",
    sec_express: "News",
    sec_course: "Courses",
    sec_blog: "Blog",
    sec_products: "Products",
    sec_free: "Free Tutorials",
    sec_invest: "Investments",
    enter_express: "Open News",
    enter_course: "Open Courses",
    enter_blog: "Open Blog",
    enter_products: "Open Products",
    enter_free: "Open Free Tutorials",
    theme_material: "Material",
    theme_github: "GitHub Light",
    theme_dark: "Dark",
    visit: "Monthly visits",
    visitor: "Visitors",
    foot_slogan: "Quantide \xB7 Quantitative research & Python trading in practice",
    follow_xhs: "Xiaohongshu",
    follow_zhihu: "Zhihu",
    follow_mp: "WeChat"
  };
  const t18n = (key, zhText) => lang === "en" && I18N_EN[key] != null ? I18N_EN[key] : zhText;
  const tabs = [
    { id: "home", name: "\u6700\u65B0\u6587\u7AE0", href: "/", i18n: "tab_home" },
    { id: "express", i18n: "sec_express", enterI18n: "enter_express", name: "\u8D44\u8BAF", href: "/express/", i18n: "tab_express" },
    { id: "course", i18n: "sec_course", enterI18n: "enter_course", name: "\u91CF\u5316\u8BFE\u7A0B", href: "/articles/course/24lectures/intro/", i18n: "tab_course" },
    { id: "blog", i18n: "sec_blog", enterI18n: "enter_blog", name: "\u535A\u5BA2", href: "/posts/tools/agent-on-tracks/", i18n: "tab_blog" },
    { id: "products", i18n: "sec_products", enterI18n: "enter_products", name: "\u91CF\u5316\u4EA7\u54C1", href: "/articles/products/index/", i18n: "tab_products" },
    { id: "free", i18n: "sec_free", enterI18n: "enter_free", name: "\u514D\u8D39\u6559\u7A0B", href: "/articles/python/best-practice-python/chap01/", i18n: "tab_free" },
    { id: "topics", name: "\u4E13\u9898", href: "/topics/", i18n: "tab_topics" },
    { id: "tags", name: "\u6587\u7AE0\u5206\u7C7B", href: "/tags/", i18n: "tab_tags" },
    { id: "follow", name: "Follow Us", href: "/contact/", i18n: "tab_follow" }
  ];
  const DRAWER_SECTIONS = ["express", "course", "blog", "products", "free"];
  function tabHref(id, zhHref) {
    if (lang !== "en") return zhHref;
    if (id === "home") return "/en/";
    const fixed = {
      express: "/en/express/",
      topics: "/en/topics/",
      tags: "/en/tags/",
      follow: "/en/contact/"
    };
    if (fixed[id]) return fixed[id];
    const keyByTab = {
      course: "articles/course/24lectures/intro",
      blog: "posts/tools/agent-on-tracks",
      products: "articles/products/index",
      free: "articles/python/best-practice-python/chap01"
    };
    return keyByTab[id] ? getAlternateUrl(keyByTab[id]) || zhHref : zhHref;
  }
  const drawerSections = [
    { id: "express", name: "\u8D44\u8BAF", href: "/express/", tree: sectionTreeFor("articles", "express/", lang) },
    { id: "course", name: "\u91CF\u5316\u8BFE\u7A0B", href: tabHref("course", "/articles/course/24lectures/intro/"), tree: sectionTreeFor("articles", "course/", lang) },
    { id: "blog", name: "\u535A\u5BA2", href: tabHref("blog", "/posts/tools/agent-on-tracks/"), tree: sectionTreeFor("posts", "", lang) },
    { id: "products", name: "\u91CF\u5316\u4EA7\u54C1", href: tabHref("products", "/articles/products/index/"), tree: sectionTreeFor("articles", "products/", lang) },
    { id: "free", name: "\u514D\u8D39\u6559\u7A0B", href: tabHref("free", "/articles/python/best-practice-python/chap01/"), tree: sectionTreeFor("articles", "python/", lang) }
  ];
  function resolveTab() {
    if (activeTab) return activeTab;
    let p = pathname || "";
    if (p === "/en" || p === "/en/") p = "/";
    else if (p.startsWith("/en/")) p = p.slice(3);
    if (p === "/" || p.startsWith("/articles/course/")) return p === "/" ? "home" : "course";
    if (p === "/express/" || p.startsWith("/articles/express/")) return "express";
    if (p.startsWith("/articles/python/")) return "free";
    if (p.startsWith("/articles/products/")) return "products";
    if (p.startsWith("/articles/") || p.startsWith("/posts/") || p.startsWith("/blog/posts/")) return "blog";
    if (p.startsWith("/tags")) return "tags";
    if (p.startsWith("/contact")) return "follow";
    return "";
  }
  const curTab = resolveTab();
  return renderTemplate(_a || (_a = __template(["<html", "", "", "", '> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description"', '><link rel="icon" href="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/quantide-alpha-yellow.jpg"><title>', '</title><link rel="canonical"', '><meta property="og:site_name"', '><meta property="og:type" content="website"><meta property="og:title"', '><meta property="og:description"', '><meta property="og:url"', '><meta property="og:image"', '><meta name="twitter:card" content="summary_large_image">', '<script type="application/ld+json">', '<\/script><script type="application/ld+json">', '<\/script><link rel="alternate" type="application/rss+xml"', "", `><link rel="stylesheet" href="/blog.css?v=20261010a"><script>
    (function () {
      try {
        var q = new URLSearchParams(location.search).get('theme');
        var t = q || localStorage.getItem('blog-theme') || document.documentElement.dataset.theme || 'material';
        document.documentElement.dataset.theme = t;
        if (q) localStorage.setItem('blog-theme', q);
      } catch (e) {}
    })();
  <\/script><script>
    // \u8BED\u8A00\u504F\u597D\uFF1A\u9996\u6B21\u8FDB\u5165\u5373\u8DF3\u5230\u5BF9\u5E94\u8BED\u8A00\u7248\u672C\uFF08\u6709\u8BD1\u6587/\u5BF9\u7167\u9875\u65F6\uFF09\uFF0C\u907F\u514D"\u4FA7\u680F\u82F1\u6587\u3001\u6B63\u6587\u4E2D\u6587"
    (function () {
      try {
        var lang = localStorage.getItem('quantide-lang');
        if (lang !== 'en' && lang !== 'zh') return;
        var d = document.documentElement;
        var alt = lang === 'en' ? d.getAttribute('data-alt-en') : d.getAttribute('data-alt-zh');
        if (alt) location.replace(alt);
      } catch (e) {}
    })();
  <\/script><!-- Google Analytics 4 --><script async src="https://www.googletagmanager.com/gtag/js?id=G-L3VJKHX7K1"><\/script><script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    // \u8FC7\u6EE4\u65E0\u5934\u6D4F\u89C8\u5668/\u91C7\u96C6\u5668\uFF1A\u5B83\u4EEC\u6E32\u67D3\u9875\u9762\u4F1A\u89E6\u53D1 gtag\uFF0C\u4EA7\u751F 0 \u4E92\u52A8\u7684"\u76F4\u8FDE"\u6D41\u91CF\u6C61\u67D3\u62A5\u8868
    var __bot = navigator.webdriver === true || /HeadlessChrome|PhantomJS/i.test(navigator.userAgent || '');
    if (!__bot) {
      gtag('js', new Date());
      gtag('config', 'G-L3VJKHX7K1');
    }
  <\/script>`, '</head> <body> <header class="topbar"> <button class="nav-burger" type="button" aria-label="\u6253\u5F00\u5BFC\u822A" aria-expanded="false" aria-controls="site-drawer" data-drawer-toggle>\u2630</button> <a class="brand" href="/"> <img src="/img/logo.jpg" alt="\u5321\u918D\u91CF\u5316" class="logo"> <span>\u5321\u918D\u91CF\u5316|\u5927\u5BCC\u7FC1\u91CF\u5316</span> </a> <div class="search-box"> <input id="blog-search" type="search"', ' data-i18n-ph-zh="\u641C\u7D22"', ' data-i18n-placeholder="search"> <div id="blog-search-result" class="search-result" hidden></div> </div> <nav class="theme-switch" aria-label="\u4E3B\u9898"> ', ' </nav> <button type="button" class="lang-toggle" data-lang-toggle aria-label="\u5207\u6362\u8BED\u8A00">', '</button> </header> <nav class="tabs" aria-label="\u680F\u76EE"> ', ' </nav> <!-- \u79FB\u52A8\u7AEF\u62BD\u5C49\uFF08\u22641024px\uFF09\uFF1A\u680F\u76EE + \u4E3B\u9898 + \u6587\u6863\u76EE\u5F55\u6811\uFF1B\u6B63\u6587\u4F18\u5148\uFF0C\u5BFC\u822A\u9ED8\u8BA4\u9690\u85CF --> <div class="drawer-backdrop" data-drawer-close></div> <aside class="drawer" id="site-drawer" aria-label="\u7AD9\u70B9\u5BFC\u822A" aria-hidden="true"> <div class="drawer-head"> <span data-i18n="nav" data-i18n-zh="\u5BFC\u822A">', '</span> <button class="drawer-close" type="button" aria-label="\u5173\u95ED\u5BFC\u822A" data-drawer-close>\u2715</button> </div> <nav class="drawer-tabs" aria-label="\u680F\u76EE\uFF08\u62BD\u5C49\uFF09"> ', " ", ' </nav> <div class="drawer-themes" aria-label="\u4E3B\u9898\uFF08\u62BD\u5C49\uFF09"> <span class="drawer-label" data-i18n="theme" data-i18n-zh="\u4E3B\u9898">', "</span> ", " </div> </aside> ", ' <footer class="foot"> <a class="foot-logo" href="/" title="\u5321\u918D\u91CF\u5316\u9996\u9875"><img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gzh_512.jpg" alt="\u5321\u918D\u91CF\u5316" loading="lazy"></a> <span data-i18n="foot_slogan" data-i18n-zh="\u5321\u918D\u91CF\u5316 \xB7 \u4E13\u6CE8\u91CF\u5316\u6295\u8D44\u7814\u7A76\u4E0E Python \u91CF\u5316\u4EA4\u6613\u5B9E\u6218">', '</span> <span class="foot-follow-links"><a href="https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c" target="_blank" rel="noopener" data-i18n="follow_xhs" data-i18n-zh="\u5C0F\u7EA2\u4E66">', '</a> / <a href="https://www.zhihu.com/people/hbaaron" target="_blank" rel="noopener" data-i18n="follow_zhihu" data-i18n-zh="\u77E5\u4E4E">', '</a> / <a href="https://mp.weixin.qq.com/s/TkE6g9x-qRkiZ2sl1hwpMg" target="_blank" rel="noopener" data-i18n="follow_mp" data-i18n-zh="\u516C\u4F17\u53F7">', '</a></span> <span class="pv" data-site-stats><span data-i18n="visit" data-i18n-zh="\u672C\u6708\u8BBF\u95EE\u91CF">', '</span> <strong data-total-pv>\u2014</strong> \xB7 <span data-i18n="visitor" data-i18n-zh="\u8BBF\u5BA2\u6570">', `</span> <strong data-total-uv>\u2014</strong><span data-updated style="color:var(--text-light);"></span></span> </footer> <script>
    // \u9875\u811A GA4 \u771F\u5B9E\u603B\u6570\uFF1A\u4F18\u5148 jsdelivr\uFF08\u6BCF\u65E5 6 \u70B9 SEO \u4EFB\u52A1\u540C\u6B65\uFF09\uFF0ClocalStorage \u7F13\u5B58 24h\uFF1B
    // \u5931\u8D25\u56DE\u9000\u6784\u5EFA\u671F site-stats.json\uFF08\u968F\u53D1\u5E03\u66F4\u65B0\uFF09
    (function () {
      var KEY = 'cf-site-stats-v1';
      var CDN = 'https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/stats/site-stats.json';
      function render(d) {
        if (!d) return;
        document.querySelectorAll('[data-total-pv]').forEach((el) => { el.textContent = (d.total_pv || 0).toLocaleString(); });
        document.querySelectorAll('[data-total-uv]').forEach((el) => { el.textContent = (d.total_uv || 0).toLocaleString(); });
        if (d.updated_at) {
          var t = new Date(typeof d.updated_at === 'number' ? d.updated_at * 1000 : d.updated_at).toLocaleDateString();
          document.querySelectorAll('[data-updated]').forEach((el) => { el.textContent = \`\uFF08\${t} \u66F4\u65B0\uFF09\`; });
        }
        var pages = d.pages || {};
        var pv = pages[location.pathname];
        document.querySelectorAll('[data-page-pv]').forEach((el) => { el.textContent = pv != null ? Number(pv).toLocaleString() : '\u2014'; });
      }
      function renderStatic() {
        fetch('/site-stats.json').then((r) => r.json()).then(render).catch(() => {});
      }
      renderStatic();
      try {
        var cached = JSON.parse(localStorage.getItem(KEY) || 'null');
        var fresh = cached && (Date.now() - (cached.at || 0) < 24 * 3600 * 1000);
        if (fresh) { render(cached.data); return; }
      } catch (e) {}
      fetch(CDN).then((r) => r.json()).then((d) => {
        render(d);
        try { localStorage.setItem(KEY, JSON.stringify({ at: Date.now(), data: d })); } catch (e) {}
      }).catch(() => {});
    })();
  <\/script> <script>
    (function () {
      try {
        var cur = document.documentElement.dataset.theme;
        document.querySelectorAll('[data-theme-link]').forEach(function (a) {
          a.classList.toggle('active', a.dataset.themeLink === cur);
          var u = new URL(a.href, location.origin);
          u.searchParams.set('theme', a.dataset.themeLink);
          a.href = u.pathname + u.search;
        });
      } catch (e) {}
      // \u8F7B\u91CF\u641C\u7D22\uFF1A\u8C03 pagefind \u9884\u5EFA\u7D22\u5F15\uFF08\u65E0\u7D22\u5F15\u65F6\u9759\u9ED8\u7981\u7528\uFF09
      // pagefind 1.x\uFF1Am.init() \u540E\u76F4\u63A5\u7528 m.debouncedSearch\uFF08\u65E7 m.options() \u5DF2\u5E9F\u5F03\uFF09
      var input = document.getElementById('blog-search');
      var box = document.getElementById('blog-search-result');
      if (!input) return;
      var idxReady = false;
      input.addEventListener('input', async function () {
        var q = input.value.trim();
        if (!q) { box.hidden = true; return; }
        try {
          if (!idxReady) {
            var m = await import('/pagefind/pagefind.js');
            await m.init();
            idxReady = m;
          }
          var r = await idxReady.debouncedSearch(q);
          var items = (r.results || []).slice(0, 8);
          var html = '';
          for (const item of items) {
            const d = await item.data();
            html += '<a href="' + d.url + '">' + ((d.meta && d.meta.title) || d.url) + '</a>';
          }
          box.innerHTML = html || '<span class="none">\u65E0\u7ED3\u679C</span>';
          box.hidden = false;
        } catch (e) { box.hidden = true; }
      });
      document.addEventListener('click', function (e) {
        if (!box.hidden && !e.target.closest('.search-box')) box.hidden = true;
      });
      // \u8BCD\u4E91\u6296\u52A8\uFF1A\u6BCF\u8BCD\u968F\u673A\u65CB\u8F6C \xB18\xB0\u3001\u4E0A\u4E0B\u9519\u4F4D \xB12px\u3001\u900F\u660E\u5EA6 0.75~1\uFF0C
      // \u5B57\u53F7\u6309 data-size\uFF08\u6784\u5EFA\u671F\u6309\u51FA\u73B0\u6B21\u6570\u7EBF\u6027\u8BA1\u7B97\uFF09\uFF0C\u989C\u8272\u6309 data-color\uFF1B
      // \u6BCF\u6B21\u8BBF\u95EE\u91CD\u65B0\u968F\u673A\uFF0C\u6709\u91CD\u53E0\u611F\uFF1B\u987A\u5E8F\u6253\u4E71\uFF0C\u70ED\u95E8\u8BCD\u4E0D\u603B\u5728\u6700\u524D
      try {
        document.querySelectorAll('[data-cloud]').forEach(function (cloud) {
          var spans = Array.prototype.slice.call(cloud.querySelectorAll('.tag-name'));
          // Fisher-Yates \u6D17\u724C\uFF08\u4EC5\u5DE6\u680F\u7A84\u4E91\u6253\u4E71\uFF0Ctags \u9875\u5C45\u4E2D\u5927\u4E91\u4FDD\u6301\u6309\u6B21\u6570\u6392\u5E8F\uFF09
          if (!cloud.hasAttribute('data-center')) {
            for (var i = spans.length - 1; i > 0; i--) {
              var j = Math.floor(Math.random() * (i + 1));
              cloud.insertBefore(spans[j].closest('a'), spans[i].closest('a'));
              var tmp = spans[i]; spans[i] = spans[j]; spans[j] = tmp;
            }
          }
          spans.forEach(function (el) {
            el.style.fontSize = el.dataset.size + 'rem';
            el.style.color = el.dataset.color;
            el.style.transform = 'rotate(' + (Math.random() * 16 - 8).toFixed(1) + 'deg)'
              + ' translateY(' + (Math.random() * 4 - 2).toFixed(1) + 'px)';
            el.style.opacity = (0.75 + Math.random() * 0.25).toFixed(2);
          });
        });
      } catch (e) {}
    })();
  <\/script> <script>
    // \u9996\u9875\u5361\u7247\u6E10\u8FDB reveal\uFF1A\u9996\u5C4F 12 \u5F20\uFF0C\u6EDA\u52A8\u89E6\u53D1\u4E0B\u4E00\u6279\uFF08\u4E0D\u9650\u603B\u91CF\uFF1B\u65E0 JS \u65F6\u5168\u90E8\u53EF\u89C1\uFF09
    (function () {
      var boxes = document.querySelectorAll('[data-reveal-batch]');
      if (!boxes.length) return;
      boxes.forEach(function (box) {
        var batch = parseInt(box.getAttribute('data-reveal-batch'), 10) || 12;
        var cards = box.querySelectorAll(':scope > .card');
        if (cards.length <= batch) return;
        for (var i = batch; i < cards.length; i++) cards[i].style.display = 'none';
        var shown = batch;
        var sentinel = document.createElement('div');
        sentinel.setAttribute('aria-hidden', 'true');
        sentinel.style.height = '1px';
        box.parentNode.insertBefore(sentinel, box.nextSibling);
        var io = new IntersectionObserver(function (entries) {
          if (!entries.some(function (e) { return e.isIntersecting; })) return;
          var next = Math.min(shown + batch, cards.length);
          for (var j = shown; j < next; j++) cards[j].style.display = '';
          shown = next;
          if (shown >= cards.length) { io.disconnect(); sentinel.remove(); }
        }, { rootMargin: '800px' });
        io.observe(sentinel);
      });
    })();
  <\/script> <script>
    // \u79FB\u52A8\u7AEF\u62BD\u5C49\u5BFC\u822A\uFF08\u22641024px\uFF09\uFF1A\u680F\u76EE/\u4E3B\u9898/\u6587\u6863\u76EE\u5F55\u6536\u8FDB\u62BD\u5C49\uFF1B\u684C\u9762 >1024 \u65F6\u76EE\u5F55\u5F52\u4F4D\u4E3A\u4FA7\u680F
    (function () {
      var body = document.body;
      var burger = document.querySelector('[data-drawer-toggle]');
      var drawer = document.getElementById('site-drawer');
      function setOpen(open) {
        body.classList.toggle('drawer-open', open);
        if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (drawer) drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      }
      document.addEventListener('click', function (e) {
        var t = e.target;
        if (!t || !t.closest) return;
        if (t.closest('[data-drawer-toggle]')) { setOpen(!body.classList.contains('drawer-open')); return; }
        if (t.closest('[data-drawer-close]')) { setOpen(false); return; }
        if (t.closest('.drawer a')) { setOpen(false); }
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });

      // \u680F\u76EE\u7236\u8282\u70B9\uFF1A\u70B9\u51FB=\u5C55\u5F00/\u6536\u8D77\u5B50\u76EE\u5F55\uFF08\u4E0D\u8DF3\u8F6C\u3001\u4E0D\u6536\u8D77\u62BD\u5C49\uFF09\uFF1B\u53F6\u5B50\u94FE\u63A5\u624D\u6536\u8D77
      document.addEventListener('click', function (e) {
        var head = e.target && e.target.closest && e.target.closest('[data-sec-toggle]');
        if (head) {
          var bodyEl = head.parentNode && head.parentNode.querySelector('[data-sec-body]');
          if (bodyEl) {
            var willOpen = bodyEl.hidden;
            bodyEl.hidden = !willOpen;
            head.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
            head.classList.toggle('open', willOpen);
          }
        }
      }, true);
    })();
  <\/script> <script>
    (function () {
      var K = 'quantide-lang';
      var EN = {
        nav: 'Navigation', theme: 'Theme', search: 'Search',
        tab_home: 'Latest', tab_express: 'News', tab_course: 'Courses', tab_blog: 'Blog',
        tab_products: 'Products', tab_free: 'Free Tutorials', tab_topics: 'Topics',
        tab_tags: 'Tags', tab_follow: 'Follow Us',
        sec_express: 'News', sec_course: 'Courses', sec_blog: 'Blog',
        sec_products: 'Products', sec_free: 'Free Tutorials',
        enter_express: 'Open News', enter_course: 'Open Courses', enter_blog: 'Open Blog',
        enter_products: 'Open Products', enter_free: 'Open Free Tutorials',
        theme_material: 'Material', theme_github: 'GitHub Light', theme_dark: 'Dark',
        toc: 'Contents', related: 'Related Posts', views: 'views this month',
        series_prev: 'Previous', series_next: 'Next',
        'level_\\u5165\\u95e8': 'Beginner', 'level_\\u8fdb\\u9636': 'Intermediate',
        'level_\\u5b9e\\u6218': 'Practitioner',
        latest: 'Latest Posts', tags_title: 'Tags',
        visit: 'Monthly visits', visitor: 'Visitors',
        foot_slogan: 'Quantide \\u00b7 Quantitative research & Python trading in practice',
        follow_xhs: 'Xiaohongshu', follow_zhihu: 'Zhihu', follow_mp: 'WeChat'
      };
      function currentLang() {
        var stored = null;
        try { stored = localStorage.getItem(K); } catch (e) {}
        if (stored) return stored;
        return document.documentElement.lang === 'en' ? 'en' : 'zh';
      }
      function apply(lang) {
        var d = document.documentElement;
        d.lang = lang === 'en' ? 'en' : 'zh-CN';
        document.querySelectorAll('[data-i18n]').forEach(function (el) {
          var k = el.getAttribute('data-i18n');
          var v = lang === 'en' && EN[k] != null ? EN[k] : el.getAttribute('data-i18n-zh');
          if (v != null) el.textContent = v;
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
          var k = el.getAttribute('data-i18n-placeholder');
          var v = lang === 'en' && EN[k] != null ? EN[k] : el.getAttribute('data-i18n-ph-zh');
          if (v != null) el.setAttribute('placeholder', v);
        });
        document.querySelectorAll('a[data-en-href]').forEach(function (a) {
          if (!a.hasAttribute('data-zh-href')) {
            a.setAttribute('data-zh-href', a.getAttribute('href'));
            if (a.hasAttribute('title')) a.setAttribute('data-zh-title', a.getAttribute('title'));
          }
          var et = a.getAttribute('data-en-title');
          var ed = a.getAttribute('data-en-desc');
          if (lang === 'en') {
            a.setAttribute('href', a.getAttribute('data-en-href'));
            var tEl = a.querySelector('.card-title');
            var dEl = a.querySelector('.card-text');
            if (tEl) {
              if (!tEl.hasAttribute('data-zh-i18n')) tEl.setAttribute('data-zh-i18n', tEl.textContent);
              if (et) tEl.textContent = et;
            } else if (a.childElementCount === 0) {
              if (!a.hasAttribute('data-zh-i18n')) a.setAttribute('data-zh-i18n', a.textContent);
              if (et) a.textContent = et;
            }
            if (dEl && ed) {
              if (!dEl.hasAttribute('data-zh-i18n')) dEl.setAttribute('data-zh-i18n', dEl.textContent);
              dEl.textContent = ed;
            }
            if (a.hasAttribute('title') && et) a.setAttribute('title', et);
          } else {
            a.setAttribute('href', a.getAttribute('data-zh-href'));
            document.querySelectorAll('[data-zh-i18n]').forEach(function (el) {
              el.textContent = el.getAttribute('data-zh-i18n');
            });
            if (a.hasAttribute('data-zh-title')) a.setAttribute('title', a.getAttribute('data-zh-title'));
          }
        });
        document.querySelectorAll('[data-lang-toggle]').forEach(function (b) {
          b.textContent = lang === 'en' ? '\\u4e2d\\u6587' : 'English';
        });
      }
      document.querySelectorAll('[data-i18n]').forEach(function (el) {
        if (!el.hasAttribute('data-i18n-zh')) el.setAttribute('data-i18n-zh', el.textContent);
      });
      document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
        if (!el.hasAttribute('data-i18n-ph-zh')) el.setAttribute('data-i18n-ph-zh', el.getAttribute('placeholder') || '');
      });
      if (currentLang() === 'en') apply('en');
      document.addEventListener('click', function (e) {
        var t = e.target && e.target.closest ? e.target.closest('[data-lang-toggle]') : null;
        if (!t) return;
        e.preventDefault();
        var next = currentLang() === 'en' ? 'zh' : 'en';
        try { localStorage.setItem(K, next); } catch (err) {}
        var d = document.documentElement;
        var alt = next === 'en' ? d.getAttribute('data-alt-en') : d.getAttribute('data-alt-zh');
        if (alt) { location.href = alt; return; }
        apply(next);
      });
    })();
  <\/script> </body> </html>`], ["<html", "", "", "", '> <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description"', '><link rel="icon" href="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/quantide-alpha-yellow.jpg"><title>', '</title><link rel="canonical"', '><meta property="og:site_name"', '><meta property="og:type" content="website"><meta property="og:title"', '><meta property="og:description"', '><meta property="og:url"', '><meta property="og:image"', '><meta name="twitter:card" content="summary_large_image">', '<script type="application/ld+json">', '<\/script><script type="application/ld+json">', '<\/script><link rel="alternate" type="application/rss+xml"', "", `><link rel="stylesheet" href="/blog.css?v=20261010a"><script>
    (function () {
      try {
        var q = new URLSearchParams(location.search).get('theme');
        var t = q || localStorage.getItem('blog-theme') || document.documentElement.dataset.theme || 'material';
        document.documentElement.dataset.theme = t;
        if (q) localStorage.setItem('blog-theme', q);
      } catch (e) {}
    })();
  <\/script><script>
    // \u8BED\u8A00\u504F\u597D\uFF1A\u9996\u6B21\u8FDB\u5165\u5373\u8DF3\u5230\u5BF9\u5E94\u8BED\u8A00\u7248\u672C\uFF08\u6709\u8BD1\u6587/\u5BF9\u7167\u9875\u65F6\uFF09\uFF0C\u907F\u514D"\u4FA7\u680F\u82F1\u6587\u3001\u6B63\u6587\u4E2D\u6587"
    (function () {
      try {
        var lang = localStorage.getItem('quantide-lang');
        if (lang !== 'en' && lang !== 'zh') return;
        var d = document.documentElement;
        var alt = lang === 'en' ? d.getAttribute('data-alt-en') : d.getAttribute('data-alt-zh');
        if (alt) location.replace(alt);
      } catch (e) {}
    })();
  <\/script><!-- Google Analytics 4 --><script async src="https://www.googletagmanager.com/gtag/js?id=G-L3VJKHX7K1"><\/script><script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    // \u8FC7\u6EE4\u65E0\u5934\u6D4F\u89C8\u5668/\u91C7\u96C6\u5668\uFF1A\u5B83\u4EEC\u6E32\u67D3\u9875\u9762\u4F1A\u89E6\u53D1 gtag\uFF0C\u4EA7\u751F 0 \u4E92\u52A8\u7684"\u76F4\u8FDE"\u6D41\u91CF\u6C61\u67D3\u62A5\u8868
    var __bot = navigator.webdriver === true || /HeadlessChrome|PhantomJS/i.test(navigator.userAgent || '');
    if (!__bot) {
      gtag('js', new Date());
      gtag('config', 'G-L3VJKHX7K1');
    }
  <\/script>`, '</head> <body> <header class="topbar"> <button class="nav-burger" type="button" aria-label="\u6253\u5F00\u5BFC\u822A" aria-expanded="false" aria-controls="site-drawer" data-drawer-toggle>\u2630</button> <a class="brand" href="/"> <img src="/img/logo.jpg" alt="\u5321\u918D\u91CF\u5316" class="logo"> <span>\u5321\u918D\u91CF\u5316|\u5927\u5BCC\u7FC1\u91CF\u5316</span> </a> <div class="search-box"> <input id="blog-search" type="search"', ' data-i18n-ph-zh="\u641C\u7D22"', ' data-i18n-placeholder="search"> <div id="blog-search-result" class="search-result" hidden></div> </div> <nav class="theme-switch" aria-label="\u4E3B\u9898"> ', ' </nav> <button type="button" class="lang-toggle" data-lang-toggle aria-label="\u5207\u6362\u8BED\u8A00">', '</button> </header> <nav class="tabs" aria-label="\u680F\u76EE"> ', ' </nav> <!-- \u79FB\u52A8\u7AEF\u62BD\u5C49\uFF08\u22641024px\uFF09\uFF1A\u680F\u76EE + \u4E3B\u9898 + \u6587\u6863\u76EE\u5F55\u6811\uFF1B\u6B63\u6587\u4F18\u5148\uFF0C\u5BFC\u822A\u9ED8\u8BA4\u9690\u85CF --> <div class="drawer-backdrop" data-drawer-close></div> <aside class="drawer" id="site-drawer" aria-label="\u7AD9\u70B9\u5BFC\u822A" aria-hidden="true"> <div class="drawer-head"> <span data-i18n="nav" data-i18n-zh="\u5BFC\u822A">', '</span> <button class="drawer-close" type="button" aria-label="\u5173\u95ED\u5BFC\u822A" data-drawer-close>\u2715</button> </div> <nav class="drawer-tabs" aria-label="\u680F\u76EE\uFF08\u62BD\u5C49\uFF09"> ', " ", ' </nav> <div class="drawer-themes" aria-label="\u4E3B\u9898\uFF08\u62BD\u5C49\uFF09"> <span class="drawer-label" data-i18n="theme" data-i18n-zh="\u4E3B\u9898">', "</span> ", " </div> </aside> ", ' <footer class="foot"> <a class="foot-logo" href="/" title="\u5321\u918D\u91CF\u5316\u9996\u9875"><img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/gzh_512.jpg" alt="\u5321\u918D\u91CF\u5316" loading="lazy"></a> <span data-i18n="foot_slogan" data-i18n-zh="\u5321\u918D\u91CF\u5316 \xB7 \u4E13\u6CE8\u91CF\u5316\u6295\u8D44\u7814\u7A76\u4E0E Python \u91CF\u5316\u4EA4\u6613\u5B9E\u6218">', '</span> <span class="foot-follow-links"><a href="https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c" target="_blank" rel="noopener" data-i18n="follow_xhs" data-i18n-zh="\u5C0F\u7EA2\u4E66">', '</a> / <a href="https://www.zhihu.com/people/hbaaron" target="_blank" rel="noopener" data-i18n="follow_zhihu" data-i18n-zh="\u77E5\u4E4E">', '</a> / <a href="https://mp.weixin.qq.com/s/TkE6g9x-qRkiZ2sl1hwpMg" target="_blank" rel="noopener" data-i18n="follow_mp" data-i18n-zh="\u516C\u4F17\u53F7">', '</a></span> <span class="pv" data-site-stats><span data-i18n="visit" data-i18n-zh="\u672C\u6708\u8BBF\u95EE\u91CF">', '</span> <strong data-total-pv>\u2014</strong> \xB7 <span data-i18n="visitor" data-i18n-zh="\u8BBF\u5BA2\u6570">', `</span> <strong data-total-uv>\u2014</strong><span data-updated style="color:var(--text-light);"></span></span> </footer> <script>
    // \u9875\u811A GA4 \u771F\u5B9E\u603B\u6570\uFF1A\u4F18\u5148 jsdelivr\uFF08\u6BCF\u65E5 6 \u70B9 SEO \u4EFB\u52A1\u540C\u6B65\uFF09\uFF0ClocalStorage \u7F13\u5B58 24h\uFF1B
    // \u5931\u8D25\u56DE\u9000\u6784\u5EFA\u671F site-stats.json\uFF08\u968F\u53D1\u5E03\u66F4\u65B0\uFF09
    (function () {
      var KEY = 'cf-site-stats-v1';
      var CDN = 'https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/stats/site-stats.json';
      function render(d) {
        if (!d) return;
        document.querySelectorAll('[data-total-pv]').forEach((el) => { el.textContent = (d.total_pv || 0).toLocaleString(); });
        document.querySelectorAll('[data-total-uv]').forEach((el) => { el.textContent = (d.total_uv || 0).toLocaleString(); });
        if (d.updated_at) {
          var t = new Date(typeof d.updated_at === 'number' ? d.updated_at * 1000 : d.updated_at).toLocaleDateString();
          document.querySelectorAll('[data-updated]').forEach((el) => { el.textContent = \\\`\uFF08\\\${t} \u66F4\u65B0\uFF09\\\`; });
        }
        var pages = d.pages || {};
        var pv = pages[location.pathname];
        document.querySelectorAll('[data-page-pv]').forEach((el) => { el.textContent = pv != null ? Number(pv).toLocaleString() : '\u2014'; });
      }
      function renderStatic() {
        fetch('/site-stats.json').then((r) => r.json()).then(render).catch(() => {});
      }
      renderStatic();
      try {
        var cached = JSON.parse(localStorage.getItem(KEY) || 'null');
        var fresh = cached && (Date.now() - (cached.at || 0) < 24 * 3600 * 1000);
        if (fresh) { render(cached.data); return; }
      } catch (e) {}
      fetch(CDN).then((r) => r.json()).then((d) => {
        render(d);
        try { localStorage.setItem(KEY, JSON.stringify({ at: Date.now(), data: d })); } catch (e) {}
      }).catch(() => {});
    })();
  <\/script> <script>
    (function () {
      try {
        var cur = document.documentElement.dataset.theme;
        document.querySelectorAll('[data-theme-link]').forEach(function (a) {
          a.classList.toggle('active', a.dataset.themeLink === cur);
          var u = new URL(a.href, location.origin);
          u.searchParams.set('theme', a.dataset.themeLink);
          a.href = u.pathname + u.search;
        });
      } catch (e) {}
      // \u8F7B\u91CF\u641C\u7D22\uFF1A\u8C03 pagefind \u9884\u5EFA\u7D22\u5F15\uFF08\u65E0\u7D22\u5F15\u65F6\u9759\u9ED8\u7981\u7528\uFF09
      // pagefind 1.x\uFF1Am.init() \u540E\u76F4\u63A5\u7528 m.debouncedSearch\uFF08\u65E7 m.options() \u5DF2\u5E9F\u5F03\uFF09
      var input = document.getElementById('blog-search');
      var box = document.getElementById('blog-search-result');
      if (!input) return;
      var idxReady = false;
      input.addEventListener('input', async function () {
        var q = input.value.trim();
        if (!q) { box.hidden = true; return; }
        try {
          if (!idxReady) {
            var m = await import('/pagefind/pagefind.js');
            await m.init();
            idxReady = m;
          }
          var r = await idxReady.debouncedSearch(q);
          var items = (r.results || []).slice(0, 8);
          var html = '';
          for (const item of items) {
            const d = await item.data();
            html += '<a href="' + d.url + '">' + ((d.meta && d.meta.title) || d.url) + '</a>';
          }
          box.innerHTML = html || '<span class="none">\u65E0\u7ED3\u679C</span>';
          box.hidden = false;
        } catch (e) { box.hidden = true; }
      });
      document.addEventListener('click', function (e) {
        if (!box.hidden && !e.target.closest('.search-box')) box.hidden = true;
      });
      // \u8BCD\u4E91\u6296\u52A8\uFF1A\u6BCF\u8BCD\u968F\u673A\u65CB\u8F6C \xB18\xB0\u3001\u4E0A\u4E0B\u9519\u4F4D \xB12px\u3001\u900F\u660E\u5EA6 0.75~1\uFF0C
      // \u5B57\u53F7\u6309 data-size\uFF08\u6784\u5EFA\u671F\u6309\u51FA\u73B0\u6B21\u6570\u7EBF\u6027\u8BA1\u7B97\uFF09\uFF0C\u989C\u8272\u6309 data-color\uFF1B
      // \u6BCF\u6B21\u8BBF\u95EE\u91CD\u65B0\u968F\u673A\uFF0C\u6709\u91CD\u53E0\u611F\uFF1B\u987A\u5E8F\u6253\u4E71\uFF0C\u70ED\u95E8\u8BCD\u4E0D\u603B\u5728\u6700\u524D
      try {
        document.querySelectorAll('[data-cloud]').forEach(function (cloud) {
          var spans = Array.prototype.slice.call(cloud.querySelectorAll('.tag-name'));
          // Fisher-Yates \u6D17\u724C\uFF08\u4EC5\u5DE6\u680F\u7A84\u4E91\u6253\u4E71\uFF0Ctags \u9875\u5C45\u4E2D\u5927\u4E91\u4FDD\u6301\u6309\u6B21\u6570\u6392\u5E8F\uFF09
          if (!cloud.hasAttribute('data-center')) {
            for (var i = spans.length - 1; i > 0; i--) {
              var j = Math.floor(Math.random() * (i + 1));
              cloud.insertBefore(spans[j].closest('a'), spans[i].closest('a'));
              var tmp = spans[i]; spans[i] = spans[j]; spans[j] = tmp;
            }
          }
          spans.forEach(function (el) {
            el.style.fontSize = el.dataset.size + 'rem';
            el.style.color = el.dataset.color;
            el.style.transform = 'rotate(' + (Math.random() * 16 - 8).toFixed(1) + 'deg)'
              + ' translateY(' + (Math.random() * 4 - 2).toFixed(1) + 'px)';
            el.style.opacity = (0.75 + Math.random() * 0.25).toFixed(2);
          });
        });
      } catch (e) {}
    })();
  <\/script> <script>
    // \u9996\u9875\u5361\u7247\u6E10\u8FDB reveal\uFF1A\u9996\u5C4F 12 \u5F20\uFF0C\u6EDA\u52A8\u89E6\u53D1\u4E0B\u4E00\u6279\uFF08\u4E0D\u9650\u603B\u91CF\uFF1B\u65E0 JS \u65F6\u5168\u90E8\u53EF\u89C1\uFF09
    (function () {
      var boxes = document.querySelectorAll('[data-reveal-batch]');
      if (!boxes.length) return;
      boxes.forEach(function (box) {
        var batch = parseInt(box.getAttribute('data-reveal-batch'), 10) || 12;
        var cards = box.querySelectorAll(':scope > .card');
        if (cards.length <= batch) return;
        for (var i = batch; i < cards.length; i++) cards[i].style.display = 'none';
        var shown = batch;
        var sentinel = document.createElement('div');
        sentinel.setAttribute('aria-hidden', 'true');
        sentinel.style.height = '1px';
        box.parentNode.insertBefore(sentinel, box.nextSibling);
        var io = new IntersectionObserver(function (entries) {
          if (!entries.some(function (e) { return e.isIntersecting; })) return;
          var next = Math.min(shown + batch, cards.length);
          for (var j = shown; j < next; j++) cards[j].style.display = '';
          shown = next;
          if (shown >= cards.length) { io.disconnect(); sentinel.remove(); }
        }, { rootMargin: '800px' });
        io.observe(sentinel);
      });
    })();
  <\/script> <script>
    // \u79FB\u52A8\u7AEF\u62BD\u5C49\u5BFC\u822A\uFF08\u22641024px\uFF09\uFF1A\u680F\u76EE/\u4E3B\u9898/\u6587\u6863\u76EE\u5F55\u6536\u8FDB\u62BD\u5C49\uFF1B\u684C\u9762 >1024 \u65F6\u76EE\u5F55\u5F52\u4F4D\u4E3A\u4FA7\u680F
    (function () {
      var body = document.body;
      var burger = document.querySelector('[data-drawer-toggle]');
      var drawer = document.getElementById('site-drawer');
      function setOpen(open) {
        body.classList.toggle('drawer-open', open);
        if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (drawer) drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      }
      document.addEventListener('click', function (e) {
        var t = e.target;
        if (!t || !t.closest) return;
        if (t.closest('[data-drawer-toggle]')) { setOpen(!body.classList.contains('drawer-open')); return; }
        if (t.closest('[data-drawer-close]')) { setOpen(false); return; }
        if (t.closest('.drawer a')) { setOpen(false); }
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });

      // \u680F\u76EE\u7236\u8282\u70B9\uFF1A\u70B9\u51FB=\u5C55\u5F00/\u6536\u8D77\u5B50\u76EE\u5F55\uFF08\u4E0D\u8DF3\u8F6C\u3001\u4E0D\u6536\u8D77\u62BD\u5C49\uFF09\uFF1B\u53F6\u5B50\u94FE\u63A5\u624D\u6536\u8D77
      document.addEventListener('click', function (e) {
        var head = e.target && e.target.closest && e.target.closest('[data-sec-toggle]');
        if (head) {
          var bodyEl = head.parentNode && head.parentNode.querySelector('[data-sec-body]');
          if (bodyEl) {
            var willOpen = bodyEl.hidden;
            bodyEl.hidden = !willOpen;
            head.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
            head.classList.toggle('open', willOpen);
          }
        }
      }, true);
    })();
  <\/script> <script>
    (function () {
      var K = 'quantide-lang';
      var EN = {
        nav: 'Navigation', theme: 'Theme', search: 'Search',
        tab_home: 'Latest', tab_express: 'News', tab_course: 'Courses', tab_blog: 'Blog',
        tab_products: 'Products', tab_free: 'Free Tutorials', tab_topics: 'Topics',
        tab_tags: 'Tags', tab_follow: 'Follow Us',
        sec_express: 'News', sec_course: 'Courses', sec_blog: 'Blog',
        sec_products: 'Products', sec_free: 'Free Tutorials',
        enter_express: 'Open News', enter_course: 'Open Courses', enter_blog: 'Open Blog',
        enter_products: 'Open Products', enter_free: 'Open Free Tutorials',
        theme_material: 'Material', theme_github: 'GitHub Light', theme_dark: 'Dark',
        toc: 'Contents', related: 'Related Posts', views: 'views this month',
        series_prev: 'Previous', series_next: 'Next',
        'level_\\\\u5165\\\\u95e8': 'Beginner', 'level_\\\\u8fdb\\\\u9636': 'Intermediate',
        'level_\\\\u5b9e\\\\u6218': 'Practitioner',
        latest: 'Latest Posts', tags_title: 'Tags',
        visit: 'Monthly visits', visitor: 'Visitors',
        foot_slogan: 'Quantide \\\\u00b7 Quantitative research & Python trading in practice',
        follow_xhs: 'Xiaohongshu', follow_zhihu: 'Zhihu', follow_mp: 'WeChat'
      };
      function currentLang() {
        var stored = null;
        try { stored = localStorage.getItem(K); } catch (e) {}
        if (stored) return stored;
        return document.documentElement.lang === 'en' ? 'en' : 'zh';
      }
      function apply(lang) {
        var d = document.documentElement;
        d.lang = lang === 'en' ? 'en' : 'zh-CN';
        document.querySelectorAll('[data-i18n]').forEach(function (el) {
          var k = el.getAttribute('data-i18n');
          var v = lang === 'en' && EN[k] != null ? EN[k] : el.getAttribute('data-i18n-zh');
          if (v != null) el.textContent = v;
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
          var k = el.getAttribute('data-i18n-placeholder');
          var v = lang === 'en' && EN[k] != null ? EN[k] : el.getAttribute('data-i18n-ph-zh');
          if (v != null) el.setAttribute('placeholder', v);
        });
        document.querySelectorAll('a[data-en-href]').forEach(function (a) {
          if (!a.hasAttribute('data-zh-href')) {
            a.setAttribute('data-zh-href', a.getAttribute('href'));
            if (a.hasAttribute('title')) a.setAttribute('data-zh-title', a.getAttribute('title'));
          }
          var et = a.getAttribute('data-en-title');
          var ed = a.getAttribute('data-en-desc');
          if (lang === 'en') {
            a.setAttribute('href', a.getAttribute('data-en-href'));
            var tEl = a.querySelector('.card-title');
            var dEl = a.querySelector('.card-text');
            if (tEl) {
              if (!tEl.hasAttribute('data-zh-i18n')) tEl.setAttribute('data-zh-i18n', tEl.textContent);
              if (et) tEl.textContent = et;
            } else if (a.childElementCount === 0) {
              if (!a.hasAttribute('data-zh-i18n')) a.setAttribute('data-zh-i18n', a.textContent);
              if (et) a.textContent = et;
            }
            if (dEl && ed) {
              if (!dEl.hasAttribute('data-zh-i18n')) dEl.setAttribute('data-zh-i18n', dEl.textContent);
              dEl.textContent = ed;
            }
            if (a.hasAttribute('title') && et) a.setAttribute('title', et);
          } else {
            a.setAttribute('href', a.getAttribute('data-zh-href'));
            document.querySelectorAll('[data-zh-i18n]').forEach(function (el) {
              el.textContent = el.getAttribute('data-zh-i18n');
            });
            if (a.hasAttribute('data-zh-title')) a.setAttribute('title', a.getAttribute('data-zh-title'));
          }
        });
        document.querySelectorAll('[data-lang-toggle]').forEach(function (b) {
          b.textContent = lang === 'en' ? '\\\\u4e2d\\\\u6587' : 'English';
        });
      }
      document.querySelectorAll('[data-i18n]').forEach(function (el) {
        if (!el.hasAttribute('data-i18n-zh')) el.setAttribute('data-i18n-zh', el.textContent);
      });
      document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
        if (!el.hasAttribute('data-i18n-ph-zh')) el.setAttribute('data-i18n-ph-zh', el.getAttribute('placeholder') || '');
      });
      if (currentLang() === 'en') apply('en');
      document.addEventListener('click', function (e) {
        var t = e.target && e.target.closest ? e.target.closest('[data-lang-toggle]') : null;
        if (!t) return;
        e.preventDefault();
        var next = currentLang() === 'en' ? 'zh' : 'en';
        try { localStorage.setItem(K, next); } catch (err) {}
        var d = document.documentElement;
        var alt = next === 'en' ? d.getAttribute('data-alt-en') : d.getAttribute('data-alt-zh');
        if (alt) { location.href = alt; return; }
        apply(next);
      });
    })();
  <\/script> </body> </html>`])), addAttribute(lang === "en" ? "en" : "zh-CN", "lang"), addAttribute(theme, "data-theme"), addAttribute(altEn, "data-alt-en"), addAttribute(altZh, "data-alt-zh"), addAttribute(ogDesc, "content"), title, addAttribute(canonical, "href"), addAttribute(siteName, "content"), addAttribute(title, "content"), addAttribute(ogDesc, "content"), addAttribute(canonical, "content"), addAttribute(SITE + image, "content"), alternateUrl && renderTemplate`<link rel="alternate"${addAttribute(lang === "en" ? "zh-CN" : "en", "hreflang")}${addAttribute(SITE + encodeUrlPath(alternateUrl), "href")}>`, unescapeHTML(JSON.stringify(jsonldSite)), unescapeHTML(JSON.stringify(jsonldOrg)), addAttribute(siteName, "title"), addAttribute(`${SITE}/rss.xml`, "href"), renderHead(), addAttribute(t18n("search", "\u641C\u7D22"), "placeholder"), addAttribute(t18n("search", "\u641C\u7D22"), "aria-label"), themes.map((t) => renderTemplate`<a${addAttribute(`?theme=${t.id}`, "href")}${addAttribute(t.id, "data-theme-link")}${addAttribute(t.id === theme ? "active" : "", "class")}${addAttribute(`theme_${t.id}`, "data-i18n")}${addAttribute(t.name, "data-i18n-zh")}>${t18n(`theme_${t.id}`, t.name)}</a>`), lang === "en" ? "\u4E2D\u6587" : "English", tabs.map((t) => renderTemplate`<a${addAttribute(tabHref(t.id, t.href), "href")}${addAttribute(t.id === curTab ? "active" : "", "class")}${addAttribute(t.id === curTab ? "page" : void 0, "aria-current")}${addAttribute(t.i18n, "data-i18n")}${addAttribute(t.name, "data-i18n-zh")}>${t18n(t.i18n, t.name)}</a>`), t18n("nav", "\u5BFC\u822A"), drawerSections.map((sec) => renderTemplate`<div class="drawer-sec"> <button class="drawer-sec-head" type="button" aria-expanded="false" data-sec-toggle> <span${addAttribute(sec.i18n, "data-i18n")}${addAttribute(sec.name, "data-i18n-zh")}>${t18n(sec.i18n, sec.name)}</span><span class="drawer-chev" aria-hidden="true">▸</span> </button> <div class="drawer-sec-body" data-sec-body hidden> <a class="drawer-enter"${addAttribute(sec.href, "href")}><span${addAttribute(sec.enterI18n, "data-i18n")}${addAttribute(`\u8FDB\u5165${sec.name}`, "data-i18n-zh")}>${t18n(sec.enterI18n, `\u8FDB\u5165${sec.name}`)}</span> →</a> <div class="doc-nav drawer-sec-tree"> ${renderComponent($$result, "DrawerTree", $$DrawerTree, { "nodes": sec.tree })} </div> </div> </div>`), tabs.filter((t) => !DRAWER_SECTIONS.includes(t.id)).map((t) => renderTemplate`<a${addAttribute(t.href, "href")}${addAttribute(t.id === curTab ? "active" : "", "class")}${addAttribute(t.i18n, "data-i18n")}${addAttribute(t.name, "data-i18n-zh")}>${t18n(t.i18n, t.name)}</a>`), t18n("theme", "\u4E3B\u9898"), themes.map((t) => renderTemplate`<a${addAttribute(`?theme=${t.id}`, "href")}${addAttribute(t.id, "data-theme-link")}${addAttribute(t.id === theme ? "active" : "", "class")}>${t.name}</a>`), renderSlot($$result, $$slots["default"]), t18n("foot_slogan", "\u5321\u918D\u91CF\u5316 \xB7 \u4E13\u6CE8\u91CF\u5316\u6295\u8D44\u7814\u7A76\u4E0E Python \u91CF\u5316\u4EA4\u6613\u5B9E\u6218"), t18n("follow_xhs", "\u5C0F\u7EA2\u4E66"), t18n("follow_zhihu", "\u77E5\u4E4E"), t18n("follow_mp", "\u516C\u4F17\u53F7"), t18n("visit", "\u672C\u6708\u8BBF\u95EE\u91CF"), t18n("visitor", "\u8BBF\u5BA2\u6570"));
}, "/Users/quantide/apps/content-factory/blog/src/layouts/Base.astro", void 0);

export { $$Base as $ };
