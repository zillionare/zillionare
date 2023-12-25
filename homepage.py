import re

import frontmatter


def get_excerpt(text: str):
    pat = r"(.+)<!--more-->"
    result = re.search(pat, text, re.MULTILINE|re.DOTALL)
    if result  is not None:
        return result.group(1).replace("\n\n", "")
    else:
        return text[:140]

def get_meta(file):
    with open(file, 'r', encoding='utf-8') as f:
        meta, content = frontmatter.parse(f.read())
        excerpt = get_excerpt(content)
        meta["excerpt"] = excerpt
        return meta



