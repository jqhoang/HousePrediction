import pandas as pd
import json
import census_get_data as cgd
import matplotlib as plt

raw_df = pd.read_csv('local-area-boundary.csv',sep=";")
prop_adr = pd.read_csv('property-addresses.csv',sep=";")
# function to change the geocode to the matching region
def find_region(x,y):
    for i in range(0,raw_df.shape[0]):
        polygon = json.loads(raw_df['Geom'][i])['coordinates'][0]
        if is_in_region(x,y,polygon):
            return raw_df['Name'][i]

# function to check if the geocode is in the polygon (region)
def is_in_region(x,y,polygon):
    # Find if a location is in polygon area by using Even–odd rule
    num = len(polygon)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        # find Δx and Δy
        delta_x = polygon[j][0] - polygon[i][0]
        delta_y = polygon[j][1] - polygon[i][1]
        # find if x hit the line between point i and j (if true -> hit)
        if ((polygon[i][1] > y) != (polygon[j][1] > y)) and \
            (x < polygon[i][0] + (delta_x * (y-polygon[i][1])/delta_y)):
                c = not c
                
        # set j to find the next line
        j = i
    return c

# to check the accuracy of checking regions function
def create_wrong_dataFrame():
    full = prop_adr.shape[0]
    correct = 0
    data = pd.read_pickle('guessed_region.zip')
    wrong_df = pd.DataFrame({"correct":[],"guessed":[]})
    for i in range(0,int(prop_adr.shape[0])):
        print(f'Scanned {i} of {full}')
        loc = json.loads(prop_adr['Geom'][i])['coordinates']
        guessed_region = data['guessed'][i]
        correct +=  guessed_region == prop_adr['Geo Local Area'][i]
        if find_region(loc[0],loc[1]) != prop_adr['Geo Local Area'][i]:
            print(prop_adr['Geo Local Area'][i])
            return
            df = pd.DataFrame({"correct":[prop_adr['Geo Local Area'][i]],"guessed":[guessed_region]})
            wrong_df = wrong_df.append(df,ignore_index=True)
    wrong_df.to_pickle('./wrong_interprete.zip')
    print(f'precision = {correct/full*100}%')
    
# use to create the dataframe for spot and region
def create_guessed_dataframe():
    full = prop_adr.shape[0]
    guessed_df = pd.DataFrame({"guessed":[]})
    for i in range(0,int(prop_adr.shape[0])):
        print(f'Scanned {i} of {full}')
        loc = json.loads(prop_adr['Geom'][i])['coordinates']
        guessed_region = find_region(loc[0],loc[1])
        df = pd.DataFrame({"guessed":[guessed_region]})
        guessed_df = guessed_df.append(df,ignore_index=True)
    guessed_df.to_pickle('./guessed_region.zip')

# to read all the locations are misclassified(regions)
def read_wrongData():
    data = pd.read_pickle('wrong_interprete.zip')
    count= 0
    print(data)
    for i in range(data.shape[0]):
        if data['correct'][i] == 'Hastings-Sunrise':
            count+=1
    print(count)

# function to create dataframe that contains latitude and longitude
def get_information(data):
    if 'Geo Local Area' in data.keys():
        region = data['Geo Local Area']
    else:
        region = find_region(data['Latitude'],data['Longitude'])
    df = cgd.get_data_year(data['TAX_ASSESSMENT_YEAR'])
    return df.loc[region,:],region

# function to rename the dataframe columns for connecting to other dataframe
def get_delta(data):
    if 'Geo Local Area' in data.keys():
        region = data['Geo Local Area']
    else:
        region = find_region(data['Latitude'],data['Longitude'])
    df = cgd.get_delta_year(data['TAX_ASSESSMENT_YEAR'])
    df.rename(columns={ 'year':'TAX_ASSESSMENT_YEAR',
                        'region':'Geo Local Area'}, inplace=True)
    return df.loc[region,:],region

# function to return the dataframe of region, year and census data
def query_census_data(df, merge=False):
    all_data_year = cgd.get_data_year_all()
    all_data_year.rename(columns={  'year':'TAX_ASSESSMENT_YEAR',
                                    'region':'Geo Local Area'}, inplace=True)
    if merge:
        return df.merge(all_data_year)
    return all_data_year

# function to return the dataframe of the change of census 
def query_delta_data(df):
    query_df = pd.DataFrame()
    for i in range(df.shape[0]):
        print(f'{i}/{df.shape[0]}')
        query, region= get_delta(df.loc[i])
        query['region'] = region
        query_df = query_df.append(query)
    return df.merge(query_df)

# function to get the dataframe of change of year=????
def get_delta_year(year,flat=False):
    return cgd.get_delta_year(year,flat)

# function to create a pickle for census data 
def create_census_property_pickle():
    data = pd.read_pickle('3.geocoded-data.zip')
    df = query_census_data(data)
    df.to_pickle('./census_prop.zip')
    df = query_census_data(data,True)
    df.to_pickle('./census_prop_merged.zip')

# function to create pickles for proportion and 
def create_delta_pickle():
    df1 = get_delta_year(2006)
    df2 = get_delta_year(2011)
    df1.to_pickle('./delta_2006_2011_table.zip')
    df2.to_pickle('./delta_2011_2016_table.zip')
    df3 = get_delta_year(2006,True)
    df4 = get_delta_year(2011,True)
    df3.to_pickle('./delta_2006_2011_flat_table.zip')
    df4.to_pickle('./delta_2011_2016_flat_table.zip')
    df5 = pd.concat([df3.drop('REGION',axis=1),df1],axis=1)
    df6 = pd.concat([df4.drop('REGION',axis=1),df2],axis=1)
    df5.to_pickle('./delta_2006_2011_merged_table.zip')
    df6.to_pickle('./delta_2011_2016_merged_table.zip')

# function to get the census and property values dataframe
def get_census_property_info():
    return pd.read_pickle('census_prop.zip')

# function to get the change of census between year 2006 and 2011
def get_delta_year_2006_2011():
    return pd.read_pickle('delta_2006_2011_table.zip')

# function to get the change of census between year 2011 and 2016
def get_delta_year_2011_2016():
    return pd.read_pickle('delta_2011_2016_table.zip')

# function to get the change of census between year 2006 and 2011 (merged to year)
def get_delta_merge_2006_2011():
    return pd.read_pickle('delta_2006_2011_merged_table.zip')

# function to get the change of census between year 2011 and 2016 (merged to year)
def get_delta_merge_2011_2016():
    return pd.read_pickle('delta_2011_2016_merged_table.zip') 

# function to get the change of census between year 2006 and 2011 (merged to year)
def get_delta_flat_2006_2011():
    return pd.read_pickle('delta_2006_2011_flat_table.zip')

create_delta_pickle()