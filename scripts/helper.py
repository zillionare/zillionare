import re


def remove_incomplete_html_tags(text):
    """
    移除未闭合的HTML标签及其后面的内容

    Args:
        text (str): 需要处理的文本

    Returns:
        str: 处理后的文本
    """
    # 更简单的实现方式：使用正则表达式直接处理
    return remove_incomplete_html_tags_simple(text)


def remove_incomplete_html_tags_simple(text):
    """
    简化版：移除未闭合的HTML标签及其后面的内容

    Args:
        text (str): 需要处理的文本

    Returns:
        str: 处理后的文本
    """
    # 使用栈来跟踪未闭合的标签
    tag_stack = []
    result = []
    i = 0

    while i < len(text):
        if text[i] == "<":
            # 找到标签的结束位置
            tag_end = text.find(">", i)
            if tag_end == -1:
                # 未找到结束的>，这是一个不完整的标签，移除它及其后面所有内容
                break

            tag_content = text[i : tag_end + 1]
            result.append(tag_content)

            # 解析标签
            if tag_content.startswith("</"):
                # 结束标签
                tag_name = tag_content[2:-1].strip().split()[0]
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
            elif tag_content.endswith("/>"):
                # 自闭合标签
                pass
            else:
                # 开始标签
                tag_name = tag_content[1:-1].strip().split()[0]
                # 不将自闭合标签放入栈中
                if tag_name.lower() not in [
                    "img",
                    "br",
                    "hr",
                    "input",
                    "meta",
                    "link",
                    "area",
                    "base",
                    "col",
                    "embed",
                    "source",
                    "track",
                    "wbr",
                ]:
                    tag_stack.append(tag_name)

            i = tag_end + 1
        else:
            result.append(text[i])
            i += 1

    # 如果还有未闭合的标签，我们需要找到导致问题的标签并截断
    if tag_stack:
        # 找到文本中最后一个未闭合标签的开始位置
        for j in range(len(result) - 1, -1, -1):
            if (
                isinstance(result[j], str)
                and result[j].startswith("<")
                and not result[j].startswith("</")
                and not result[j].endswith("/>")
            ):
                tag_name = result[j][1:-1].strip().split()[0]
                if tag_name in tag_stack:
                    # 截断到这个标签之前
                    return "".join(result[:j])

    return "".join(result)


def clean_html_content(text):
    """
    清理HTML内容，移除未闭合的标签

    Args:
        text (str): 需要清理的文本

    Returns:
        str: 清理后的文本
    """
    # 如果有未闭合的HTML标签，移除该标签及其后面所有内容
    return remove_incomplete_html_tags_simple(text)
