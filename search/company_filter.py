import re
from urllib.parse import urlparse


# 明显非企业页面关键词
BLOCK_KEYWORDS = [
    "dictionary",
    "wikipedia",
    "statista",
    "statistics",
    "union",
    "verband",
    "verein",
    "style",
    "design",
    "blog",
    "news",
    "article",
    "definition",
    "meaning",
    "what is",
    "what-is",
    "learn",
    "academy",
    "forum",
    "f6s",
    "aeroleads",
    "investopedia",
    "cambridge",
    "government",
    "ministry",
    "database",
]


# 非企业域名
BAD_DOMAINS = [
    "google.",
    "bing.",
    "duckduckgo.",
    "yahoo.",
    "searx",
]


# 企业特征词
COMPANY_WORDS = [
    "gmbh",
    "ag",
    "kg",
    "inc",
    "ltd",
    "llc",
    "corp",
    "industrial",
    "automation",
    "technik",
    "technologies",
    "systems",
    "solutions",
    "engineering",
    "manufacturing",
    "factory",
    "software",
]


def clean_company_name(title):
    """
    清理搜索标题
    """

    if not title:
        return ""


    # 去掉 "| 后面的网页标题"
    title = re.sub(
        r"\s*\|.*$",
        "",
        title
    )


    # 去掉 "- 后面的描述"
    title = re.sub(
        r"\s+-\s+.*$",
        "",
        title
    )


    return title.strip()



def is_valid_company_name(
        title,
        url,
        description=""
):
    """
    判断搜索结果是否是真实企业
    """

    if not title or not url:
        return False


    text = (
        title
        + " "
        + url
        + " "
        + description
    ).lower()



    # 黑名单过滤

    for keyword in BLOCK_KEYWORDS:

        if keyword in text:
            return False



    # 域名检查

    try:

        domain = urlparse(url).netloc.lower()


        if not domain:
            return False


        for bad in BAD_DOMAINS:

            if bad in domain:
                return False


    except:

        return False



    # 标题长度

    if len(title.strip()) < 5:
        return False



    # 企业评分

    score = 0


    for word in COMPANY_WORDS:

        if word in text:
            score += 1



    # 没有任何企业特征，过滤

    if score == 0:
        return False



    return True



def filter_company_results(results):
    """
    SearXNG结果过滤入口

    输入:
    [
        {
            title:"",
            url:"",
            description:""
        }
    ]

    返回:
    企业结果
    """


    filtered = []

    seen = set()



    for item in results:


        title = item.get(
            "title",
            ""
        )

        url = item.get(
            "url",
            ""
        )

        description = item.get(
            "description",
            ""
        )



        if not is_valid_company_name(
            title,
            url,
            description
        ):
            continue



        # URL去重

        if url in seen:
            continue


        seen.add(url)



        # 增加清洗后的公司名

        item["company_name"] = clean_company_name(
            title
        )


        filtered.append(item)



    return filtered