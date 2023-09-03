import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit.components.v1 as components

#import pydeck as pdk
#from dotenv import load_dotenv

#load_dotenv()#.env読み込み

URL = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
API_KEY = '5b72fd618663afad'

body = {}

def getShop(body, URL):
    response = requests.get(URL, params=body)
    datumn = response.json()
    stores = datumn['results']['shop']  # 'shop' キーで店舗情報を取得
    stores_datas = []  # 店舗名を格納するリスト
    for store in stores:
        #name = store['name']  # 各店舗の 'name' キーから名前を取得
        stores_datas.append([store['name'], store['budget']['average'], store['open'], store['urls']['pc']])  # リストに追加
    return stores_datas  # 店のリストを返す

st.title('大学生のための居酒屋検索🔎')
st.caption('飲み放題ありの店舗のみ出力されます^_^')

with st.form(key='form'):
    selected_keyword = st.text_input('地名 or キーワードを入力', '町田')
    selected_free_food = st.toggle('食べ放題')
    private_room = st.toggle('個室あり')
    midnight2 = st.toggle('23時以降食事OK')
    if selected_free_food:
        free_food = 1   
    else:
        free_food = 0  
    if selected_free_food:
        private_room = 1   
    else:
        private_room = 0  
    if midnight2:
        midnight = 1
    else:
        midnight = 0
    count = st.slider("検索店舗数", 1, 20, 10)
    submit_btn = st.form_submit_button('検索')

body = {
    'key' : API_KEY,
    'keyword' : selected_keyword,
    'free_drink' : 1,
    'free_food' : free_food,
    'private_room' : private_room,
    'midnight_meal' : midnight,
    'count' : count,
    'format' : 'json',
    #'sommelier' : sommelier
}
columns = ['name', 'budget', 'open', 'urls']

if(submit_btn):
    answers = getShop(body, URL)
    st.success(f'{len(answers)}店舗出力されました☺️')
    df_stores = pd.DataFrame(answers, columns=columns)
    st.dataframe(df_stores)
    st.info('もう一度検索する場合は、ブラウザを更新してください😺', icon="ℹ️")

#st.text(('Powered by', '<a href="http://webservice.recruit.co.jp/"ホットペッパー Webサービス</a>'))

components.html(
    '''
    <a href="http://webservice.recruit.co.jp/"><img src="http://webservice.recruit.co.jp/banner/hotpepper-s.gif" alt="ホットペッパー Webサービス" width="135" height="17" border="0" title="ホットペッパー Webサービス"></a>
    '''
)
#Powered by <a href="http://webservice.recruit.co.jp/">ホットペッパー Webサービス</a>