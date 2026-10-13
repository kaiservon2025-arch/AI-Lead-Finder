import requests
import re

from bs4 import BeautifulSoup



def fetch_page(url):

    try:

        response = requests.get(

            url,

            timeout=10,

            headers={

                "User-Agent":
                    "Mozilla/5.0"

            }

        )


        response.raise_for_status()


        return response.text


    except Exception as e:

        print(
            "网页访问失败:",
            e
        )

        return ""





def extract_email(text):

    emails = re.findall(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text

    )


    for email in emails:

        if "example" not in email.lower():

            return email


    return ""





def extract_phone(text):

    phones = re.findall(

        r"(\+?\d[\d\s\-\/\(\)]{7,25}\d)",

        text

    )


    for phone in phones:


        clean_phone = " ".join(

            phone.split()

        )


        digits = re.sub(

            r"\D",

            "",

            clean_phone

        )


        if len(digits) >= 8 and len(digits) <= 15:

            return clean_phone



    return ""





def enrich_company(company):


    url = company.get(

        "url",

        ""

    )


    html = fetch_page(url)



    if not html:

        return {

            "contact_page": "",

            "email": "",

            "phone": "",

            "address": "",

            "career_page": ""

        }



    soup = BeautifulSoup(

        html,

        "html.parser"

    )


    text = soup.get_text(

        " "

    )



    return {


        "contact_page": "",


        "email":

            extract_email(text),


        "phone":

            extract_phone(text),


        "address": "",


        "career_page": ""

    }