import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import sqlite3
import datetime

def read_booklist(menu, name):
    user_name = select_username_users(name)
    id = []
    title = []
    authors = []
    publishedDate = []
    pageCount = []
    description = []
    thumbnail = []
    status = []
    borrower = []
    checkoutdate = []
    returndate = []
    isbn = []
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM booklist")
    for row in cur:
        id.append(row[0])
        title.append(row[1])
        authors.append(row[2])
        publishedDate.append(row[3])
        pageCount.append(row[4])
        description.append(row[5])
        thumbnail.append(row[6])
        status.append(row[7])
        borrower.append(row[8])
        checkoutdate.append(row[9])
        returndate.append(row[10])
        isbn.append(row[11])
    con.close()
    df = pd.DataFrame(
        {
            'No': id,
            'タイトル': title,
            '著者': authors,
            '貸出状況': status,
            '借りてる人': borrower,
            '貸出日': checkoutdate,
            '返却日': returndate,
            '出版日': publishedDate,
            'ページ数': pageCount,
            '要約': description,
            'サムネイル': thumbnail,
            'ISBNコード': isbn
        }
    )
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_selection(selection_mode="single")
    gridOptions = gb.build()
    data = AgGrid(
        df,
        # theme="streamlit",
        # fit_columns_on_grid_load=True,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.SELECTION_CHANGED
    )
    if len(data["selected_rows"]) > 0:
        st.write('タイトル：'+data["selected_rows"][0]['タイトル'])
        st.write('貸出状況：'+data["selected_rows"][0]['貸出状況']+'　借りてる人：'+data["selected_rows"][0]['借りてる人']+ '　貸出日：'+data["selected_rows"][0]['貸出日']+ '　返却日：'+data["selected_rows"][0]['返却日'])
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write('要約：'+data["selected_rows"][0]['要約'])
        with col2:
            st.image(data["selected_rows"][0]['サムネイル'], width=200)
        if menu == "read":
            if data["selected_rows"][0]['貸出状況'] == "返却済":
                borrowbook = st.button("本を借りる")
                if borrowbook:
                    update_status_borrow(data["selected_rows"][0]['ISBNコード'], user_name)
                    st.success("本を借りました："+data["selected_rows"][0]['タイトル'])
            elif data["selected_rows"][0]['借りてる人'] == user_name:
                returnbook = st.button("本を返却する")
                if returnbook:
                    update_status_return(data["selected_rows"][0]['ISBNコード'])
                    st.success("本を返却しました："+data["selected_rows"][0]['タイトル'])
        if menu == "control":
            deletebook = st.button("本を削除する")
            if deletebook:
                delete_booklist(data["selected_rows"][0]['ISBNコード'])
                st.success("本を削除しました："+data["selected_rows"][0]['タイトル'])

def insert_booklist(title, authors, publishedDate, pageCount, description, thumbnail, status, borrower, checkoutdate, returndate, isbn):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    sql = 'INSERT INTO booklist (title, authors, publishedDate, pageCount, description, thumbnail, status, borrower,  checkoutdate, returndate, isbn) values (?,?,?,?,?,?,?,?,?,?,?)'
    data = [title, authors, publishedDate, pageCount, description, thumbnail, status, borrower, checkoutdate, returndate, isbn]
    cur.execute(sql, data)
    con.commit()
    con.close()

def delete_booklist(isbn):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    sql = 'DELETE FROM booklist WHERE isbn=?'
    data = [isbn]
    cur.execute(sql, data)
    con.commit()
    con.close()

def update_status_borrow(isbn, borrower):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    today = datetime.date.today()
    sql = 'UPDATE booklist SET status="貸出中", checkoutdate=? , returndate="-", borrower=? WHERE isbn=?'
    data = [today, borrower, isbn]
    cur.execute(sql, data)
    con.commit()
    con.close()

def update_status_return(isbn):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    today = datetime.date.today()
    sql = 'UPDATE booklist SET status="返却済", checkoutdate="-", returndate=?, borrower="-" WHERE isbn=?'
    data = [today, isbn]
    cur.execute(sql, data)
    con.commit()
    con.close()

def insert_users(name, username, password, lastlogindate, admin):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    sql = 'INSERT INTO users (name, username, password, lastlogindate, admin) values (?,?,?,?,?)'
    data = [name, username, password, lastlogindate, admin]
    cur.execute(sql, data)
    con.commit()
    con.close()

def select_all_users():
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    con.close()
    return users

def select_admin_users(name):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    sql = "SELECT admin FROM users WHERE name=?"
    data = [name]
    cur.execute(sql, data)
    admin = cur.fetchone()
    con.close()
    return admin[0]

def select_username_users(name):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    sql = "SELECT username FROM users WHERE name=?"
    data = [name]
    cur.execute(sql, data)
    username = cur.fetchone()
    con.close()
    return username[0]

def delete_user(name):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    sql = 'DELETE FROM users WHERE name=?'
    data = [name]
    cur.execute(sql, data)
    con.commit()
    con.close()

def update_lastlogindate(name):
    con = sqlite3.connect('./book.db')
    cur = con.cursor()
    dt_now = datetime.datetime.now()
    sql = 'UPDATE users SET lastlogindate=? WHERE name=?'
    data = [dt_now.strftime('%Y-%m-%d %H:%M:%S'), name]
    cur.execute(sql, data)
    con.commit()
    con.close()