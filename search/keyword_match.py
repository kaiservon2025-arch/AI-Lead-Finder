def match_keywords(
    text,
    keywords
):
    """
    关键词匹配

    输入：

    text:
    企业标题+内容

    keywords:
    用户输入关键词列表


    返回：

    {
        matched:
        True/False,

        matched_keywords:
        []
    }

    """


    if not text:

        return {
            "matched": False,
            "matched_keywords": []
        }



    if isinstance(keywords, str):

        keywords = [
            keywords
        ]



    matched_keywords = []



    text_lower = text.lower()



    for keyword in keywords:


        if not keyword:

            continue



        keyword_clean = keyword.strip()



        if not keyword_clean:

            continue



        if keyword_clean.lower() in text_lower:


            matched_keywords.append(
                keyword_clean
            )



    return {

        "matched":
            len(matched_keywords) > 0,


        "matched_keywords":
            matched_keywords
    }