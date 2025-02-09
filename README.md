# 書籍貸出アプリ

## 説明
PythonのフレームワークStreamlitを用いた社内向けの書籍貸出アプリです。  
ゲストアカウントからアプリが使用できます。  
ログイン機能、書籍閲覧・検索・登録・削除機能をCRUD処理で実装。  
データベース自体は小規模なのでDBファイルを作成してSQLite3で書込みしています。  
アプリのデプロイはStreamlit Cloudを使用しています。

## 仕様
＜ログイン画面＞  
・UsernameとPasswordを入力、loginボタンでログイン可（DBにないユーザーはエラー）  

＜書籍管理画面＞  
閲覧メニュー：DBにある書籍の一覧をデータテーブルで表示。  
　　　　　　　行選択すると書籍の情報と貸出状況が表示される。  
　　　　　　　貸出状況が返却済の本は借りることができる。  
　　　　　　　借りてる人がログインユーザーであれば返却できる。  
書籍登録メニュー：ISBNコードを入力するとGoogleBooksAPIから書籍情報をJSONで取得。  
　　　　　　　　　GoogleBooksAPIは1,000回/日まで取得可能。  
　　　　　　　　　登録ボタンで閲覧・書籍管理メニューのテーブルに登録される。  
書籍管理メニュー：DBにある書籍の一覧をデータテーブルで表示。  
　　　　　　　　　行選択すると書籍の情報と貸出状況が表示される。  
　　　　　　　　　削除ボタンでDBから書籍情報を削除する。

## 参考サイト
Streamlit公式  
https://streamlit.io/

Streamlitの使い方の細かいところ  
https://zenn.dev/ohtaman/articles/streamlit_tips

How to Add a User Authentication Service (Login Form) in Streamlit   
https://www.youtube.com/watch?v=JoFGrSRj4X4
