import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import json


def extract_datetime(file_key, t_type):
    if 'secs' in file_key:
        time = file_key.split('_')[2].split('-')
        if t_type == 'hour':
            hour = time[0]
            return hour
        elif t_type == 'minute':
            minute = time[1]
            return minute
        else:
            raise ValueError("Incorrect t_type input!")
    else:
        time = file_key.split('_')[-1]
        if t_type == 'hour':
            hour = time[:2]
            return hour
        elif t_type == 'minute':
            minute = time[2:4]
            return minute
        else:
            raise ValueError("Incorrect t_type input!")
            

### Change the file path accordingly   
path = './data/forestia/*.csv'
paths = glob.glob(path)

# columns = ['file_key', 'recording_date', 'pi_id', 'species_class',
#        'confidence_score', 'time_segment_id', 'collected_biodiversity_score',
#        'device_type']
dfs = []
for path in paths:
#    print(path)
    df = pd.read_csv(path)
    df = df.drop(['Unnamed: 0', 'created_at', 'device_type'], axis=1)
    dfs.append(df)
dfs = pd.concat(dfs, axis=0)
df = dfs.copy()
del dfs
unique_classes = df['species_class'].unique()

df['unique_date'] = df['pi_id']+'_'+ df['recording_date']
df['filename'] = df.loc[:, 'time_segment_id'].apply(lambda x: '_'.join(x.split('_')[:2]))
df['year'] = df.loc[:,'recording_date'].apply(lambda x: x.split('-')[0])
df['month'] = df.loc[:,'recording_date'].apply(lambda x: x.split('-')[1])
df['date'] = df.loc[:,'recording_date'].apply(lambda x: x.split('-')[2])
df['hour'] = df.loc[:,'file_key'].apply(lambda x: extract_datetime(x, 'hour'))
df['minute'] = df.loc[:, 'file_key'].apply(lambda x: extract_datetime(x, 'minute'))
df['ith_sec'] = df.loc[:, 'time_segment_id'].apply(lambda x: x.split('_')[-1])

hourly_count = df[['confidence_score', 'unique_date', 'hour', 'species_class']].groupby(['unique_date', 'hour', 'species_class']).count()
hourly_count.columns = ['count']
hourly_avg_conf = df[['confidence_score', 'unique_date', 'hour', 'species_class']].groupby(['unique_date', 'hour', 'species_class']).mean()
hourly_avg_conf.columns = ['avg_conf']
hourly_data = pd.concat([hourly_count, hourly_avg_conf], axis=1)

hourly_data_pivot = hourly_data.pivot_table(index=['unique_date', 'hour'], columns='species_class', values='count', fill_value=0)
# hourly_data_pivot = hourly_data_pivot.drop(["Noise", "Plane", "Thunderstorm", "Human_noise"], axis=1)
hourly_data_conf = hourly_data.pivot_table(index=['unique_date', 'hour'], columns='species_class', values='avg_conf', fill_value=0)
hourly_data_conf = hourly_data_conf.drop(["Noise", "Plane", "Thunderstorm", "Human_noise"], axis=1)
hourly_data_conf.columns = [item+'_conf' for item in hourly_data_conf.columns]
hourly_data_final = pd.concat([hourly_data_pivot, hourly_data_conf], axis=1)
hourly_data_final = hourly_data_final.reset_index()
hourly_data_final.to_csv('forestia_processed_df.csv', index=False)


