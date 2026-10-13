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
# 初始化邮件模板数据库
# =====================


def init_email_database():

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS email_templates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,


            template_name TEXT,


            subject TEXT,


            content TEXT,


            created_time TEXT

        )
        """
    )



    conn.commit()

    conn.close()






# =====================
# 添加模板
# =====================


def add_template(

    template_name,

    subject,

    content

):


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        INSERT INTO email_templates
        (

            template_name,

            subject,

            content,

            created_time

        )

        VALUES (?,?,?,?)

        """,

        (

            template_name,

            subject,

            content,

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )



    conn.commit()

    conn.close()






# =====================
# 获取全部模板
# =====================


def get_templates():


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        SELECT *

        FROM email_templates

        ORDER BY id DESC

        """

    )


    rows = cursor.fetchall()



    conn.close()



    return rows






# =====================
# 根据ID查询模板
# =====================


def get_template_by_id(

    template_id

):


    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(

        """
        SELECT *

        FROM email_templates

        WHERE id=?

        """,

        (

            template_id,

        )

    )



    row = cursor.fetchone()



    conn.close()



    return row






# =====================
# 测试
# =====================


if __name__ == "__main__":


    init_email_database()


    print(

        "邮件模板数据库初始化完成"

    )