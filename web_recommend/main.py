import streamlit as st 
import pandas as pd
import pickle
from book import book_UI
import warnings
from movie import movie_UI
from game import game_UI

pd.reset_option('all')
warnings.simplefilter(action='ignore', category=FutureWarning)

st.title("Recommendation Systems")
def header(url):
     st.markdown(f"""<p style="color:#33ff33;
            font-size:24px;border-radius:2%;">{url}</p>""", unsafe_allow_html=True)
header("This is a recommendation engine for movies,games and books.")
title=pd.read_csv('data/title.csv')
game_data=pd.read_csv("data/steam.csv")
movies = pickle.load(open('models\movies\movie_list.pkl','rb'))
books=pd.read_csv('data/data.csv',error_bad_lines = False,warn_bad_lines=False)
book_title = books['title'].drop_duplicates()
book_title=pd.DataFrame(book_title)
movie_title = movies['title'].values
movie_title=pd.DataFrame(movie_title)
movie_title = movie_title.rename(columns={0: 'title'})
game_title=game_data['name'].drop_duplicates()
game_title=pd.DataFrame(game_title)
game_title = game_title.rename(columns={'name': 'title'})
input=st.selectbox('Enter the Product name:',title['title'])

def init(inp):
  if inp in list(book_title['title']):
    return('book')
  elif inp in list(movie_title['title']):
    return('movie')
  else:
    return('game')

def book():
  st.write('This is the book model')
  book_UI(input)

def movie():
  st.write('This is the movie model')
  movie_UI(input)

def game():
  st.write('This is the game model')
  game_UI(input)

if st.button("Show Recommendation"):
    if init(input)=="book":
      book()
    elif init(input)=="movie":
      movie()
    elif init(input)=="game":
      game()