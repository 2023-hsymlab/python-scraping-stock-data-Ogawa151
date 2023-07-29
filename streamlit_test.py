import streamlit as st
import streamlit_option_menu
import pandas as pd
from pandas_datareader import data
import numpy as np
import datetime
from datetime import timedelta
import jpholiday
import sys

def main():
    with st.sidebar:
        selected = streamlit_option_menu.option_menu(menu_title=None,
            options=["Home", "株の売買", "現在の損益", "株価検索", "Chat", "Tag"],
            icons=["hours", "puzzle-fill", "envelope", "stats", "chat-dots", "tag-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "'0'!important", "background-color": "#ddeebb"},
                "icon": {"color": "#ff0000", "font-size": "15px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#ffccff"},
                "nav-link-selected": {"background-color": "#ffaaff"},
            }
        )

    st.title(f"サイドメニューで {selected} を選択")
    
    if selected == "Home":
        st.write("ほーむぺーじだぜ")
    
    elif selected == "株の売買":
        #st.title(f"サイドメニューで {selected} を選択")
        stock_trading()

    elif selected == "現在の損益":

        df = pd.read_csv('stock_trade_data0.csv', header=0)
        stock_pl(df, 10000000)

            
def stock_trading():
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
            f.write('\n' + str(today.date()) + ',' + str(bs_tf) + ',' + str(code) + ',' + str(amount))
        df0 = pd.read_csv('stock_trade_data0.csv', header=0)
        st.table(df0)

    #print(df)

#pl_done_tf = 0 #更新の必要がない時に「現在の損益」を押しても一回取得して計算したデータを表示するだけjにするやつ　保留
#pl_extime = datetime.datetime.now()

def stock_pl(df_purchase, hold_money): #売買日付、売か買か、売買した銘柄（証券コード）,売買した数　の列を含むdf
    today = datetime.datetime.now()
    #if today.hour 
    #tomorrow_9oc = datetime.datetime(today.year, today.month, today.day, 9, 0, 0) datetime.timedelta(days=)
    #if pl_done_tf == 1 and  - datetime.datetime.now():
    pl_sum = hold_money
    #pl_sum_fee = 0
    df_purchase_pl = df_purchase #損益用に新しいdf
    df_holding_stock =pd.DataFrame({ 'Code': [0],
                                     'Amount': [0]}) #持ち株データを保持(先頭にダミーデータ)
    #df_purchase_pl.insert(2, 'Company', '---')#会社名用
    df_purchase_pl['unit_purchase'] = 0 #終値単価ー売買時
    df_purchase_pl['purchase'] = 0 #売買した日の終値いくら　列追加
    #df_purchase_pl['P/L'] = 0 #昨日の終値時点での損益いくら　列追加
    df_purchase_pl['fee'] = 0 #売買時の委託手数料
    #df_purchase_pl['P/L(in_fee)'] = 0 #手数料含めて、昨日の終値時点で売った場合の損益
    #df_purchase_pl.loc['sum'] = 
    for i in range(len(df_purchase)):

        purchase_day = datetime.datetime.strptime(df_purchase['Date'][i], "%Y-%m-%d") #売買した日
        df_purchase_realdata = data.DataReader(df_purchase_pl['Code'][i].astype('str') + '.JP', 'stooq', purchase_day, purchase_day)

        if len(df_purchase_realdata.index) > 0:
            if df_purchase_pl['buy_or_sell'][i] == 0: #買ったデータのとき
                #df_purchase_pl['Company'][i] = df_company.query('コード == df_purchase["Code"][i]')['銘柄名'][0]
                purchase_day = datetime.datetime.strptime(df_purchase['Date'][i], "%Y-%m-%d") #買った日
                #print(purchase_day)
                df_purchase_realdata = data.DataReader(df_purchase_pl['Code'][i].astype('str') + '.JP', 'stooq', purchase_day, purchase_day)

                df_purchase_pl['unit_purchase'][i] = df_purchase_realdata['Close'][0] #買った株の単価
                df_purchase_pl['purchase'][i] = - (df_purchase_realdata['Close'][0] * df_purchase_pl['Amount'][i])
                df_purchase_pl['fee'][i] = (df_purchase_pl['purchase'][i] * 0.005 * 1.10)
                pl_sum += (df_purchase_pl['purchase'][i] + df_purchase_pl['fee'][i])
            

                df_temp = df_holding_stock[df_holding_stock['Code'] == df_purchase_pl['Code'][i]] #いま見ている売買データの銘柄が保持株にあるか検索してその行を抜き出す
                if not df_temp.empty: #すでに買っている株を追加で買った場合
                    df_holding_stock['Amount'][df_temp.index.values[0]] += df_purchase_pl['Amount'][i]
                    print(df_holding_stock)
                else: #いま保持していない株を買った場合、保有株データに登録
                    df_holding_stock.loc[len(df_holding_stock)] = [df_purchase_pl['Code'][i], df_purchase_pl['Amount'][i]]
                    print(df_holding_stock)

            else: #売ったデータの時
                purchase_day = datetime.datetime.strptime(df_purchase['Date'][i], "%Y-%m-%d") #売った日
                #print(purchase_day)
                df_purchase_realdata = data.DataReader(df_purchase_pl['Code'][i].astype('str') + '.JP', 'stooq', purchase_day, purchase_day)
                #print(df_purchase_realdata)
                df_purchase_pl['unit_purchase'][i] = df_purchase_realdata['Close'][0] #売った株の単価
                df_purchase_pl['purchase'][i] = df_purchase_realdata['Close'][0] * df_purchase_pl['Amount'][i] #売った株の価格
                df_purchase_pl['fee'][i] = - (df_purchase_pl['purchase'][i] * 0.005 * 1.10)
                pl_sum += (df_purchase_pl['purchase'][i] + df_purchase_pl['fee'][i])

                df_temp =  df_holding_stock[df_holding_stock['Code'] == df_purchase_pl['Code'][i]] #いま見ている売買データの銘柄が保持株にあるか検索してその行を抜き出す
                if df_temp.empty: #持っていないのに売ったことになっている場合
                    print('パターン1')
                    sys.exit('Invalid stock-trade data in the row' + str(i))
                else:
                    index_temp = df_temp.index.values[0] #保持株dfのうちいま見ている銘柄の行のインデックス
                    print('index_temp:' + str(index_temp))
                    stockAmount_diff = df_holding_stock['Amount'][index_temp] - df_purchase_pl['Amount'][i] #保持している株-売った株数
                    if stockAmount_diff == 0: #この株売りによってその会社の株が無くなった場合（＝全部売った）
                        df_holding_stock = df_holding_stock.drop(index_temp) #保持株データからその行を消す
                        print(df_holding_stock)
                        df_holding_stock = df_holding_stock.set_axis(list(range(len(df_holding_stock))))
                        print(df_holding_stock)
                    elif stockAmount_diff > 0: #部分的に売った場合
                        df_holding_stock['Amount'][index_temp] -= df_purchase_pl['Amount'][i]
                    else: #保持株以上に株を売ったようなデータになっているとき
                        print('パターン2')
                        sys.exit('Invalid stock-trade data in the row' + str(i))
        
        #print(i)
    
    df_holding_stock = df_holding_stock.set_axis(list(range(len(df_holding_stock)))) #index(行名)を振り直す
    holding_stock_value = 0
    df_holding_stock['now_unit'] = 0 #現在(前営業日)の株単価(終値)
    df_holding_stock['value'] = 0 #現在の持ち株の価値(株単価*量)
    yesterday = n_bizdays_ago(1)
    for i in range(1, len(df_holding_stock)):
        df_temp = data.DataReader(df_holding_stock['Code'][i].astype('str') + '.JP', 'stooq', yesterday, yesterday)
        print(df_temp)
        df_holding_stock['now_unit'][i] = df_temp['Close'][0] #現在(前営業日)の株単価(終値)
        df_holding_stock['value'][i] = df_holding_stock['Amount'][i] * df_temp['Close'][0]#現在の持ち株の価値(株単価*量)
        holding_stock_value += df_holding_stock['value'][i]
    
    total_assets = pl_sum + holding_stock_value

    capital_gains_tax = 0 #譲渡益税（現在の儲け(=所持金+所持株の価値が1000万を超える場合、超えた分の20%)）
    if total_assets > 10000000:
        capital_gains_tax = ((total_assets) - 10000000) * 0.2

    pl_info = pd.DataFrame({'手持金': [pl_sum],
                            '持ち株の価値': [holding_stock_value],
                            '資産合計': [total_assets],
                            '譲渡益税': [capital_gains_tax]})
    

    st.table(df_purchase_pl)
    st.table(df_holding_stock)
    st.table(pl_info)
    st.write("手持金: " + str(pl_sum)) #いま持っている所持金
    st.write("持ち株の価値: " + str(holding_stock_value)) #いま持っている株の価値

    st.write("資産合計: " + str(total_assets))
    
    st.write("譲渡益税: " + str(capital_gains_tax))

    #pl_extime = datetime.datetime.now()
    #pl_done_tf = 1


#ref. : https://qiita.com/hid_tanabe/items/3c5e6e85c6c65f7b38be
def isBizDay(DATE):
    Date = datetime.date(int(DATE.year), int(DATE.month), int(DATE.day))
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return 0
    else:
        return 1


def n_bizdays_ago(n): #n営業日前を出す
    #stooqの仕様的に、翌営業日にならないと前営業日のデータは取れない。
    #よって今日を含んでn+1日ぶん数えなくてはならない。例えば日曜日の１営業日前は木曜日になる。
    today = datetime.datetime.now()
    i = 0 #結果的に休日を含んだn日前になるカウンター
    c = n+1 #平日を数えた時にだけ減らしていくカウンター
    while c!=0:
        if isBizDay(today - timedelta(i)): #i日前が平日だったら
            n_bizdays = today - timedelta(i)
            i+=1
            c-=1
        else:
            i+=1
    return n_bizdays


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