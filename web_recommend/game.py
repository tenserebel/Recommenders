import streamlit as st
import pandas as pd 
import numpy as np
import requests
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 


game_data=pd.read_csv("data/steam.csv")
info=pd.read_csv("data/steam_data.csv")
desc=pd.read_csv("data/steam_games.csv")
count_vec = CountVectorizer(stop_words='english')
with open('models\game\data.pkl','rb') as f:
       data=pickle.loads(f.read())

@st.cache()
def output(game_input):
    count_matrix = count_vec.fit_transform(data['alls']) 

    cosine_sim = cosine_similarity(count_matrix, count_matrix)
   
    ind = data[data['name'] == game_input].index.to_list()[0]
    cos_scor = list(enumerate(cosine_sim[ind]))
    cos_scor = sorted(cos_scor, key=lambda x: x[1], reverse=True)
    cos_scor = cos_scor[1:7]
    ten_ind = [i[0] for i in cos_scor]
    return data['name'].iloc[ten_ind] 
    
title=game_data['name'].drop_duplicates()
def game_UI(game_input):
    st.write("The recomended games are:")
    games=output(game_input)
    games=list(games)
    for i in range(len(games)):
        with st.expander(f"{games[i]}"):
            url=info[info['name']==games[i]]['url']
            image,description=st.columns(2)
            with image:
                try:
                    img_url=info[info['name']==games[i]]['img_url']
                    img_url=list(img_url)
                    st.image(img_url[0])
                except IndexError:
                    pass
            with description:
                try:
                    description=desc[desc['name']==games[i]]['desc_snippet']
                    description=list(description)
                    st.write(description[0])
                except IndexError:
                    pass
            try:
                url=list(url)
                url=str(url[0])
                link = f'[Game URL]({url})'
                st.markdown(link, unsafe_allow_html=True)
            except IndexError:
                pass
            date,developer,price=st.columns(3)
            with date:
                st.write("Date")
                try:
                    date_data=info[info['name']==games[i]]['date']
                    date_data=list(date_data)
                    date_data=date_data[0]
                    st.write(date_data)
                except IndexError:
                    pass
            with developer:
                st.write("Developer")
                try:
                    dev_data=info[info['name']==games[i]]['developer']
                    dev_data=list(dev_data)
                    dev_data=dev_data[0]
                    st.write(dev_data) 
                except IndexError:
                    pass   
            with price:
                st.write("Price:")
                try:
                    pri=desc[desc['name']==games[i]]['original_price']
                    pri=list(pri)
                    st.write(pri[0])
                except IndexError:
                    pass







