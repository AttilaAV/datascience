import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import plotly.graph_objects as go

#Merging the 5 csvs into one CSV 
df = pd.read_csv('./Test files/spacedata1.csv')


files = [file for file in os.listdir('./Test files')]

#creating an empty dataframe
all_space_data = pd.DataFrame()

for file in files:
    df = pd.read_csv('./Test files/' + file, header=None, error_bad_lines=False)
    all_space_data = pd.concat([all_space_data, df])
    
all_space_data.columns = ["timestamp", "axis"]
    
all_space_data.to_csv('all_data.csv')
print(all_space_data.head())

#cleaning the data
#Just removing NaN data
nan_df = all_space_data[all_space_data.isna().any(axis=1)]
nan_df.head()

all_space_data = all_space_data.dropna(how='any')
print(all_space_data.head())

#Getting data by Hours
all_space_data['Hours'] = all_space_data['timestamp'].apply(lambda x: str(x).split(':')[0].split(' ')[1])
print(all_space_data.tail())

#printing results grouped by hour
results = all_space_data.groupby('Hours').sum().reset_index()
print(results)

print(all_space_data.sort_values(by='axis'))

#plotting the data to see peak values visually 
fig = go.Figure(data=go.Scatter(
    y = all_space_data['axis'],
    mode = 'lines'
))

fig.show()

#Finding high peak values over 200 difference, creating a list with the timestamps
all_space_data['high_peak'] = (all_space_data.axis.diff() >= 200)

plotList = all_space_data.loc[all_space_data['high_peak'] == True, 'timestamp'].values

print("\n Peak data's timestamps")
print(plotList)