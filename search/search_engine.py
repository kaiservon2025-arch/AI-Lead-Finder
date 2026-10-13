import requests
from datetime import datetime

from search.company_filter import is_valid_company


SEARXNG_URL = "http://localhost:8080/search"



# =====================
# 构建搜索关键词
# =====================

def build_search_queries(
    keyword,
    country="",
    region="",
    industry=""
):

    location = " ".join(
        x for x in [
            country,
            region
        ]
        if x
    )


    queries = []


    if keyword:

        queries.append(
            f"{keyword} company {location}"
        )


        queries.append(
            f"{keyword} GmbH {location}"
        )


        queries.append(
            f"{keyword} manufacturer {location}"
        )


        queries.append(
            f"{keyword} supplier {location}"
        )


        if industry:

            queries.append(
                f"{industry} {keyword} company {location}"
            )


    return queries





# =====================
# 调用 SearXNG
# =====================

def search_searxng(query):

    try:

        response = requests.get(

            SEARXNG_URL,

            params={

                "q": query,

                "format": "json"

            },

            timeout=15

        )


        response.raise_for_status()


        data = response.json()


        return data.get(
            "results",
            []
        )


    except Exception as e:

        print(
            "SearXNG搜索失败:",
            e
        )

        return []






# =====================
# 企业搜索入口
# =====================

def search_company(
    keyword,
    country="",
    region="",
    industry=""
):


    queries = build_search_queries(

        keyword,

        country,

        region,

        industry

    )


    all_results = []


    # 去重缓存

    seen_urls = set()

    seen_names = set()



    for query in queries:


        results = search_searxng(

            query

        )



        for item in results:



            if not is_valid_company(item):

                continue



            company_name = item.get(

                "title",

                ""

            ).strip()



            url = item.get(

                "url",

                ""

            ).strip()



            if not company_name or not url:

                continue



            if url in seen_urls:

                continue



            if company_name in seen_names:

                continue



            seen_urls.add(url)

            seen_names.add(company_name)



            all_results.append(

                {


                    "company_name":

                        company_name,


                    "country":

                        country,


                    "region":

                        region,


                    "industry":

                        industry,


                    "title":

                        item.get(

                            "title",

                            ""

                        ),


                    "content":

                        item.get(

                            "content",

                            ""

                        ),


                    "url":

                        url,


                    "search_query":

                        query,


                    "created_time":

                        datetime.now().strftime(

                            "%Y-%m-%d %H:%M:%S"

                        )


                }

            )



    return all_results