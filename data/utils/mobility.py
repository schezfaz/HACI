import pandas as pd
import numpy as np
import csv

df = pd.read_csv('mobility.csv')  
# df = df.reset_index() 
df = df.fillna(0)
# print(df)

df_mobility = df.copy()

for column in df_mobility.columns:
    if column != 'date' and column!= 'location_key':
        # df_mobility[column] = (df_mobility[column].astype(int)/df_mobility[column].astype(int)).abs().max()
        df_mobility[column] = (df_mobility[column].astype(int) - df_mobility[column].astype(int).min()) / (df_mobility[column].astype(int).max() - df_mobility[column].astype(int).min())    


df_mobility['mobility_all'] = df_mobility[list(df_mobility.columns)].sum(axis=1)
print(list(df_mobility.columns))

# print(df_mobility)

# print(df_mobility['mobility_all'])

# print(df_mobility['date'])

df_mobility.to_csv('mobility_cummulative.csv')  

# df_mobility['date'] = pd.to_datetime(df_mobility.date)
# # tidx = df_mobility.date_range('2020-02-15', '2022-12-09', name='date')
# # df_mobility.groupby(df_mobility.dates.dt.month)['mobility_all'].transform('mean')
# df_mobility.groupby(pd.PeriodIndex(df_mobility['date'], freq="M")).mean()

# print(df_mobility)

unique_countries = df_mobility.location_key.unique()
print(unique_countries)

DataFrameDict = {elem : pd.DataFrame() for elem in unique_countries}

for key in DataFrameDict.keys():
    print('working on 1:', key)
    DataFrameDict[key] = df_mobility[:][df_mobility.location_key == key]

# for country in df_mobility.location_key.unique():
#     print(df_mobility.loc[df_mobility['location_key'] == country])

# print(DataFrameDict['AE'])

mean_dict = {elem : pd.DataFrame() for elem in unique_countries}
for key in mean_dict.keys():
    print('working on 2:', key)
    mean_dict[key] = DataFrameDict[key].mean(axis=0)

x = pd.DataFrame.from_dict(mean_dict)
# print(x.T)
x=x.T

print('here')
x.to_csv('mean_mobility_1.csv')  

def replace_names():
    country_dict = {}
    with open('index.csv', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            if '_' not in str(row[0]):
                country_dict[row[0]] = row[5]
    # print(country_dict)

    data = []
    with open('mean_mobility.csv') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            try:
                # print(country_dict[row[0]])
                row[0] = country_dict[row[0]]
                data.append(row)
            except:
                data.append(row)

    with open('mean_mobility_pie.csv','w') as csvFile:
        csvWriter = csv.writer(csvFile, lineterminator='\n')
        for d in data:
            csvWriter.writerow(d)


def mobility_pie():
    data = []
    with open('mobility_cummulative.csv') as csvFile:
        csvReader =  csv.reader(csvFile)
        c = 0
        for line in csvReader:
            if 'location_key' in line[2]:
                data.append(line)
            if '_' not in line[2]:
                data.append(line)
                # print(line[2])


    with open('mobility-pie.csv','w') as csvFile:
        csvWriter = csv.writer(csvFile, lineterminator='\n')
        for d in data:
            csvWriter.writerow(d)

def mobility_pie_mean():
    df = pd.read_csv('mobility-pie.csv')  
    # print(df)
    df = df.fillna(0)
    df_mobility = df.copy()
    df_mobility = df_mobility.iloc[: , 1:]
    # print(list(df_mobility.columns))

    unique_countries = df_mobility.location_key.unique()
    # print('uniq: ', unique_countries)

    DataFrameDict = {elem : pd.DataFrame() for elem in unique_countries}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = df_mobility[:][df_mobility.location_key == key]


    mean_dict = {elem : pd.DataFrame() for elem in unique_countries}
    for key in mean_dict.keys():
        mean_dict[key] = DataFrameDict[key].mean(axis=0)

    x = pd.DataFrame.from_dict(mean_dict)
    # print(x.T)
    x=x.T
    # print(x)
    # x.to_csv('mean_mobility.csv')  
import pandas as pd
import csv

def cummulative():
    df = pd.read_csv('mobility.csv')  
    # df = df.reset_index() 
    df = df.fillna(0)
    # print(df)

    df_mobility = df.copy()

    for column in df_mobility.columns:
        if column != 'date' and column!= 'location_key':
            # df_mobility[column] = (df_mobility[column].astype(int)/df_mobility[column].astype(int)).abs().max()
            df_mobility[column] = (df_mobility[column].astype(int) - df_mobility[column].astype(int).min()) / (df_mobility[column].astype(int).max() - df_mobility[column].astype(int).min())    


    df_mobility['mobility_all'] = df_mobility[list(df_mobility.columns)].sum(axis=1)
    print(list(df_mobility.columns))

    df_mobility.to_csv('mobility_cummulative.csv')  

# cummulative()

def mobility_pie():
    data = []
    with open('mobility_cummulative.csv') as csvFile:
        csvReader =  csv.reader(csvFile)
        c = 0
        for line in csvReader:
            if 'location_key' in line[2]:
                data.append(line)
            if '_' not in line[2]:
                data.append(line)
                # print(line[2])


    with open('mobility-pie.csv','w') as csvFile:
        csvWriter = csv.writer(csvFile, lineterminator='\n')
        for d in data:
            csvWriter.writerow(d)

def mobility_pie_mean():
    df = pd.read_csv('mobility-pie.csv')  
    # print(df)
    df = df.fillna(0)
    df_mobility = df.copy()
    df_mobility = df_mobility.iloc[: , 1:]
    # print(list(df_mobility.columns))

    unique_countries = df_mobility.location_key.unique()
    # print('uniq: ', unique_countries)

    DataFrameDict = {elem : pd.DataFrame() for elem in unique_countries}
    for key in DataFrameDict.keys():
        DataFrameDict[key] = df_mobility[:][df_mobility.location_key == key]


    mean_dict = {elem : pd.DataFrame() for elem in unique_countries}
    for key in mean_dict.keys():
        mean_dict[key] = DataFrameDict[key].mean(axis=0)

    x = pd.DataFrame.from_dict(mean_dict)
    # print(x.T)
    x=x.T
    # print(x)
    x.to_csv('mean_mobility.csv')  

# # mobility_pie()
# mobility_pie_mean()
# # create_means()


def replace_names():
    country_dict = {}
    with open('index.csv', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile)
        for row in csvReader:
            if '_' not in str(row[0]):
                country_dict[row[0]] = row[5]
    # print(country_dict)

    data = []
    with open('mean_mobility.csv') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            try:
                # print(country_dict[row[0]])
                row[0] = country_dict[row[0]]
                data.append(row)
            except:
                data.append(row)

    with open('mobility_monthly.csv','w') as csvFile:
        csvWriter = csv.writer(csvFile, lineterminator='\n')
        for d in data:
            csvWriter.writerow(d)

# replace_names()


# # import csv
# # with open("mobility-AE.csv", mode="r") as file:
# #     csvFile = csv.reader(file)
# #     unique_countries = []
# #     for line in csvFile:
# #         if line[1] != 'location_key' and line[1] not in unique_countries:
# #             unique_countries.append(line[1])

# # country_dict = {}
# # for country in unique_countries:
# #     country_dict[country] = 1

# # print(country_dict)

# # with open("mobility-AE.csv", mode="r") as file:
# #     csvFile = csv.reader(file) 
# #     for country in unique_countries:
# #         print('country:' , country)
# #         for row in csvFile:
# #             if(row[1]=='AF'):
# #                 print(row)
# #             if row[1] == country:
# #                 # print(row[1])
# #                 country_dict[country] = country_dict[country] + 1
# #     print(country_dict)


#monthly mobility
import pandas as pd
import numpy as np
import csv

# df = pd.read_csv('mobility_month_wise.csv')   
# df_mobility = df.iloc[: , 1:]
# # print(df)

# unique_countries = df_mobility.location_key.unique()
# print(unique_countries)

# DataFrameDict = {elem : pd.DataFrame() for elem in unique_countries}

# for key in DataFrameDict.keys():
#     DataFrameDict[key] = df_mobility[:][df_mobility.location_key == key]


# mean_dict = {elem : pd.DataFrame() for elem in unique_countries}
# for key in mean_dict.keys():
#     print('working on 2:', key)
#     mean_dict[key] = DataFrameDict[key].groupby(pd.PeriodIndex(DataFrameDict[key]['date'], freq="M"))['mobility_all'].mean()

# x = pd.DataFrame.from_dict(mean_dict)
# print(x.T)
# x=x.T

# print('here')
# x.to_csv('mobility_month_wise.csv')  

country_dict = {}
with open('index.csv', encoding='utf-8') as csvfile:
    csvReader = csv.reader(csvfile)
    for row in csvReader:
        if '_' not in str(row[0]):
            country_dict[row[0]] = row[5]
# print(country_dict)

data = []
with open('mobility_month_wise.csv') as csvFile:
    csvReader = csv.reader(csvFile)
    for row in csvReader:
        try:
            # print(country_dict[row[0]])
            row[0] = country_dict[row[0]]
            data.append(row)
        except:
            data.append(row)

with open('mobility_monthly.csv','w') as csvFile:
    csvWriter = csv.writer(csvFile, lineterminator='\n')
    for d in data:
        csvWriter.writerow(d)