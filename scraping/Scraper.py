import requests
from pymongo import MongoClient
import pandas as pd

with open('C:/Users/Acer/RecommendationSystem/Credentials') as f:
    acc_name = f.readline()
    email = f.readline()
    password = f.readline()   
    API_KEY = f.readline()
    f.close()
    

connection_string = 'mongodb+srv://{}:{}@cluster0.mfdjn.mongodb.net/?retryWrites=true&w=majority'.format(acc_name, password)
client = MongoClient(connection_string)
db = client['RecommendationSystem']
collection = db['Movies']
movies_list = []

for year in range (1980, 2023):
    nb_of_movies = 20
    p=1
    while nb_of_movies == 20:
        response = requests.get(
            'https://api.themoviedb.org/3/discover/movie?api_key=6196fd87f7e12945a5f7e24500542692&primary_release_year={}&page={}'.format(year ,p))
        movies = response.json()
        results = movies['results']
        collection.insert_many(results)
        nb_of_movies = len(results)
        movies_list.extend(results)
        if p%20 == 0: print(p)
        p+=1
        
movies = pd.DataFrame(movies_list)
# movies.to_csv('Movies.csv')

movies = pd.read_csv(r'C:/Users/Acer/RecommendationSystem/Movies.csv', index_col=0)

movies_info = []       

for movie_id in movies['id']:
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6196fd87f7e12945a5f7e24500542692&language=en-US'.format(movie_id))
    res = response.json()
    movies_info.append(res)
    if len(movies_info)%10000 == 0: print(len(movies_info))
    
df = pd.json_normalize(movies_info) 
#df.to_csv('movies_info.csv')  
