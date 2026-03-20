6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git config --global user.email "jyslove05@gmail.com"

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git config --global user.name "yesung05"

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git list
git: 'list' is not a git command. See 'git --help'.

The most similar commands are
        bisect
        rev-list

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ dir
app.py  pandas_analysis.py  requirements.txt  venv

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ wdir
bash: wdir: command not found

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ ls
app.py  pandas_analysis.py  requirements.txt  venv/

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ .git init
bash: .git: command not found

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git init
Reinitialized existing Git repository in C:/Users/6-112/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis/.git/

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git init
Reinitialized existing Git repository in C:/Users/6-112/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis/.git/

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git add .

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git commit -m 'gitignore 추가'
[master 86dc013] gitignore 추가
 1 file changed, 13 insertions(+)
 create mode 100644 .gitignore

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git push
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 418 bytes | 418.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/yesung05/BigdataAnalysis
   bd8f20f..86dc013  master -> master

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ git diff

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ grep data app.py
    data = {
    st.session_state.df = pd.DataFrame(data)
    new_data = {
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
st.dataframe(st.session_state.df, use_container_width=True)

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ touch helloworld.py

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ cat app.py | head -5
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="빅데이터 분석 프로젝트", page_icon="📊")

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ cd ..

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성 (main)
$ cd BigdataAnalysis/

6-112@112-15 MINGW64 ~/Desktop/빅데이터분석프로그래밍/조예성/BigdataAnalysis (master)
$ mv helloworld.py readme.md
