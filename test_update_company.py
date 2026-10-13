from search.company_enricher import enrich_company

from database.update_company import update_company_info



company = {

    "url":

        "https://industrial.softing.com/de/index.html"

}



print("=" * 60)

print("开始企业信息补全")

print("=" * 60)



info = enrich_company(

    company

)



print(info)



print("=" * 60)

print("写入数据库")

print("=" * 60)



update_company_info(

    30,

    info

)


print("更新完成")