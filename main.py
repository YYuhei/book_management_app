import streamlit as st
from streamlit_option_menu import option_menu
import requests
import crud
import streamlit_authenticator as stauth

# ログイン画面
users = crud.select_all_users()
names = [user[1] for user in users]
usernames = [user[2] for user in users]
hashed_passwords = [user[3] for user in users]

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "book_app",
    "asdf;lkj",
    cookie_expiry_days=1)
name, authentication_status, username = authenticator.login("ログイン", "main")

if authentication_status == False:
    st.error("UsernameまたはPasswordが一致していません")

if authentication_status == None:
    st.warning("UsernameとPasswordを入力してください")
    st.write("※ゲストアカウントはこちら")
    st.write("Username：gest , Password：12345")

if authentication_status:
    # 最終ログイン日時を更新
    crud.update_lastlogindate(name)
    # admin=1:管理者、admin=0:一般
    admin = crud.select_admin_users(name)

    st.header('書籍貸出アプリ')
    # サイドバー設定
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"ようこそ {name} さん")
    with st.sidebar:
        if admin == 1:  
            selected = option_menu(
                "メニュー", 
                ["閲覧", "書籍登録", "書籍管理"],
                icons=['book', 'pencil-square', 'wrench'],
                menu_icon="app-indicator", default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        if admin == 0:
            selected = option_menu(
                "メニュー", 
                ["閲覧"],
                icons=['book'],
                menu_icon="app-indicator", default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

    if selected == "閲覧":
        crud.read_booklist("read", name)

    if selected == "書籍登録":
        isbn = st.text_input('ISBNコードを入力してください')        
        if isbn != '':
            try:
                # GoogleBooksにAPIを投げる(1,000回/日まで可能)
                result = requests.get("https://www.googleapis.com/books/v1/volumes?country=JP&q=isbn:"+isbn)
                # 返却されたJSONを辞書型に変換
                data = result.json()
                # 表示項目の設定(存在しない項目は"-"で表示)
                if "title" in data["items"][0]["volumeInfo"]:
                    title = data["items"][0]["volumeInfo"]["title"]
                else:
                    title = "-"
                if "authors" in data["items"][0]["volumeInfo"]:
                    authors = data["items"][0]["volumeInfo"]["authors"][0]
                else:
                    authors = "-"
                if "publishedDate" in data["items"][0]["volumeInfo"]:
                    publishedDate = data["items"][0]["volumeInfo"]["publishedDate"]
                else:
                    publishedDate = "-"
                if "pageCount" in data["items"][0]["volumeInfo"]:
                    pageCount = str(data["items"][0]["volumeInfo"]["pageCount"])
                else:
                    pageCount = "-"
                if "description" in data["items"][0]["volumeInfo"]:
                    description = data["items"][0]["volumeInfo"]["description"]
                else:
                    description = "-"
                if "imageLinks" in data["items"][0]["volumeInfo"]:
                    if "thumbnail" in data["items"][0]["volumeInfo"]["imageLinks"]:
                        thumbnail = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
                else:
                    thumbnail = "http://design-ec.com/d/e_others_50/l_e_others_501.png"

                #書籍情報を表示する。
                if data["items"][0]["id"]!="9gpcewAACAAJ":
                    st.write("タイトル："+title)
                    st.write("著者："+authors)
                    st.write("出版日："+publishedDate)
                    st.write("ページ数："+pageCount)
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write("要約："+description)
                    with col2:
                        st.image(thumbnail, width=200)
                    regist = st.button("本を登録する")
                    if regist:
                        crud.insert_booklist(
                            title,
                            authors,
                            publishedDate,
                            pageCount,
                            description,
                            thumbnail,
                            "返却済",
                            "-",
                            "-",
                            "-",
                            isbn,
                        )
                        st.success("本を登録しました："+title)
            except:
                st.write("通信エラー")

    if selected == "書籍管理":
        crud.read_booklist("control", name)
