import sqlite3
import os
from datetime import datetime



DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "leads.db"
)



def get_connection():

    return sqlite3.connect(
        DB_PATH
    )





# =====================
# 初始化数据库
# =====================


def init_database():

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (

            id INTEGER PRIMARY KEY AUTOINCREMENT,


            company_name TEXT,

            country TEXT,

            region TEXT,

            industry TEXT,


            matched_keywords TEXT,

            matched_content TEXT,


            contact_name TEXT,

            contact_position TEXT,


            email TEXT,

            phone TEXT,


            source_url TEXT,

            source_type TEXT,


            selected INTEGER DEFAULT 0,


            email_status TEXT DEFAULT '未发送',


            created_time TEXT

        )
        """
    )



    # =====================
    # 自动检查字段
    # =====================


    cursor.execute(
        "PRAGMA table_info(companies)"
    )


    columns = [

        row[1]

        for row in cursor.fetchall()

    ]



    if "selected" not in columns:


        cursor.execute(

            """
            ALTER TABLE companies
            ADD COLUMN selected INTEGER DEFAULT 0
            """

        )



    conn.commit()

    conn.close()






# =====================
# 添加企业
# =====================


def add_company(data):


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        INSERT INTO companies (

            company_name,

            country,

            region,

            industry,


            matched_keywords,

            matched_content,


            contact_name,

            contact_position,


            email,

            phone,


            source_url,

            source_type,


            selected,

            email_status,


            created_time

        )


        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,


        (

            data.get(
                "company_name",
                ""
            ),


            data.get(
                "country",
                ""
            ),


            data.get(
                "region",
                ""
            ),


            data.get(
                "industry",
                ""
            ),


            data.get(
                "matched_keywords",
                ""
            ),


            data.get(
                "matched_content",
                ""
            ),


            data.get(
                "contact_name",
                ""
            ),


            data.get(
                "contact_position",
                ""
            ),


            data.get(
                "email",
                ""
            ),


            data.get(
                "phone",
                ""
            ),


            data.get(
                "source_url",
                ""
            ),


            data.get(
                "source_type",
                ""
            ),


            0,


            data.get(
                "email_status",
                "未发送"
            ),



            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )



    conn.commit()

    conn.close()







# =====================
# 获取企业列表
# =====================


def get_companies():


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        SELECT *

        FROM companies

        ORDER BY id DESC

        """

    )



    rows = cursor.fetchall()



    conn.close()



    return rows






# =====================
# 根据ID获取企业
# =====================


def get_company_by_id(company_id):


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        SELECT *

        FROM companies

        WHERE id=?

        """,

        (

            company_id,

        )

    )



    row = cursor.fetchone()



    conn.close()



    return row






# =====================
# 更新选择状态
# =====================


def update_selected(

    company_id,

    selected

):


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        UPDATE companies

        SET selected=?

        WHERE id=?

        """,

        (

            selected,

            company_id

        )

    )



    conn.commit()

    conn.close()





# =====================
# 测试
# =====================


if __name__ == "__main__":


    init_database()


    print(

        "数据库初始化完成"

    )