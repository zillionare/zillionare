import { c as createAstro, a as createComponent, d as addAttribute, e as renderHead, b as renderTemplate } from '../../../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import 'clsx';
import { q as listDocs } from '../../../chunks/docs_DzpopuIG.mjs';
export { renderers } from '../../../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
async function getStaticPaths() {
  return listDocs().filter((d) => d.source === "posts").map((d) => ({ params: { slug: d.slug } }));
}
const $$ = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$;
  const { slug } = Astro2.params;
  const target = `/posts/${slug}/`;
  return renderTemplate`<html lang="zh-CN"> <head><meta charset="utf-8"><meta http-equiv="refresh"${addAttribute(`0; url=${target}`, "content")}><link rel="canonical"${addAttribute(target, "href")}><title>已搬迁</title>${renderHead()}</head> <body> <p>页面已搬迁，<a${addAttribute(target, "href")}>点此跳转</a>。</p> </body></html>`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/blog/posts/[...slug].astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/blog/posts/[...slug].astro";
const $$url = "/blog/posts/[...slug]/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$,
  file: $$file,
  getStaticPaths,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
