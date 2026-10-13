import sqlite3


DB_PATH = "database/leads.db"



def update_company_info(

    company_id,

    info

):


    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()



    cursor.execute(

        """
        UPDATE companies

        SET

            email = ?,

            phone = ?

        WHERE id = ?

        """,

        (

            info.get(
                "email",
                ""
            ),

            info.get(
                "phone",
                ""
            ),

            company_id

        )

    )



    conn.commit()

    conn.close()