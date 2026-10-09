import { v as getAllMeta } from '../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../renderers.mjs';

const SITE = "https://www.quantide.cn";
const GET = () => {
  const latest = getAllMeta().filter((m) => m.date).sort((a, b) => a.date < b.date ? 1 : -1).slice(0, 50);
  const lines = [
    "# 匡醍量化（Quantide）",
    "",
    "> 专注量化投资研究与 Python 量化交易实战的技术博客与资讯站：因子研究、AI 交易、量化职场与每日行业动态。",
    "",
    "## 核心栏目",
    `- [博客](${SITE}/posts/tools/agent-on-tracks/): 量化技术文章（Python、因子、回测、工具）`,
    `- [资讯](${SITE}/express/): 每日量化行业动态与研报精选`,
    `- [量化课程](${SITE}/articles/course/24lectures/intro/): 24 讲量化课程`,
    `- [免费教程](${SITE}/articles/python/best-practice-python/chap01/): Python 量化入门教程`,
    `- [专题](${SITE}/topics/): 按主题聚合（因子、机器学习、回测、职场等）`,
    "",
    "## 最新文章",
    ...latest.map((m) => `- [${m.title}](${SITE}${m.url}): ${(m.excerpt || "").replace(/\s+/g, " ").slice(0, 140)}`),
    "",
    "## 订阅与索引",
    `- [RSS](${SITE}/rss.xml)`,
    `- [Sitemap](${SITE}/sitemap-index.xml)`,
    ""
  ];
  return new Response(lines.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" }
  });
};

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  GET
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
