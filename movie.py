import pandas as pd
#import numpy as np

#from sklearn.neighbors import NearestNeighbors



pd.set_option('display.max_columns', 100)

df = pd.read_csv('KNN_movies.csv', index_col = 0, lineterminator='\n')

df2 = df['title year'].tolist()

#features = df.drop(['title'], axis=1)
#knn = NearestNeighbors(metric='cosine', algorithm='auto')
#knn.fit(features)

#distances, indices = knn.kneighbors(features)

#dist = pd.DataFrame(distances)
#ind = pd.DataFrame(indices)
#dist.to_csv('distances.csv')
#ind.to_csv('indices.csv')
distances = pd.read_csv('distances.csv').drop('Unnamed: 0', axis=1).values
indices = pd.read_csv('indices.csv').drop('Unnamed: 0', axis=1).values

def get_index(movie):
    if movie in df['title year'].tolist():
        return df.loc[df['title year'] == movie].index.to_list()[0]
    else:
        return None

all_titles = list(df['title year'].values)

def get_id_from_partial_name(partial):
    for name in all_titles:
        if partial in name:
            print(name,  all_titles.index(name))

def print_similar_movies(movie=None):
    movies = []
    overviews = []
    paths = []
    all = []
    if movie:
        if get_index(movie):
            found_id = get_index(movie)
            for id in indices[found_id][1:]:
                movies.append(df.loc[id]['title year'])
                overviews.append(df.loc[id]['overview'])
                paths.append(df.loc[id]['full_poster_path'])
        else:
            for x in range(4):
                movies.append('Brak filmu w bazie     ')
                overviews.append('Brak opisu')
                paths.append('https://static.vecteezy.com/system/resources/previews/005/337/799/original/icon-image-not-found-free-vector.jpg')
    else:
        for x in range(4):
            movies.append('Brak filmu w bazie     ')
            overviews.append('Brak opisu')
            paths.append('https://static.vecteezy.com/system/resources/previews/005/337/799/original/icon-image-not-found-free-vector.jpg')
    all.append(movies)
    all.append(overviews)
    all.append(paths)
    return all