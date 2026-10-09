import { c as createAstro, a as createComponent, r as renderComponent, b as renderTemplate, m as maybeRenderHead, d as addAttribute } from '../../chunks/astro/server_CTn7mrR8.mjs';
import 'piccolore';
import { $ as $$Base } from '../../chunks/Base_DZRQqO12.mjs';
export { renderers } from '../../renderers.mjs';

const $$Astro = createAstro("https://www.quantide.cn");
const $$Contact = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Contact;
  const theme = Astro2.url.searchParams.get("theme") || "material";
  const channels = [
    {
      name: "Xiaohongshu (RED)",
      url: "https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c",
      desc: "Nearly 50k followers \u2014 the leading quant account on Xiaohongshu. Search \u201CQuantide\u201D and pick the first user."
    },
    {
      name: "WeChat Official Account",
      url: "https://mp.weixin.qq.com/s/TkE6g9x-qRkiZ2sl1hwpMg",
      desc: "Follow \u201CQuantide\u201D on WeChat for daily Python and quantitative strategy content, plus course support."
    },
    {
      name: "Zhihu",
      url: "https://www.zhihu.com/people/hbaaron",
      desc: "Columns and podcasts on Zhihu \u2014 a listed contributor in the economics & management rankings."
    },
    {
      name: "GitHub",
      url: "https://github.com/zillionare",
      desc: "Follow our open-source projects and tools on GitHub."
    }
  ];
  return renderTemplate`${renderComponent($$result, "Base", $$Base, { "title": "Follow Us | Quantide", "description": "Follow Quantide on Xiaohongshu, WeChat, Zhihu and GitHub.", "theme": theme, "activeTab": "follow", "pathname": "/en/contact/", "lang": "en", "alternateUrl": "/contact/", "altZh": "/contact/" }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<div class="doc-layout" style="grid-template-columns: minmax(0, 1fr);"> <article class="doc-main"> <h1>Follow Us</h1> <div class="md-body"> ${channels.map((c) => renderTemplate`<section> <h2>${c.name}</h2> <p>${c.desc} <a${addAttribute(c.url, "href")} target="_blank" rel="noopener">Follow →</a></p> </section>`)} </div> </article> </div> ` })}`;
}, "/Users/quantide/apps/content-factory/blog/src/pages/en/contact.astro", void 0);

const $$file = "/Users/quantide/apps/content-factory/blog/src/pages/en/contact.astro";
const $$url = "/en/contact/";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Contact,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
