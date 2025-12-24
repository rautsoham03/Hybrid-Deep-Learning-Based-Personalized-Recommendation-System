# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 00:08:25 2025

@author: sanke
"""


import pandas as pd
import os 
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import LabelEncoder, MinMaxScaler
# from sklearn.model_selection import train_test_split

os.chdir(r'C:\Users\sanke\Downloads\movielens100k')
# Load the available files# Load the available files
movies_df = pd.read_csv('movies.csv')
tags_df = pd.read_csv('tags.csv') # Load tags
ratings_df = pd.read_csv('ratings.csv')
tags_df = tags_df[['userId','movieId','tag','timestamp']]
ratings_df.rename(columns={'timestamp': 'timestamp_rating'}, inplace=True)

# AGGREGATION: Group by (userId, movieId) and join all UNIQUE tags
# This creates ONE row per unique (user, movie) pair that had a tag.
aggregated_tags_df = tags_df.groupby(['userId', 'movieId'])['tag'].apply(
    # Use x.dropna() to remove float/NaN values before joining
    lambda x: ', '.join(x.dropna().unique())
).reset_index(name='concatenated_tags')

print(f"Aggregated Tags DataFrame size: {aggregated_tags_df.shape}")

# 1. Merge ratings and tags
merged_df = pd.merge(
    ratings_df,
    aggregated_tags_df,
    on=['userId', 'movieId'],
    how='left')

# 2. Merge the result with movies
final_df = pd.merge(
    merged_df,
    movies_df[['movieId', 'title', 'genres']],
    on='movieId',
    how='left'
)

final_df['rating_time'] = pd.to_datetime(final_df['timestamp_rating'],unit='s')
final_df['rating_time'].head(4)

final_df['userId'].nunique()

final_df['tags']=final_df['concatenated_tags']
final_df = final_df.drop('concatenated_tags',axis=1)

# Use .str.replace() which is optimized for element-wise string replacement
final_df['genres'] = final_df['genres'].str.replace('|', ',', regex=False)
final_df.dtypes
final_df.drop('timestamp_rating',axis=1,inplace=True)
final_df.dtypes

# 1. Initialize Encoders
# user_encoder = LabelEncoder()
# movie_encoder = LabelEncoder()

# 2. Fit and Transform User IDs and movie IDs
# This creates a new column with values from 0 up to N_users - 1
# final_df['user_id_encoded'] = user_encoder.fit_transform(final_df['userId'])
# final_df['movie_id_encoded'] = movie_encoder.fit_transform(final_df['movieId'])


final_df.to_csv(r'C:\Users\sanke\OneDrive\Desktop\DDA project\movielens100k.csv',index=False)
