import pandas as pd
import numpy as np
import requests

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from datetime import datetime


movies = pd.read_csv(r'C:/Users/Acer/RecommendationSystem/Movies.csv')
info = pd.read_csv(
    '/home/piotrek/Documents/RecommendationSystem/movies_info.csv')

movies.info()
info.info()

movies.drop_duplicates(subset=['id', 'title', 'release_date'], inplace=True)
info.drop_duplicates(subset=['id', 'title', 'release_date'], inplace=True)

duplicated_columns = []
for column in movies.columns:
    if column in info.columns:
        duplicated_columns.append(column)

print('Zduplikowane kolumny: {}/{}'.format(len(duplicated_columns), len(movies.columns)))
for column in movies.columns:
    if column not in info.columns:
        print(column)

info = info.loc[info['status'].isin(['Released', 'In Production',
                                     'Post Production', 'Planned'])]

info = info.drop(['Unnamed: 0', 'backdrop_path', 'belongs_to_collection',
                 'homepage', 'imdb_id', 'status', 'status_code',
                  'tagline', 'belongs_to_collection.poster_path',
                  'belongs_to_collection.id', 'status_message', 'spoken_languages',
                  'original_title', 'belongs_to_collection.name', 'adult',
                  'belongs_to_collection.backdrop_path', 'success', 'video',
                  'budget', 'runtime', 'revenue', 'popularity', 'id'], axis=1)


def def_genres(row):
    genres = []
    res = list(eval(row))
    for x in res:
        for key, value in x.items():
            if 'id' in key:
                genres.append(value)
    return genres


def get_companies(row):
    companies = []
    res = list(eval(row))
    for x in res:
        for key, value in x.items():
            if 'id' in key:
                companies.append(value)
    return companies


def get_countries(row):
    countries = []
    res = list(eval(row))
    for x in res:
        for key, value in x.items():
            if 'iso_3166_1' in key:
                countries.append(value)
    return countries


'''
list_ids = []
list_names = []
def get_dict(row):
    res = list(eval(row))
    for x in res:
        for key, value in x.items():
            if 'id' in key:
                if value not in list_ids:
                    list_ids.append(value)
            if 'name' in key:
                if value not in list_names:
                    list_names.append(value)'''

# info.genres.apply(get_dict)
# info['production_companies'].apply(get_dict)
# info['production_countries'].apply(get_dict)

#genres = pd.DataFrame(list(zip(list_ids, list_names)), columns = ['Genre_id', 'Genre_name']).to_csv('Genres.csv')
#companies = pd.DataFrame(list(zip(list_ids, list_names)), columns = ['Company_id', 'Company_name']).to_csv('Companies.csv')
#countries = pd.DataFrame(list(zip(list_ids, list_names)), columns = ['Country_id', 'Country_name']).to_csv('Country.csv')

info['genres_new'] = info.genres.apply(def_genres)
info['production_company'] = info['production_companies'].apply(get_companies)
info['countries'] = info['production_countries'].apply(get_countries)

info = info.drop(['genres', 'production_companies',
                 'production_countries'], axis=1)
#info['nb of genres'] = info['genres_new'].str.len()
#info['nb of production companies'] = info['production_company'].str.len()
#info.drop(['nb of genres', 'nb of production companies'], axis=1)


info['release_date'] = info['release_date'].astype(str)
century = 0


def get_production_century(row):
    global century
    if row[0] == 'n':
        row = row.replace('n', '00').replace('a0', '00')
    century = row[2] + '0'
    return str(century)


def get_production_year(row):
    year = row[0:4]
    return str(year)


info = info.replace('n', 0).replace(np.nan, 0)
info['production_year'] = info['release_date'].apply(get_production_year)
info['production_century'] = info['production_year'].apply(
    get_production_century)


C = info['vote_average'].mean()
m = info['vote_count'].quantile(0.9)


def weighted_rating(row, m=m, C=C):
    v = row['vote_count']
    R = row['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)


info['score'] = info.apply(weighted_rating, axis=1)

info = info.drop(['vote_average', 'vote_count', 'release_date'], axis=1)


def col_1(row):
    if(len(row) >= 1):
        col_1 = row[0]
    else:
        col_1 = None
    return col_1



info['genre'] = info.genres_new.apply(col_1)

info['company'] = info['production_company'].apply(col_1)

info['country'] = info['countries'].apply(col_1)

le = LabelEncoder()
info['country'] = le.fit_transform(info['country'])

le = LabelEncoder()
info['original_language'] = le.fit_transform(info['original_language'])


info = info.drop(['genres_new', 'production_company', 'countries'], axis=1)

info['title'] = info['title'].str.lower()
info['title year'] = info['title'] + ' ' + info['production_year']
info = info.drop(['title', 'production_year'], axis=1)
info = info.replace('n', 0).replace(np.nan, 0)

lr = LabelEncoder()

info['movie_id'] = lr.fit_transform(info['title year'])

df = pd.get_dummies(info, columns=['production_century'])
df = pd.get_dummies(df, columns=['genre'])
df = df.set_index('movie_id')

mms = MinMaxScaler()
titles = info[['title year', 'movie_id', 'overview', 'poster_path']]

df = df.drop(['title year', 'overview', 'poster_path'], axis=1)
mms.fit(df)
#df = mms.fit_transform(df)
df = pd.DataFrame(mms.transform(df), index=df.index, columns=df.columns)
df = pd.merge(df, titles, on='movie_id')

def get_full_poster_path(row):
    path = 'https://image.tmdb.org/t/p/original' + row
    return path
df['full_poster_path'] = df['poster_path'].apply(get_full_poster_path)
df = df.drop('poster_path', axis=1)
#df.to_csv('KNN_movies1.csv')




