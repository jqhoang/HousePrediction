import extract_map_boundary as emb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# function to draw a graph for population change in each ethinicity
def draw_graph(i):
    plt.bar(x_axis,d2006[i]*100,width,label="Year 2006")
    plt.bar(x_axis+width,d2011[i]*100,width,label="Year 2011")
    plt.title(f'Graph of {commonList[i]}')
    plt.xticks(x_axis + width/2, labels.str[:2])
    plt.legend()
    plt.ylabel("% of population change")
    plt.xlabel("region")
    plt.show()

# read property value change from dataframes
delta2006 = emb.get_delta_year_2006_2011().drop('REGION',axis=1)
delta2011 = emb.get_delta_year_2011_2016().drop('REGION',axis=1)

# drop the columns that contains nan for year 2006
for i in delta2006.columns:
    for j in delta2006[i]:
        if math.isnan(j):
            delta2006 = delta2006.drop(i,axis=1)
            break

# drop the columns that contains nan for year 2011
for i in delta2011.columns:
    for j in delta2011[i]:
        if math.isnan(j):
            delta2011 = delta2011.drop(i,axis=1)
            break

# draw the graph
commonList = delta2011.columns.intersection(delta2006.columns)
d2006 = np.zeros((len(commonList),delta2006.shape[0]))
d2011 = np.zeros((len(commonList),delta2006.shape[0]))
count = 0
for i in commonList:
    d2006[count] = np.array(delta2006[i])
    d2011[count] = np.array(delta2011[i])
    count+=1
labels = delta2006.index
x_axis = np.arange(len(labels))

width = 0.35

for i in range(len(commonList)):
    draw_graph(i)


