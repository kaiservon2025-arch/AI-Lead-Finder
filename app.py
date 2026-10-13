import streamlit as st
import pandas as pd


from database.database import (
    init_database,
    get_companies,
    add_company
)


from database.email_database import (
    init_email_database,
    add_template,
    get_templates,
    get_template_by_id
)

from search.search_engine import (
    search_company
)


from search.keyword_match import (
    match_keywords
)
from search.company_filter import (
    filter_company_results
)


# =====================
# 初始化数据库
# =====================

init_database()

init_email_database()





# =====================
# 页面配置
# =====================


st.set_page_config(

    page_title="AI Lead Finder",

    layout="wide"

)





# =====================
# CSS
# =====================


st.markdown(

"""
<style>


html,
body,
[class*="css"] {


    font-family:

    "Microsoft YaHei",
    "Inter",
    sans-serif;


}



.main {


    background:#F5F7FB;


}




h1 {


    font-size:26px !important;

    font-weight:700 !important;

    color:#0B1F3A;


}



h2 {


    font-size:22px !important;


}




/* =====================
Sidebar
===================== */



section[data-testid="stSidebar"] {


    width:280px !important;


}




[data-testid="stSidebar"] {


    background:#081B33;


}




[data-testid="stSidebar"] * {


    color:white;


}




[data-testid="stSidebar"] h2 {


    font-size:26px !important;


    font-weight:800 !important;


}




[data-testid="stSidebar"] p {


    font-size:14px;


    opacity:0.7;


}






/* =====================
菜单
===================== */



.stRadio {


    margin-top:35px;


}




.stRadio label {


    font-size:19px !important;


    font-weight:550 !important;


    padding:12px 16px;


    margin-bottom:8px;


    border-radius:8px;


    background:transparent;


    position:relative;


}




.stRadio label:hover {


    background:

    rgba(59,130,246,0.15);


}





.stRadio input {


    display:none;


}






/* =====================
卡片
===================== */


.metric-box {


    background:white;


    padding:22px;


    border-radius:14px;


    box-shadow:

    0 4px 12px rgba(0,0,0,0.08);


}



.metric-box h4 {


    color:#64748B;


    font-size:15px;


}




.metric-box h1 {


    font-size:32px !important;


}






/* =====================
按钮
===================== */


.stButton button {


    height:42px;


    border-radius:8px;


    background:#2563EB;


    color:white;


    font-size:15px;


    font-weight:600;


    border:none;


}




.stButton button:hover {


    background:#1D4ED8;


}




</style>

""",

unsafe_allow_html=True

)






# =====================
# 左侧菜单
# =====================


with st.sidebar:



    st.markdown(

"""
<h2>
AI Lead Finder
</h2>


<p>
Enterprise AI Platform
</p>


<hr>

""",

unsafe_allow_html=True

)



    menu = st.radio(

        "",

        [

            "工作台",

            "客户搜索",

            "企业列表",

            "邮件模板"

        ]

    )



    st.markdown(

"""
<br>

<div style="
font-size:13px;
opacity:0.6;
">

Version 0.1

</div>

""",

unsafe_allow_html=True

)
# =====================
# 工作台
# =====================


if menu == "工作台":


    st.title(
        "工作台"
    )



    companies = get_companies()



    c1,c2,c3 = st.columns(3)



    with c1:


        st.markdown(

f"""

<div class="metric-box">


<h4>企业数量</h4>


<h1>{len(companies)}</h1>


</div>

""",

unsafe_allow_html=True

)




    with c2:


        st.markdown(

"""

<div class="metric-box">


<h4>待联系客户</h4>


<h1>0</h1>


</div>

""",

unsafe_allow_html=True

)




    with c3:


        st.markdown(

"""

<div class="metric-box">


<h4>邮件发送</h4>


<h1>0</h1>


</div>

""",

unsafe_allow_html=True

)




    st.divider()



    st.subheader(

        "最近搜索"

    )



    if companies:


        for company in companies[:5]:

            st.write(

                company[1]

            )


    else:


        st.info(

            "暂无搜索记录"

        )








# =====================
# 客户搜索
# =====================


# =====================
# 客户搜索
# =====================

elif menu == "客户搜索":

    st.title(
        "客户搜索"
    )

    keyword = st.text_input(
        "关键词"
    )

    country = st.text_input(
        "国家"
    )

    region = st.text_input(
        "地区"
    )

    industry = st.text_input(
        "行业"
    )


    if st.button(
        "开始搜索"
    ):

        if not keyword:

            st.warning(
                "请输入关键词"
            )

        else:

            with st.spinner(
                "正在搜索企业..."
            ):

                results = search_company(
                    keyword=keyword,
                    country=country,
                    region=region,
                    industry=industry
                )


                results = filter_company_results(
                    results
                )


                save_count = 0


                for item in results:

                    text = (
                        item.get(
                            "title",
                            ""
                        )
                        +
                        " "
                        +
                        item.get(
                            "content",
                            ""
                        )
                    )


                    match_result = match_keywords(
                        text,
                        keyword
                    )


                    if not match_result["matched"]:

                        continue


                    company_data = {

                        "company_name":
                            item.get(
                                "company_name",
                                item.get(
                                    "title",
                                    ""
                                )
                            ),

                        "country":
                            country,

                        "region":
                            region,

                        "industry":
                            industry,

                        "matched_keywords":
                            ",".join(
                                match_result[
                                    "matched_keywords"
                                ]
                            ),

                        "matched_content":
                            text,

                        "source_url":
                            item.get(
                                "url",
                                ""
                            ),

                        "source_type":
                            "关键词搜索"

                    }


                    add_company(
                        company_data
                    )


                    save_count += 1



            st.success(
                f"搜索完成，新增 {save_count} 家企业"
            )


            st.subheader(
                "搜索结果"
            )


            for item in results:

                st.write(
                    "企业:",
                    item.get(
                        "company_name",
                        item.get(
                            "title",
                            ""
                        )
                    )
                )


                st.write(
                    "来源:",
                    item.get(
                        "url",
                        ""
                    )
                )


                st.divider()







# =====================
# 企业列表
# =====================


elif menu == "企业列表":


    st.title(

        "企业列表"

    )



    companies = get_companies()



    if companies:


        columns = [

            "ID",

            "企业名称",

            "国家",

            "地区",

            "行业",

            "命中关键词",

            "命中内容",

            "联系人",

            "职位",

            "邮箱",

            "电话",

            "来源网址",

            "来源类型",

            "selected",

            "邮件状态",

            "创建时间"

        ]



        df = pd.DataFrame(

            companies,

            columns=columns

        )



        df.insert(

            0,

            "选择",

            False

        )



        show_columns = [

            "选择",

            "ID",

            "企业名称",

            "国家",

            "地区",

            "行业",

            "命中关键词",

            "联系人",

            "职位",

            "邮箱",

            "电话",

            "来源网址",

            "邮件状态"

        ]



        show_df = df[show_columns]



        edited_df = st.data_editor(

            show_df,

            use_container_width=True,

            hide_index=True,


            column_config={


                "选择":

                    st.column_config.CheckboxColumn(

                        "选择企业",

                        help="选择需要发送邮件的企业"

                    ),


                "企业名称":

                    st.column_config.TextColumn(

                        width="large"

                    )

            }

        )



        selected_rows = edited_df[

            edited_df["选择"] == True

        ]



        st.info(

            f"已选择 {len(selected_rows)} 家企业"

        )



        col1,col2 = st.columns(2)



        with col1:


            if st.button(

                "批量发送邮件",

                use_container_width=True

            ):



                if len(selected_rows) > 0:


                    st.success(

                        f"准备发送给 {len(selected_rows)} 家企业"

                    )


                else:


                    st.warning(

                        "请先选择企业"

                    )




        with col2:


            st.button(

                "导出 Excel",

                use_container_width=True

            )



    else:


        st.info(

            "暂无企业数据"

        )

# =====================
# 邮件模板
# =====================

elif menu == "邮件模板":

    st.title("邮件模板")

    st.caption(
        "管理销售邮件模板，支持企业信息变量替换。"
    )


    # =====================
    # 新建模板
    # =====================

    st.subheader("新建邮件模板")


    template_name = st.text_input(
        "模板名称",
        key="template_name_input"
    )


    subject = st.text_input(
        "邮件主题",
        key="template_subject_input"
    )


    content = st.text_area(
        "邮件正文",
        height=250,
        key="template_content_input",
        placeholder="""您好 {{联系人姓名}}

我们了解到 {{企业名称}}。

希望与贵公司在 {{行业}} 领域交流合作。

联系方式：
{{邮箱}}"""
    )



    st.markdown(
        """
### 可用变量

邮件发送时可以自动替换：

- `{{企业名称}}`
- `{{联系人姓名}}`
- `{{邮箱}}`
- `{{职位}}`
- `{{国家}}`
- `{{地区}}`
- `{{行业}}`


示例：

模板：

您好 {{联系人姓名}}

希望与 {{企业名称}} 在 {{行业}} 领域合作。


替换后：

您好 Michael

希望与 ABC GmbH 在工业自动化领域合作。
        """
    )



    # =====================
    # 保存模板
    # =====================

    if st.button(
        "保存模板",
        key="save_template_button"
    ):


        if not template_name.strip():

            st.warning(
                "请输入模板名称"
            )


        elif not subject.strip():

            st.warning(
                "请输入邮件主题"
            )


        elif not content.strip():

            st.warning(
                "请输入邮件正文"
            )


        else:


            add_template(

                template_name.strip(),

                subject.strip(),

                content.strip()

            )


            st.success(
                "模板保存成功"
            )


            st.rerun()



    st.divider()



    # =====================
    # 已保存模板
    # =====================


    st.subheader(
        "已有模板"
    )


    templates = get_templates()



    if templates:


        template_names = []


        template_dict = {}



        for item in templates:


            template_id = item[0]

            name = item[1]


            template_names.append(name)


            template_dict[name] = template_id




        selected_template = st.selectbox(

            "选择模板",

            template_names

        )



        template_id = template_dict[
            selected_template
        ]



        template = get_template_by_id(

            template_id

        )



        st.write(
            "模板名称"
        )

        st.info(
            template[1]
        )


        st.write(
            "邮件主题"
        )

        st.code(
            template[2]
        )


        st.write(
            "邮件正文"
        )

        st.text_area(

            "内容",

            template[3],

            height=200,

            disabled=True

        )



        st.divider()



        # =====================
        # 变量预览
        # =====================


        st.subheader(
            "变量替换预览"
        )


        preview = template[3]



        variables = {


            "{{企业名称}}":
                "ABC GmbH",


            "{{联系人姓名}}":
                "Michael",


            "{{邮箱}}":
                "contact@abc.com",


            "{{职位}}":
                "采购经理",


            "{{国家}}":
                "德国",


            "{{地区}}":
                "慕尼黑",


            "{{行业}}":
                "工业自动化"

        }



        for key,value in variables.items():

            preview = preview.replace(

                key,

                value

            )



        st.text_area(

            "预览结果",

            preview,

            height=200,

            disabled=True

        )



    else:


        st.info(
            "暂无邮件模板，请先创建。"
        )