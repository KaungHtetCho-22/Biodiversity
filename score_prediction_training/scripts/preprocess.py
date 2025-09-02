import os
import pandas as pd
import numpy as np
import glob
import argparse


argparser = argparse.ArgumentParser()
argparser.add_argument('--csv_path', help="Path of csv file(s).")
# argparser.add_argument('--metric', help="count or mean.")
args = argparser.parse_args()

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
        time = file_key.split('_')[3]
        if t_type == 'hour':
            hour = time[:2]
            return hour
        elif t_type == 'minute':
            minute = time[2:4]
            return minute
        else:
            raise ValueError("Incorrect t_type input!")
        
### Since the early groud truths are based on 5 levels biodiversity scores, we have to convert them into 3 classes(0,1,2).
def convert_score_levels(score):
    if score == 1:
        return 2
    elif score == 2:
        return 2
    elif score == 3:
        return 1
    elif score == 5:
        return 0
    else:
        raise ValueError("Wrong Biodiversity Score Level!!!")


### Read csv files and convert them into a single frequency pivot table
path = f'{args.csv_path}/*.csv'
paths = glob.glob(path)

dfs = []
for path in paths:
    tmp_df = pd.read_csv(path)
    tmp_df = tmp_df[['file_key', 'recording_date', 'pi_id', 'species_class', 'confidence_score', 'time_segment_id', 'collected_biodiversity_score', 'device_type']]
    dfs.append(tmp_df)
df = pd.concat(dfs, axis=0).reset_index(drop=True)
del dfs

mobiles = ['IOT6', 'IOT9', 'IOT10', 'IOT7']
df = df[~df['pi_id'].isin(mobiles)]
unique_classes = df['species_class'].unique()
        
df['unique_date'] = df['pi_id']+'_'+ df['recording_date']
df['hour'] = df.loc[:,'file_key'].apply(lambda x: extract_datetime(x, 'hour'))

hourly_count = df[['pi_id', 'unique_date', 'species_class', 'confidence_score', 'collected_biodiversity_score', 'hour']].groupby(['unique_date', 'pi_id', 'species_class', 'collected_biodiversity_score', 'hour']).count()
hourly_count.columns = ['count']

hourly_data_pivot = hourly_count.pivot_table(index=['unique_date', 'pi_id', 'collected_biodiversity_score', 'hour'], columns='species_class', values='count', fill_value=0)
# hourly_data_pivot = hourly_data_pivot.drop(["Noise", "Plane", "Thunderstorm", "Human_noise"], axis=1)
hourly_data_pivot.reset_index(inplace=True)
hourly_data_pivot['biodiversity_level'] = hourly_data_pivot['collected_biodiversity_score'].apply(lambda x: convert_score_levels(x))
hourly_data_pivot.drop('collected_biodiversity_score', axis=1, inplace=True)

print(hourly_data_pivot)
hourly_data_pivot.to_csv('pivot_table.csv', index=False)
# hourly_metric = hourly_metric.reset_index('pi_id')
