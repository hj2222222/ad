import streamlit as st
import requests
from pymongo import MongoClient

url = 'DB_URL'
client = MongoClient(url)
database = client['aiproject']
collection = database['advertisement']


st.title("광고 문구를 생성해주는 서비스앱")
product_name = st.text_area("제품 이름", "")
details = st.text_area("주요 내용 ", "")
options = st.multiselect("광고 문구의 느낌",
                        ["기본", "재밌게", "차분하게",
                         "과장스럽게","참신하게","고급스럽게",
                         "센스있게","아름답게"]
                        )

if st.button("광고 문구 생성하기"):
    advertise = {"product_name":product_name,"details":details,
    "tone_and_manner": ", ".join(options)}
    response = requests.post("http://localhost:8000/ad",
                                 json=advertise)
    print(response)
    ad = response.json()['ad']
    st.success(ad)
    ads = {"product_name":product_name,"details":details,
    "tone_and_manner": ", ".join(options),"ment" : ad}
    print(ads)
    collection.insert_one(ads)
    result = collection.find({})
    datas = {
        "기업이름":[],
        "세부내용":[],
        "느낌":[],
        "멘트":[]
    }
    print(result)
    for data in result:
        datas["기업이름"].append(data['product_name'])
        datas["세부내용"].append(data['details'])
        datas["느낌"].append(data['tone_and_manner'])
        datas["멘트"].append(data['ment'])
        print(data['product_name'])

    st.table(datas)