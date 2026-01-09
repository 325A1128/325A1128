import streamlit as st

from random import randint,shuffle

#プログラムが再実行されたときにリセットされたくない変数たち
if 'page' not in st.session_state:
    st.session_state.page = 'home' #ページ
    st.session_state.cnt = 0 #正解数
    st.session_state.juu = 0 #10進数の整数
    st.session_state.mon = 1 #今が何問目か
    st.session_state.seigo = '' #正誤判定
    st.session_state.sentakushi = [] #選択肢を保持する
    
#基数変換して文字列で返すプログラム
def henkan(juu,hen):
    if juu == 0:
        return '0'
    chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    ret = '' 
    while juu > 0:
        ret = chars[int(juu % hen)] + ret
        juu = int(juu / hen)
    return ret

#正誤判定プログラム
def seigo(but):
    if but == st.session_state.juu:
        st.session_state.cnt += 1
        st.session_state.seigo = '〇正解'
    else:
        st.session_state.seigo = '✕不正解'

#問題作成プログラム
def mondai():
    #1問目→2問目→3問目で出題される数字の範囲を変える
    nanido = {1: (1,15),2: (16,63),3: (64,127)}
    low,high = nanido[st.session_state.mon]
    st.session_state.juu = randint(low,high)
    #選択肢のリスト[正解,不正解,不正解,不正解]
    sentaku = [st.session_state.juu,
               st.session_state.juu+1,
               st.session_state.juu-1,
               st.session_state.juu+2]
    #リストの中をシャッフルして正解のボタンの位置を変える
    shuffle(sentaku)
    st.session_state.sentakushi = sentaku
        
#ホーム画面
if st.session_state.page == 'home':
    st.title('基数変換問題')
    #問題ボタン
    if st.button('10➡2'):
        st.session_state.cnt = 0
        st.session_state.mon = 1
        mondai()
        st.session_state.henkan = 2
        st.session_state.page = 'p1'
        st.rerun()
    if st.button('10➡8'):
        st.session_state.cnt = 0
        st.session_state.mon = 1
        mondai()
        st.session_state.henkan = 8
        st.session_state.page = 'p1'
        st.rerun()
    if st.button('10➡16'):
        st.session_state.cnt = 0
        st.session_state.mon = 1
        mondai()
        st.session_state.henkan = 16
        st.session_state.page = 'p1'
        st.rerun()
    if st.button('2➡10'):
        st.session_state.cnt = 0
        st.session_state.mon = 1
        mondai()
        st.session_state.henkan = 2
        st.session_state.page = 'p2'
        st.rerun()
    if st.button('8➡10'):
        st.session_state.cnt = 0
        st.session_state.mon = 1
        mondai()
        st.session_state.henkan = 8
        st.session_state.page = 'p2'
        st.rerun()
    if st.button('16➡10'):
        st.session_state.cnt = 0
        st.session_state.mon = 1
        mondai()
        st.session_state.henkan = 16
        st.session_state.page = 'p2'
        st.rerun()
        
#10→nの問題ページ
elif st.session_state.page == 'p1':
    st.title(st.session_state.juu)
    
    for n in st.session_state.sentakushi:
        if st.button(henkan(n,st.session_state.henkan),key=f'p1{n}'):
            if n == st.session_state.juu:
                st.session_state.seigo = '〇正解'
                st.session_state.cnt += 1
            else:
                st.session_state.seigo = '✕不正解'
            st.session_state.page = 'p1_ans'
            st.rerun()

#n→10の問題ページ
elif st.session_state.page == 'p2':
    st.title(henkan(st.session_state.juu,st.session_state.henkan))
    
    for n in st.session_state.sentakushi:
        if st.button(str(n),key=f'p2{n}'):
            if n == st.session_state.juu:
                st.session_state.seigo = '〇正解'
                st.session_state.cnt += 1
            else:
                st.session_state.seigo = '✕不正解'
            st.session_state.page = 'p2_ans'
            st.rerun()

#10→nの答えページ
elif st.session_state.page == 'p1_ans':
    st.title(st.session_state.seigo)
    st.write(f'10進数:{st.session_state.juu}')
    st.write('↓')
    st.write(f'{st.session_state.henkan}進数:{henkan(st.session_state.juu,2)}')
    #三問目なら結果ページに飛ばす
    if st.session_state.mon < 3:
        if st.button('次の問題へ'):
            st.session_state.mon += 1
            mondai()
            st.session_state.page = 'p1'
    else:
        if st.button('結果'):
            st.session_state.page = 'p3'
    st.rerun()
  
#n→10の答えページ          
elif st.session_state.page == 'p2_ans':
    st.title(st.session_state.seigo)
    st.write(f'{st.session_state.henkan}進数:{henkan(st.session_state.juu,st.session_state.henkan)}')
    st.write('↓')
    st.write(f'10進数:{st.session_state.juu}')
    if st.session_state.mon < 3:
        if st.button('次の問題へ'):
            st.session_state.mon += 1
            mondai()
            st.session_state.page = 'p2'
    else:
        if st.button('結果'):
            st.session_state.page = 'p3'
    st.rerun()
            
#結果ページ
elif st.session_state.page == 'p3':
    st.title('結果')
    st.write(f'{st.session_state.cnt}/3問正解')
    if st.button('ホームに戻る'):
        st.session_state.page = 'home'
        st.rerun()