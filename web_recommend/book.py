import streamlit as st 
import pickle
import pandas as pd 
import numpy as np
import requests
import json
from models.book import books_api
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
df=pd.read_csv(r'data/df.csv')
df1=pd.read_csv(r'data/data.csv',error_bad_lines = False,warn_bad_lines=False)
with open(r'model.pkl','rb') as f:
    model=pickle.loads(f.read())  
model.fit(df)
dist, idlist = model.kneighbors(df)

def book_covers(name):
        cover=[]
        try:
            book_id = df1[df1['title'] == name].index
            book_id = book_id[0]
        except IndexError:
            pass
        for newid in idlist[book_id]:
            cover.append(df1.loc[newid].isbn)
        return cover
    
def Recommender(name):
            book_list = []
            try:
                book_id = df1[df1['title'] == name].index
                book_id = book_id[0]
            except IndexError:
                pass
            for newid in idlist[book_id]:
                book_list.append(df1.loc[newid].title)
            return book_list
def details(isbn,set):
        try:
            api = books_api.Api()
            json_data = api.list(f'isbn:{isbn}')
            data =json_data['items'][0]
            if set=='link':
                return (data['volumeInfo']['previewLink'])
            if set=='des':
                return (data['volumeInfo']['description'])
        except KeyError:
            pass
def desc(inp,mode):
    response_API = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{inp}&jscmd=details&format=json')
    data = response_API.text
    data=json.loads(data)
    if mode=='book':
        return data[f'ISBN:{inp}']['preview_url']
    elif mode=='des':
        return data[f'ISBN:{inp}']['details']['description'] 
    elif mode=='pages':
        return data[f'ISBN:{inp}']['details']['number_of_pages']
    elif mode=='date':
        return data[f'ISBN:{inp}']['details']['publish_date'] 

def book_UI(book_input):
    output1=Recommender(book_input)
    st.write(f"The Recommended Books for **{book_input}**: ")
    for i in range(1,len(output1)):
        with st.expander(f'{i}) {output1[i]}'):
            isbn=book_covers(book_input)
            cover,description=st.columns(2)
            with cover:
                url="http://covers.openlibrary.org/b/isbn/{}-L.jpg".format(isbn[i])
                st.image(url)
            with description:
                try:
                    st.write("Description")
                    st.write(details(isbn[i],'des'))
                except None:
                    st.write('No description available')
                    pass
            detail,ebook=st.columns(2)
            with detail:
                link = f"[More Info]({details(isbn[i],'link')})"
                st.markdown(link, unsafe_allow_html=True)
            with ebook:
                link1=f"[Ebook]({desc(isbn[i],'book')})"
                st.markdown(link1, unsafe_allow_html=True)
            

                    

