from search.company_enricher import enrich_company


company = {

    "company_name":
        "Softing Industrial",

    "url":
        "https://industrial.softing.com"

}


result = enrich_company(company)


print(result)