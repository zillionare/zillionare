import { v as getAllMeta } from '../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../renderers.mjs';

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function GET(context) {
  const SITE = "https://www.quantide.cn";
  const items = getAllMeta()
    .filter((m) => m.date)
    .sort((a, b) => (a.date < b.date ? 1 : -1))
    .slice(0, 50)
    .map((m) => {
      const url = SITE + encodeURI(m.url);
      const desc = (m.excerpt || "").replace(/\]\]>/g, "]]&gt;");
      return `    <item>\n      <title>${esc(m.title)}</title>\n      <link>${url}</link>\n      <guid isPermaLink="true">${url}</guid>\n      <pubDate>${new Date(m.date).toUTCString()}</pubDate>\n      <description><![CDATA[${desc}]]></description>\n    </item>`;
    })
    .join("\n");
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>\n    <title>匡醍量化|大富翁量化</title>\n    <link>${SITE}</link>\n    <description>专注量化投资研究与 Python 量化交易实战</description>\n    <language>zh-CN</language>\n${items}\n</channel></rss>`;
  return new Response(xml, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
}

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  GET
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
