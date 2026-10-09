import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import hljs from 'highlight.js/lib/common';

// 内容源：zillionare docs 下的公开内容，供 Astro getStaticPaths 使用。
// 单根：BLOG_DOCS_DIR；多根：BLOG_DOCS_DIRS（路径分隔符分隔，先到先得，供公开+私有源构建）。
// 发布规则：frontmatter.slug（完整站内路径，如 posts/factor-strategy/x）优先；
// 无 slug 时兼容旧布局（articles/**、blog/posts/**）；两者都没有 → 不发布。

const DOCS_ROOTS = (process.env.BLOG_DOCS_DIRS
  ? process.env.BLOG_DOCS_DIRS.split(path.delimiter).filter(Boolean)
  : [process.env.BLOG_DOCS_DIR || path.join(os.homedir(), 'workspace/zillionare/docs')]);
const DOCS_DIR = DOCS_ROOTS[0];
// 内容源：key = URL 前缀，dir = docs 下相对目录（兼容旧布局用）
const SOURCES = [
  { key: 'articles', dir: 'articles' },
  { key: 'posts', dir: path.join('blog', 'posts') },
];
const SOURCE_KEYS = ['articles', 'posts'];
const LEGACY_DIRS = { articles: 'articles', posts: path.join('blog', 'posts') };
// 首页卡片默认图（无 img 且正文无图时用）
const DEFAULT_COVER = '/img/logo.jpg';

// 栏目分段：左栏按栏目显示子树，而非整棵 articles 树
// key = 栏目标识，prefix = slug 前缀，label = 左栏标题
const SECTIONS = [
  { id: 'course', source: 'articles', prefix: 'course/', label: '量化课程' },
  { id: 'free', source: 'articles', prefix: 'python/', label: '免费教程' },
  { id: 'products', source: 'articles', prefix: 'products/', label: '量化产品' },
  // express/investment 归入博客栏目，与 posts 共用左栏树（下文 getSectionTree 处理）
  { id: 'blog', source: 'posts', prefix: '', label: '博客目录' },
];

// URL 路径编码：encodeURI 保中文字节安全，但会放过裸 `%`（如「95%」）——
// 补一次未转义 % → %25，避免 sitemap/链接里的 % 触发 nginx 400。
function encodeUrlPath(p) {
  return encodeURI(p || '').replace(/%(?![0-9A-Fa-f]{2})/g, '%25');
}

// 按 slug 判定所属栏目（返回 SECTIONS 项；express/investment 归 blog）
function resolveSection(source, slug) {
  if (source === 'posts') return SECTIONS.find((s) => s.id === 'blog');
  for (const s of SECTIONS) {
    if (s.source === 'articles' && s.prefix && slug.startsWith(s.prefix)) return s;
  }
  // articles 下未命中分段的（express/investment），归博客栏目
  return SECTIONS.find((s) => s.id === 'blog');
}

function docsRoot() {
  return DOCS_DIR;
}

// 全树扫描（跳过 _/. 前缀与 .navhide 目录），返回 [{rel, abs}]（rel 去 .md）
function walkAll(root) {
  const out = [];
  const rec = (dir, rel, top) => {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch { return; }
    // .navhide 隐藏整棵子树（根目录不生效，保持旧语义）
    if (!top && entries.some((e) => e.name === '.navhide')) return;
    for (const e of entries) {
      if (e.name.startsWith('_') || e.name.startsWith('.')) continue;
      const full = path.join(dir, e.name);
      const r = rel ? `${rel}/${e.name}` : e.name;
      if (e.isDirectory()) rec(full, r, false);
      else if (e.name.endsWith('.md')) out.push({ rel: r.slice(0, -3), abs: full });
    }
  };
  rec(root, '', true);
  return out;
}

// 全部文档：{ source: 'articles'|'posts', slug, url }
// 过滤占位页：blog/posts/index.md（material-blog-plugin 遗留，仅 8 字节 "# Blog"）
const INDEX_PLACEHOLDERS = new Set(['posts/index']);
let _docsIndex = null;
let _docsByKey = null;
function buildDocIndex() {
  if (_docsIndex) return _docsIndex;
  const out = [];
  const seen = new Set();
  for (const root of DOCS_ROOTS) {
    for (const { rel, abs } of walkAll(root)) {
      let meta = {};
      try {
        meta = parseFrontmatter(fs.readFileSync(abs, 'utf-8')).meta;
      } catch { continue; }
      let source = null;
      let slug = null;
      let lang = 'zh';
      // frontmatter.slug 仅在带已知前缀（posts/…、articles/…、en/posts/…）时生效；
      // mkdocs 时代残留的裸 slug（如 slug: factor-ml-faq）忽略，按旧布局取路径 slug
      const fmSlug = (meta.slug || '').replace(/^\/+|\/+$/g, '');
      const fmParts = fmSlug ? fmSlug.split('/') : [];
      if (fmParts.length >= 3 && fmParts[0] === 'en' && SOURCE_KEYS.includes(fmParts[1])) {
        lang = 'en';
        source = fmParts[1];
        slug = fmParts.slice(2).join('/');
      } else if (fmParts.length >= 2 && SOURCE_KEYS.includes(fmParts[0])) {
        source = fmParts[0];
        slug = fmParts.slice(1).join('/');
      } else if (rel === LEGACY_DIRS.articles || rel.startsWith(`${LEGACY_DIRS.articles}/`)) {
        source = 'articles';
        slug = rel.slice(LEGACY_DIRS.articles.length).replace(/^\//, '');
      } else if (rel === LEGACY_DIRS.posts || rel.startsWith(`${LEGACY_DIRS.posts}/`)) {
        source = 'posts';
        slug = rel.slice(LEGACY_DIRS.posts.length).replace(/^\//, '');
      } else {
        continue; // 非发布内容（podcast/videoscripts/根级页面等）
      }
      if (!slug) continue;
      const key = `${lang === 'en' ? 'en/' : ''}${source}/${slug}`;
      if (seen.has(key) || INDEX_PLACEHOLDERS.has(key)) continue;
      seen.add(key);
      const url = lang === 'en' ? encodeUrlPath(`/en/${source}/${slug}/`) : encodeUrlPath(`/${key}/`);
      out.push({ source, slug, url, key, lang, rel, path: abs });
    }
  }
  // 排序与旧行为一致：articles 前 posts 后，组内按 slug 字典序（同 slug 时 zh 前 en 后）
  out.sort((a, b) => (SOURCE_KEYS.indexOf(a.source) - SOURCE_KEYS.indexOf(b.source))
    || (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0)
    || (a.lang < b.lang ? -1 : a.lang > b.lang ? 1 : 0));
  _docsIndex = out;
  _docsByKey = new Map(out.map((d) => [d.key, d]));
  return out;
}
function listDocs() {
  return buildDocIndex().map(({ source, slug, url, key, lang, rel }) => ({ source, slug, url, key, lang, rel }));
}

// 按 key（zh: posts/x；en: en/posts/x）取文件路径
function docPathByKey(key) {
  buildDocIndex();
  const hit = _docsByKey.get(String(key || ''));
  return hit ? hit.path : null;
}

// zh URL → en 译文 {url,title} 映射（供链接级语言切换）
let _enAlt = null;
function enAltMap() {
  if (_enAlt) return _enAlt;
  _enAlt = new Map();
  const enByKey = new Map(getAllMeta('en').map((m) => [m.key, m]));
  for (const m of getAllMeta('zh')) {
    const en = enByKey.get(`en/${m.key}`);
    if (en) _enAlt.set(m.url, { url: en.url, title: en.title, desc: en.excerpt || '' });
  }
  return _enAlt;
}
// 给链接附加语言切换属性（有译文时）：data-en-href / data-en-title
function enAttrs(url) {
  const hit = enAltMap().get(url);
  if (!hit) return {};
  const out = { 'data-en-href': hit.url, 'data-en-title': hit.title };
  if (hit.desc) out['data-en-desc'] = hit.desc;
  return out;
}

// 语言配对：zh key ↔ en key 的对方 URL（不存在返回 null）
function getAlternateUrl(key) {
  buildDocIndex();
  let altKey = null;
  if (key.startsWith('en/')) altKey = key.slice(3);
  else if (key.startsWith('posts/') || key.startsWith('articles/')) altKey = `en/${key}`;
  const hit = altKey ? _docsByKey.get(altKey) : null;
  return hit ? hit.url : null;
}

function docPath(source, slug) {
  const idx = buildDocIndex();
  const hit = _docsByKey.get(`${source}/${slug}`);
  if (hit) return hit.path;
  const s = SOURCES.find((x) => x.key === source);
  if (!s) throw new Error(`未知内容源: ${source}`);
  return idx && path.join(DOCS_DIR, s.dir, `${slug}.md`);
}

// frontmatter 全解析：支持多行（| 块）、行内数组（[a, b]）、缩进行续行
function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { meta: {}, body: text };
  const meta = {};
  let curKey = null;
  let blockMode = false;
  for (const rawLine of m[1].split('\n')) {
    const line = rawLine.replace(/\r$/, '');
    if (blockMode) {
      if (/^(?: {2,}|\t)/.test(line) || !line.trim()) {
        meta[curKey] += (meta[curKey] ? '\n' : '') + line.trim();
        continue;
      }
      blockMode = false;
      curKey = null;
    }
    const kv = line.match(/^(\w[\w-]*):\s*(.*)$/);
    if (!kv) {
      // 缩进续行（如 tags 下的 - item）
      if (curKey && /^\s+-\s+/.test(line)) {
        meta[curKey] += (meta[curKey] ? ',' : '') + line.replace(/^\s+-\s+/, '').trim();
      }
      continue;
    }
    curKey = kv[1];
    let val = kv[2].trim();
    if (val === '|' || val === '>') {
      meta[curKey] = '';
      blockMode = true;
      continue;
    }
    meta[curKey] = val.replace(/^["']|["']$/g, '');
  }
  return { meta, body: text.slice(m[0].length) };
}

// 取 excerpt：frontmatter excerpt 优先，否则正文首段（去 md 标记，截 120 字）
function makeExcerpt(meta, body) {
  if (meta.excerpt) return meta.excerpt.replace(/\s+/g, ' ').slice(0, 160);
  const text = body
    .replace(/^```[\s\S]*?^```/gm, '')
    .replace(/^---+$/gm, '')
    .replace(/^[#>|\-\* \d.]+/gm, '')
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[([^\]]*)\]\(.*?\)/g, '$1')
    .replace(/[*_`~]/g, '')
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l.length > 20);
  return (text[0] || '').slice(0, 160);
}

// 取封面：返回 {src, auto}
// frontmatter img/image/cover 优先（auto=false，正文不动）；
// 否则取正文第一张图（auto=true，调用方应从正文剔除该图避免重复展示）
function makeCover(meta, body) {
  if (meta.img || meta.image || meta.cover) return { src: meta.img || meta.image || meta.cover, auto: false };
  const m = body.match(/!\[.*?\]\((https?:[^)\s]+)\)/) || body.match(/<img[^>]+src=["'](https?:[^"']+)["']/);
  if (!m) return { src: DEFAULT_COVER, auto: false };
  return { src: m[1], auto: true };
}

// 剔除正文第一张自动封面图（markdown 图片或 <img>，仅首个匹配；<cap> 说明行保留）
function stripAutoCover(body, coverSrc) {
  if (!coverSrc || coverSrc === DEFAULT_COVER) return body;
  const esc = coverSrc.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return body
    .replace(new RegExp(`^[ \\t]*!\\[.*?\\]\\(${esc}\\)[ \\t]*\\n?`, 'm'), '')
    .replace(new RegExp(`^[ \\t]*<img[^>]+src=["']${esc}["'][^>]*>[ \\t]*\\n?`, 'm'), '');
}

// slug 化
function slugify(text) {
  return text.toLowerCase()
    .replace(/[*_`~[\]()]/g, '')
    .replace(/[^\w\u4e00-\u9fff\s-]/g, '')
    .trim().replace(/\s+/g, '-');
}

// 用 marked 渲染并收集 TOC：返回 { html, toc }
// 渲染时给每个 h1-h3 注入 id（已有 id 的保留），TOC 与正文天然一致，锚点永远有效
// 代码块走 highlight.js 构建期高亮：与 TOC renderer 合并为一次 marked.use
// （marked.use 多次调用会互相覆盖同名 renderer，必须合并注册）
// 调用方在顶层只需：import { marked } from "marked"; import { applyHighlight } from "../../lib/docs.js"; applyHighlight(marked);
// 之后所有 code 块带类 hljs language-<lang>，CSS 见 blog.css
function _hlCode(code, lang) {
  try {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    // 无语言标注：只对短块自动检测（防大文本 highlightAuto 吃内存）
    if (!code || code.length > 4000) {
      return code.replace(/&/g, '&amp;').replace(/</g, '&lt;');
    }
    const auto = hljs.highlightAuto(code, ['python', 'bash', 'javascript', 'sql', 'yaml', 'json', 'r', 'cpp']);
    return auto.value;
  } catch {
    return code.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  }
}
function applyHighlight(marked) {
  if (!marked || marked._hl_ready) return;
  marked._hl_ready = true;
}
function renderWithToc(marked, md) {
  const toc = [];
  const seen = {};
  const renderer = {
    heading({ tokens, depth }) {
      if (depth > 3) return false; // h4+ 走默认渲染
      const text = this.parser.parseInline(tokens);
      const plain = text.replace(/<[^>]+>/g, '').replace(/[*_`~[\]()]/g, '').trim();
      let id = slugify(plain) || 'sec';
      seen[id] = (seen[id] || 0) + 1;
      if (seen[id] > 1) id = `${id}-${seen[id] - 1}`;
      toc.push({ level: depth, text: plain.slice(0, 80), id });
      return `<h${depth} id="${id}">${text}</h${depth}>\n`;
    },
    code({ text, lang }) {
      const cls = lang ? `hljs language-${lang}` : 'hljs';
      const lines = (text || '').replace(/\n$/, '').split('\n');
      const gutter = lines
        .map((_, i) => `<span class="cl">${i + 1}</span>`)
        .join('');
      const body = _hlCode(text || '', lang || '');
      return `<pre><code class="${cls}"><span class="ln" aria-hidden="true">${gutter}</span><span class="cl-body">${body}</span></code></pre>\n`;
    },
  };
  marked.use({ renderer });
  const html = marked.parse(md);
  return { html, toc };
}

// ---------- 左栏 / 词云 helpers（模块级缓存，单次构建只读盘一次） ----------

let _allMeta = null;
// 全量元信息：[{source, slug, url, title, date, tags[]}]
function getAllMeta(lang = 'zh') {
  if (!_allMeta) {
    _allMeta = {};
    for (const d of listDocs()) {
      let raw;
      try {
        raw = fs.readFileSync(docPathByKey(d.key), 'utf-8');
      } catch { continue; }
      const { meta, body } = parseFrontmatter(raw);
      (_allMeta[d.lang] = _allMeta[d.lang] || []).push({
        source: d.source,
        slug: d.slug,
        key: d.key,
        lang: d.lang,
        rel: d.rel,
        url: d.url,
        title: meta.title || d.slug.split(path.sep).pop(),
        date: meta.date || '',
        tags: parseTags(meta),
        excerpt: meta.excerpt || makeExcerpt(meta, body),
        cover: makeCover(meta, body).src,
      });
    }
  }
  return _allMeta[lang] || [];
}

// 相关推荐（规则版）：同 tags 交集 → 同目录 → 同 source，取 N 篇。
// LLM 语义版由 Flask 预计算写 related.json，构建期优先读缓存。
function getRelated(source, slug, n = 4) {
  // 1. LLM 缓存优先
  try {
    const cachePath = path.join(process.cwd(), 'src', 'data', 'related.json');
    const cache = JSON.parse(fs.readFileSync(cachePath, 'utf-8'));
    const key = `${source}/${slug}`;
    if (cache[key]?.length) {
      const byUrl = new Map(getAllMeta().map((m) => [m.url, m]));
      const out = cache[key]
        .map((u) => byUrl.get(u))
        .filter(Boolean)
        .slice(0, n);
      if (out.length) return out;
    }
  } catch { /* 无缓存则走规则 */ }
  // 2. 规则版：tags 交集 → 同目录 → 同 source 最新
  const all = getAllMeta();
  const me = all.find((m) => m.source === source && m.slug === slug);
  if (!me) return [];
  const myTags = new Set(me.tags);
  const myDir = slug.includes('/') ? slug.slice(0, slug.lastIndexOf('/')) : '';
  const scored = [];
  for (const m of all) {
    if (m.source === source && m.slug === slug) continue;
    if (m.url.includes('/express/')) continue; // 时效资讯不进相关推荐
    const inter = m.tags.filter((t) => myTags.has(t)).length;
    const sameDir = m.slug.includes('/')
      ? m.slug.slice(0, m.slug.lastIndexOf('/')) === myDir && m.source === source
      : myDir === '' && m.source === source;
    const sameSrc = m.source === source;
    const score = inter * 10 + (sameDir ? 5 : 0) + (sameSrc ? 1 : 0);
    if (score > 0) scored.push({ m, score });
  }
  scored.sort((a, b) => b.score - a.score || (a.m.date < b.m.date ? 1 : -1));
  return scored.slice(0, n).map((s) => s.m);
}

// 统一 tags 解析：按逗号（含中文逗号）分割，尊重引号内的空格/逗号；
// 读写两侧都按此规范：tags: [a, b, "multi word c]
function parseTags(meta) {
  if (!meta.tags) return [];
  // 祛除整体包裹（遗留 "[a, b]" / '"[a, b]"' 形式）
  const s = String(meta.tags).trim().replace(/^[\s\["']+|[\s\]"']+$/g, '').trim();
  // 先按逗号切分，再把引号不配对的相邻段合并（修复 "Hermes Agent" 这类多词标签被拆散）
  const segs = s.split(/[,;，]/);
  const quoteCount = (str) =>
    ((str.replace(/[a-zA-Z0-9\u4e00-\u9fff]['’][a-zA-Z0-9\u4e00-\u9fff]/g, '')).match(/["']/g) || []).length;
  const out = [];
  let buf = null;
  for (const seg of segs) {
    if (buf === null) {
      if (quoteCount(seg) % 2 === 1) buf = seg;
      else out.push(seg);
    } else {
      buf += ',' + seg;
      if (quoteCount(buf) % 2 === 0) { out.push(buf); buf = null; }
    }
  }
  if (buf !== null) out.push(buf);
  return out
    .map((t) => t.trim().replace(/^[\s\["']+|[\s\]"']+$/g, '').trim())
    .filter(Boolean);
}

// 原站词云配色（random-colors.html 12 色），确定性 hash 取色，构建期稳定
const TAG_COLORS = ['DarkRed', 'DarkGoldenrod', 'DarkGreen', 'DarkOliveGreen',
  'DarkCyan', 'DarkTurquoise', 'DarkBlue', 'DarkMagenta',
  'DarkViolet', 'DarkSlateBlue', 'DarkOrchid', 'DarkSlateGray'];
function tagColor(tag) {
  let h = 0;
  for (const c of tag) h = ((h * 31 + c.codePointAt(0)) >>> 0);
  return TAG_COLORS[h % TAG_COLORS.length];
}

// ── 主题分类（13 主题，与 CF seo_topics.py 的 TOPICS 对齐）──
// 主题英文名（EN 列表页/云图；id 同 TOPICS）
const TOPIC_EN = {
  factor: 'Factor Strategies', python: 'Python for Quant', data: 'Data & Storage',
  ml: 'Machine Learning & LLM', algo: 'Algorithms & HFT', backtest: 'Backtesting & Risk',
  career: 'Quant Careers', quant: 'Quant 101', dev: 'Developer Productivity',
  papers: 'Papers & Research', news: 'News', products: 'Products & Ecosystem',
  courses: 'Courses',
};
function topicName(id, lang = 'zh') {
  if (lang === 'en' && TOPIC_EN[id]) return TOPIC_EN[id];
  return TOPICS[id] ? TOPICS[id].name : id;
}
const TOPICS = {
  factor: { name: '因子策略', desc: '因子挖掘、策略研究、Alphalens、组合优化' },
  python: { name: 'Python量化编程', desc: 'Numpy/Pandas、Jupyter、Python 工程实践' },
  data: { name: '数据与存储', desc: '数据源选型、数据库、存储格式、数据工程' },
  ml: { name: '机器学习与LLM', desc: '机器学习、深度学习、LLM 与 Agent 交易' },
  algo: { name: '算法与高频交易', desc: '算法交易、高频、期权波动率、做市套利' },
  backtest: { name: '回测与风控', desc: '回测框架、绩效评估、风险管理、统计基础' },
  career: { name: '量化职场', desc: '量化职业、人物、求职与成长' },
  quant: { name: '量化通识', desc: '量化投资通识、市场、交易与 QMT 实盘接口' },
  dev: { name: '开发效率', desc: 'AI 编程助手、开发工具、效率工程' },
  papers: { name: '研报与论文', desc: '研报解读、论文复现、免费学术资源' },
  news: { name: '资讯', desc: '市场资讯、周报、快讯（时效内容）' },
  products: { name: '产品与生态', desc: '大富翁产品、开源生态、免费资源站' },
  courses: { name: '课程', desc: '量化课程、入门路径、新手指南' },
};

// 文章所属主题（读 CF 生成的 src/data/topics.json，key 口径同 related.json）
function getTopicsFor(source, slug) {
  try {
    const cache = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'src', 'data', 'topics.json'), 'utf-8'));
    return (cache[`${source}/${slug}`] || []).filter((id) => TOPICS[id]);
  } catch {
    return [];
  }
}

// 主题云（文章页侧栏 + tags 页用）：[{id, tag(中文名), count, size, color, href}]
function buildTopicsCloud(lang = 'zh') {
  const counts = {};
  if (lang === 'en') {
    for (const m of getAllMeta('en')) {
      for (const id of getTopicsFor(m.source, m.slug)) {
        if (TOPICS[id]) counts[id] = (counts[id] || 0) + 1;
      }
    }
  } else {
    let cache = {};
    try {
      cache = JSON.parse(
        fs.readFileSync(path.join(process.cwd(), 'src', 'data', 'topics.json'), 'utf-8'));
    } catch {}
    for (const ids of Object.values(cache)) {
      for (const id of ids) {
        if (TOPICS[id]) counts[id] = (counts[id] || 0) + 1;
      }
    }
  }
  const vals = Object.values(counts);
  const lo = vals.length ? Math.min(...vals) : 0;
  const hi = vals.length ? Math.max(...vals) : 1;
  const span = hi - lo || 1;
  const base = lang === 'en' ? '/en/topics/' : '/topics/';
  return Object.keys(TOPICS)
    .map((id) => ({
      id,
      tag: topicName(id, lang),
      count: counts[id] || 0,
      size: (0.7 + (((counts[id] || 0) - lo) / span) * 0.9).toFixed(2),
      color: tagColor(TOPICS[id].name),
      href: `${base}${id}/`,
    }))
    .sort((a, b) => b.count - a.count);
}

// 系列导航：同目录同级文档，按"文件名数字前缀 → 文件名"排序（不依赖杂乱的 seq 字段）。
// 返回 {prev, next, index, total}（prev/next: {url, title} 或 null；index: /tags/#topic-<第一个主题> 或 null）
// 注意：articles 目录多为章节系列（01-xx/02-xx），天然成链；news/单篇目录单文件时返回 null。
function getSeriesNav(source, slug, lang = 'zh') {
  const dir = slug.includes('/') ? slug.slice(0, slug.lastIndexOf('/')) : '';
  const sibs = getAllMeta(lang)
    .filter((m) => m.source === source
      && (m.slug.includes('/') ? m.slug.slice(0, m.slug.lastIndexOf('/')) : '') === dir
      && !m.url.includes('/express/'))
    .sort((a, b) => {
      const num = (s) => {
        const m2 = (s.split('/').pop() || '').match(/^(\d+)/);
        return m2 ? parseInt(m2[1], 10) : 1e9;
      };
      return (num(a.slug) - num(b.slug)) || (a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0);
    });
  if (sibs.length < 2) return { prev: null, next: null, index: null, total: 0 };
  const idx = sibs.findIndex((m) => m.source === source && m.slug === slug);
  if (idx < 0) return { prev: null, next: null, index: null, total: sibs.length };
  return {
    prev: idx > 0 ? { url: sibs[idx - 1].url, title: sibs[idx - 1].title } : null,
    next: idx < sibs.length - 1 ? { url: sibs[idx + 1].url, title: sibs[idx + 1].title } : null,
    index: null,
    total: sibs.length,
  };
}

// ── 难度与阅读路径（CF 生成 src/data/levels.json；key 口径同 topics/related）──
function getLevelFor(source, slug) {
  try {
    const cache = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'src', 'data', 'levels.json'), 'utf-8'));
    const lv = cache[`${source}/${slug}`];
    return lv === '入门' || lv === '进阶' || lv === '实战' ? lv : null;
  } catch {
    return null;
  }
}

const _LEVEL_ORDER = { '入门': 0, '进阶': 1, '实战': 2 };

// 阅读路径：同主题内按 level → 文件名数字 → slug 排序，给出当前篇的上下文位置。
// 主题内部经常有系列（同目录 01/02/..），排序天然形成学习链。
function getReadingPath(source, slug, topicIds) {
  if (!topicIds || !topicIds.length) return { total: 0, pos: 0, topic: null };
  const topic = topicIds[0];
  let cache = {};
  try {
    cache = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'src', 'data', 'topics.json'), 'utf-8'));
  } catch {}
  const chain = getAllMeta()
    .filter((m) => {
      try {
        return (cache[`${m.source}/${m.slug}`] || []).includes(topic);
      } catch { return false; }
    })
    .sort((a, b) => {
      const la = getLevelFor(a.source, a.slug);
      const lb = getLevelFor(b.source, b.slug);
      const d = ((_LEVEL_ORDER[la] ?? 1) - (_LEVEL_ORDER[lb] ?? 1));
      if (d) return d;
      return a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0;
    });
  const idx = chain.findIndex((m) => m.source === source && m.slug === slug);
  const at = (i) => (i >= 0 && i < chain.length ? { url: chain[i].url, title: chain[i].title } : null);
  return {
    total: chain.length, pos: idx >= 0 ? idx + 1 : 0, topic,
    topicName: TOPICS[topic] ? TOPICS[topic].name : topic,
    prev: idx > 0 ? at(idx - 1) : null,
    next: idx >= 0 && idx < chain.length - 1 ? at(idx + 1) : null,
  };
}

// 专题页：某主题下全部文章（按 难度→日期 倒序），供 /topics/<id>/ 使用
function listMetaByTopic(topicId, lang = 'zh') {
  let cache = {};
  try {
    cache = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'src', 'data', 'topics.json'), 'utf-8'));
  } catch {}
  return getAllMeta(lang)
    .filter((m) => (cache[`${m.source}/${m.slug}`] || []).includes(topicId))
    .sort((a, b) => {
      const la = getLevelFor(a.source, a.slug);
      const lb = getLevelFor(b.source, b.slug);
      const d = ((_LEVEL_ORDER[la] ?? 1) - (_LEVEL_ORDER[lb] ?? 1));
      if (d) return d;
      return (b.date || '') < (a.date || '') ? -1 : (b.date || '') > (a.date || '') ? 1 : 0;
    });
}

// 主题简介（人工维护 src/data/topic-intros.json；缺失回落 TOPICS.desc）
function getTopicIntro(topicId) {
  try {
    const cache = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'src', 'data', 'topic-intros.json'), 'utf-8'));
    if (cache[topicId]) return cache[topicId];
  } catch {}
  return TOPICS[topicId] ? TOPICS[topicId].desc : '';
}

// 转化位目标：按所属主题选课程/产品入口（与 topics.json TOPICS 对齐）
const CONVERT_LINKS = {
  default: { label: '量化 24 课：从 Python 到实盘', href: '/articles/course/24lectures/intro/' },
  python: { label: '免费教程：Numpy / Pandas 量化必修', href: '/articles/python/numpy-pandas/01-introduction/' },
  data: { label: '数据存储选型：HDF5 / Parquet / DuckDB', href: '/tags/#topic-data' },
  qmt: { label: 'QMT 从安装到实盘', href: '/tags/#topic-quant' },
  career: { label: '量化职场：求职与成长', href: '/tags/#topic-career' },
  courses: { label: '量化 24 课：从 Python 到实盘', href: '/articles/course/24lectures/intro/' },
};
function getConvertLink(topicIds) {
  for (const id of topicIds || []) {
    if (CONVERT_LINKS[id]) return { ...CONVERT_LINKS[id], topic: id };
  }
  return { ...CONVERT_LINKS.default, topic: null };
}

// 目录名英文化（EN 侧栏/抽屉）：历史中文目录段 → 英文
const DIR_EN = {
  '2026十大量化技术': 'Top 10 Quant Tech 2026',
  '21天驯化AI打工仔': '21 Days Taming AI',
  '数据持久化': 'Data Persistence',
  '策略研究': 'Strategy Research',
  '量化库': 'Quant Library',
  '量化库-数据持久化': 'Quant Library: Data Persistence',
  '量化杂谈': 'Quant Miscellany',
};
function dirLabel(name, lang) {
  if (lang !== 'en') return name;
  return String(name).split('/').map((s) => DIR_EN[s] || s).join('/');
}

// 栏目分段树：左栏只显示当前栏目子树
// course/free/products → articles 下对应前缀；blog → posts 整棵 + articles/express|investment
// lang='en' 时用英文元数据建树（标题/URL 直接英文，服务端渲染，避免中英闪烁）
// 返回 { label, tree }，tree 格式同 getSourceTree
function getSectionTree(source, slug, lang = 'zh') {
  const sec = resolveSection(source, slug);
  if (sec.id !== 'blog') {
    // 截掉前缀，子树提升一级：python/visualize/x → visualize/x
    // 前缀根下的零散文件（如 products/*.md）收拢到目录名组，不自成一组
    const prefix = sec.prefix;
    const metas = getAllMeta(lang).filter((m) =>
      m.source === 'articles' && m.slug.startsWith(prefix));
    const sub = metas.map((m) => ({
      ...m,
      slug: m.slug.slice(prefix.length),
      url: m.url, // URL 不变
    }));
    const dirName = prefix.replace(/\/$/, '').split('/').pop();
    return { label: sec.label, tree: buildTreeFromMetas(sub, slug.slice(prefix.length), dirName, lang) };
  }
  // 资讯栏目：只列 express，按日期倒序（最新在前）
  if (source === 'articles' && slug.startsWith('express/')) {
    const metas = getAllMeta(lang)
      .filter((m) => m.source === 'articles' && m.slug.startsWith('express/'))
      .sort((a, b) => (a.slug < b.slug ? 1 : -1));
    const tree = [];
    for (const m of metas) {
      const parts = m.slug.split('/');
      const top = parts.length >= 4 ? `${parts[1]}-${parts[2]}` : (parts[1] || '往期');
      const topLabel = dirLabel(top, lang);
      let node = tree.find((n) => n.dir === topLabel);
      if (!node) {
        node = { dir: topLabel, open: slug.startsWith(`express/${top.replace('-', '/')}`), children: [] };
        tree.push(node);
      }
      node.children.push({
        name: m.date || parts[parts.length - 1],
        url: m.url, title: m.title, isDir: false, current: m.slug === slug,
      });
    }
    return { label: '资讯目录', tree };
  }
  // 投资栏目：category 子树（investment/ 前缀剥离，不显示父节点）
  if (source === 'articles' && slug.startsWith('investment/')) {
    const prefix = 'investment/';
    const metas = getAllMeta(lang).filter((m) =>
      m.source === 'articles' && m.slug.startsWith(prefix));
    const sub = metas.map((m) => ({
      ...m,
      slug: m.slug.slice(prefix.length),
      url: m.url, // URL 不变
    }));
    return { label: '投资目录', tree: buildTreeFromMetas(sub, slug.slice(prefix.length), '', lang) };
  }
  // 博客栏目：按物理目录（年/月）分组展示（posts/<year>/<month>/ 重排后的新布局）
  const postMetas = getAllMeta(lang).filter((m) => m.source === 'posts');
  const tree = buildYearMonthTree(postMetas, slug, lang);
  return { label: '博客目录', tree };
}

// 物理目录树：posts/<year>/<month>（en 前缀自动识别）→ [{dir: '2026', children: [月目录节点…]}]
function buildYearMonthTree(metas, curSlug, lang) {
  const MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];
  const ymOf = (rel) => {
    const parts = String(rel || '').split('/');
    const i = parts.indexOf('posts');
    if (i >= 0 && /^\d{4}$/.test(parts[i + 1] || '') && /^\d{2}$/.test(parts[i + 2] || '')) {
      return [parts[i + 1], parts[i + 2]];
    }
    return null;
  };
  const cur = metas.find((m) => m.slug === curSlug);
  const curYM = cur ? ymOf(cur.rel) : null;
  const years = new Map();
  for (const m of metas) {
    const ym = ymOf(m.rel);
    if (!ym) continue; // 非年月目录（历史残留）不展示
    const [y, mo] = ym;
    if (!years.has(y)) {
      years.set(y, { dir: y, open: false, children: [], _months: new Map() });
    }
    const ynode = years.get(y);
    if (!ynode._months.has(mo)) {
      const mnum = parseInt(mo, 10);
      ynode._months.set(mo, {
        name: lang === 'en' ? (MONTHS_EN[mnum - 1] || mo) : `${mnum}月`,
        num: mnum, isDir: true, open: false, kids: [],
      });
      ynode.children.push(ynode._months.get(mo));
    }
    const mnode = ynode._months.get(mo);
    mnode.kids.push({ name: mo, url: m.url, title: m.title, current: m.slug === curSlug, date: m.date || '' });
    if (curYM && curYM[0] === y && curYM[1] === mo) {
      mnode.open = true;
      ynode.open = true;
    }
  }
  const out = [...years.values()].sort((a, b) => (a.dir < b.dir ? 1 : -1));
  for (const ynode of out) {
    ynode.children.sort((a, b) => b.num - a.num);
    for (const mnode of ynode.children) {
      mnode.kids.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1
        : (a.title < b.title ? -1 : 1)));
    }
    delete ynode._months;
  }
  return out;
}

// 由 metas 建树（getSourceTree 内核抽取，供分段树复用）
// flatGroup：单段 slug（如分段根下的零散文件）收拢到的组名；不传则保持自成一组
function buildTreeFromMetas(metas, curSlug, flatGroup = '', lang = 'zh') {
  const curL1 = curSlug.split('/')[0] || '';
  const l1 = new Map();
  const ensureGroup = (name) => {
    if (!l1.has(name)) l1.set(name, { dir: dirLabel(name, lang), open: name === curL1 || (flatGroup && name === flatGroup), children: [], _dirs: new Map() });
    return l1.get(name);
  };
  for (const m of metas) {
    const parts = m.slug.split('/');
    if (parts.length === 1 && flatGroup) {
      // 单段文件：收拢到目录名组，用 title 显示
      const node = ensureGroup(flatGroup);
      node.children.push({ name: parts[0], url: m.url, title: m.title, isDir: false, current: m.slug === curSlug });
      continue;
    }
    const d1 = parts[0];
    const node = ensureGroup(d1);
    if (parts.length === 1) {
      node.children.push({ name: parts[0], url: m.url, title: m.title, isDir: false, current: m.slug === curSlug });
    } else if (parts.length === 2) {
      node.children.push({ name: parts[1], url: m.url, title: m.title, isDir: false, current: m.slug === curSlug });
    } else {
      const d2 = parts[1];
      if (!node._dirs.has(d2)) {
        node._dirs.set(d2, { name: dirLabel(d2, lang), isDir: true, kids: [], open: false });
        node.children.push(node._dirs.get(d2));
      }
      const d2node = node._dirs.get(d2);
      const kid = {
        name: parts.slice(2).join('/'), url: m.url, title: m.title, current: m.slug === curSlug,
      };
      d2node.kids.push(kid);
      if (kid.current) d2node.open = true; // 当前文章所在 L2 自动展开
    }
  }
  for (const node of l1.values()) {
    node.children.sort((a, b) => (a.isDir === b.isDir ? (a.name < b.name ? -1 : 1) : (a.isDir ? -1 : 1)));
    for (const c of node.children) if (c.kids) c.kids.sort((a, b) => (a.name < b.name ? -1 : 1));
    delete node._dirs;
  }
  return [...l1.values()].sort((a, b) => (a.dir < b.dir ? -1 : 1));
}

// 首页卡片：有 date 的文档按日期倒序，取前 N
function homeCards(limit = 0) {
  const cards = [];
  for (const d of listDocs()) {
    if (d.lang !== 'zh') continue;
    let raw;
    try {
      raw = fs.readFileSync(docPathByKey(d.key), 'utf-8');
    } catch { continue; }
    const { meta, body } = parseFrontmatter(raw);
    if (!meta.date) continue;
    cards.push({
      url: d.url,
      title: meta.title || d.slug.split(path.sep).pop(),
      date: meta.date,
      excerpt: makeExcerpt(meta, body),
      cover: makeCover(meta, body).src,
    });
  }
  cards.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1
    : (a.url < b.url ? -1 : 1)));
  return limit > 0 ? cards.slice(0, limit) : cards;
}

// GitHub alert（> [!info]/tip/warning/...）→ !!! kind 标准块，再走统一渲染
// 标题行可选：> **Title** 首行做标题；无标题行则用 kind 名
function githubAlerts(md) {
  return md.replace(/^[ \t]*>[ \t]*\[!([\w+-]+)\][ \t]*\n((?:^[ \t]*>.*\n?)*)/gm,
    (all, kind, body) => {
      const lines = body.split('\n')
        .map((l) => l.replace(/^[ \t]*>[ \t]?/, ''))
        .filter((l, i, a) => !(i === a.length - 1 && !l.trim()));
      let title = '';
      if (lines.length && /^\*\*(.+)\*\*$/.test(lines[0].trim())) {
        title = lines.shift().trim().slice(2, -2);
      }
      const indented = lines.map((l) => (l.trim() ? '    ' + l : '')).join('\n');
      return `!!! ${kind.toLowerCase()}${title ? ` "${title}"` : ''}\n${indented}\n`;
    });
}

// 剥离正文裸 <script> 块（Typora 导出残留，如 syllabus.md 尾部的 sidebar-toc 脚本）
// 围栏代码块内的 <script> 教学示例不受影响（先摘出围栏，处理完再填回）
function stripRawScripts(md) {
  const fences = [];
  const protected_ = md.replace(/^(`{3,}|~{3,})[^\n]*\n[\s\S]*?^\1[ \t]*$/gm,
    (m) => `\u0000FENCE${fences.push(m) - 1}\u0000`);
  const stripped = protected_.replace(/^[ \t]*<script\b[^>]*>[\s\S]*?<\/script>[ \t]*\n?/gim, '');
  return stripped.replace(/\u0000FENCE(\d+)\u0000/g, (_, i) => fences[Number(i)]);
}

// admonition 语法块（!!!/???，含由 githubAlerts 转来的）→ 简单样式的 div/ details
// 正文收集规则：标记行之后，空行与缩进行都属于 admonition（支持多段落）；
// 只有遇到第一个「非空且非缩进」行才结束，该行原样保留给后续解析。
function admonitions(md) {
  md = githubAlerts(md);
  const lines = md.split('\n');
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    // 标题兼容两种写法：带引号（规范）与不带引号（历史稿大量存在，如 `!!! tip 笔记要点`）
    const m = /^(!!!|\?\?\?)\s*([\w+-]+)(?:\s+(?:"([^"]*)"|([^\n"]+)))?\s*$/.exec(lines[i]);
    if (!m) { out.push(lines[i]); continue; }
    const isBang = m[1] === '!!!';
    const kind = m[2];
    const title = (m[3] || m[4] || '').trim();
    const body = [];
    let j = i + 1;
    for (; j < lines.length; j++) {
      const l = lines[j];
      if (!l.trim()) { body.push(''); continue; }
      if (/^(?: {4}|\t)/.test(l)) { body.push(l.replace(/^(?: {4}|\t)/, '')); continue; }
      break;
    }
    while (body.length && !body[body.length - 1].trim()) body.pop();
    const bodyHtml = body.join('\n');
    if (isBang) {
      out.push(`<div class="admonition admonition-${kind}"><p class="admonition-title">${title || kind}</p>\n${bodyHtml}\n</div>`);
    } else {
      out.push(`<details class="admonition admonition-${kind}"><summary class="admonition-title">${title || kind}</summary>\n${bodyHtml}\n</details>`);
    }
    i = j - 1;
  }
  return out.join('\n');
}

export { getTopicIntro as A, encodeUrlPath as B, TOPICS as T, applyHighlight as a, docPath as b, admonitions as c, docPathByKey as d, stripRawScripts as e, getTopicsFor as f, getSectionTree as g, makeExcerpt as h, getAlternateUrl as i, getRelated as j, getSeriesNav as k, getConvertLink as l, makeCover as m, getLevelFor as n, getReadingPath as o, parseFrontmatter as p, listDocs as q, renderWithToc as r, stripAutoCover as s, enAttrs as t, docsRoot as u, getAllMeta as v, buildTopicsCloud as w, listMetaByTopic as x, topicName as y, homeCards as z };
