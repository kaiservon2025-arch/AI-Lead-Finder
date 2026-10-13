from search.search_engine import search_company

from database.database import (
    init_database,
    add_company,
    get_companies
)


# =====================
# 初始化数据库
# =====================

init_database()


# =====================
# 搜索条件
# =====================

keyword = "industrial automation"

country = "Germany"

region = "Bavaria"

industry = "Manufacturing"



print("=" * 60)
print("开始搜索")
print("=" * 60)



# =====================
# 搜索
# =====================

results = search_company(

    keyword=keyword,

    country=country,

    region=region,

    industry=industry

)



print(
    "搜索结果:",
    len(results)
)



# =====================
# 保存企业
# =====================

save_count = 0


for item in results:


    company_name = item.get(
        "company_name",
        ""
    )


    if not company_name:

        continue



    company_data = {


        "company_name":

            company_name,


        "country":

            country,


        "region":

            region,


        "industry":

            industry,


        "matched_keywords":

            keyword,


        "matched_content":

            item.get(
                "content",
                ""
            ),


        "source_url":

            item.get(
                "url",
                ""
            ),


        "source_type":

            "SearXNG搜索"

    }



    add_company(

        company_data

    )


    save_count += 1


    print(
        "保存企业:",
        company_name
    )



print()

print(
    "保存完成:",
    save_count
)



# =====================
# 查看数据库
# =====================

print()

print("=" * 60)

print("数据库企业列表")

print("=" * 60)



companies = get_companies()



for company in companies:

    print(company)