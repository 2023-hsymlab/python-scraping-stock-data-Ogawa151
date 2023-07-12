import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta

def main():
    # Streamlit が対応している任意のオブジェクトを可視化する (ここでは文字列)
    df = pd.read_csv('stock_trade_data.csv', header=0)

    today = datetime.datetime.now()
    st.write("今日は" + str(today.year), '年 ', str(today.month), '月 ', str(today.day), '日')

    with st.form("my_form", clear_on_submit=False):
        code = st.text_input('証券コード')
        buy_or_sell = st.radio('売買', ('買', '売'), horizontal=True)
        amount = st.text_input('株数(100単位)')
        #series = st.selectbox(label='初めて出現したシリーズ', options=[f'ドラクエ{i}' for i in range(1, 13)])
        submitted = st.form_submit_button("取引登録")

    filepath = 'stock_trade_data0.csv'
    if submitted:
        if buy_or_sell == '買':
            bs_tf = 0
        else:
            bs_tf = 1
        with open(filepath, mode='a') as f:
            f.write('\n' + str(today.date()) + ',' + str(code) + ',' + str(bs_tf) + ',' + str(amount))
        df0 = pd.read_csv('stock_trade_data0.csv', header=0)
        st.table(df0)

    #print(df)

def main0():
    st.title('Application title')# タイトル
    st.header('Header')# ヘッダ
    st.text('Some text')# 純粋なテキスト
    st.subheader('Sub header')# サブレベルヘッダ
    st.markdown('**Markdown is available **')# マークダウンテキスト
    st.latex(r'\bar{X} = \frac{1}{N} \sum_{n=1}^{N} x_i')# LaTeX テキスト
    st.code('print(\'Hello, World!\')')# コードスニペット
    st.error('Error message')# エラーメッセージ
    st.warning('Warning message')# 警告メッセージ
    st.info('Information message')# 情報メッセージ
    st.success('Success message')# 成功メッセージ
    st.exception(Exception('Oops!'))# 例外の出力
    # 辞書の出力
    d = {
        'foo': 'bar',
        'users': [
            'alice',
            'bob',
        ],
    }
    st.json(d)


if __name__ == '__main__':
    main()