import pandas as pd

# function to load the data from csv files
def load_csv_files():
    language2006_df = pd.read_csv("CensusTotalPopByMT2006.csv",index_col=[0],engine="python",header=0)
    language2011_df = pd.read_csv("CensusTotalPopByMT2011.csv",index_col=[0],engine="python",header=0)
    language2016_df = pd.read_csv("CensusTotalPopByMT2016.csv",index_col=[0],engine="python",header=0)
    household2006_df = pd.read_csv("censusPopulationWithNumberPplPerHh2006.csv",index_col=[0],engine="python",header=0)
    household2011_df = pd.read_csv("censusPopulationWithNumberPplPerHh2011.csv",index_col=[0],engine="python",header=0)
    household2016_df = pd.read_csv("censusPopulationWithNumberPplPerHh2016.csv",index_col=[0],engine="python",header=0)
    return [language2006_df, language2011_df, language2016_df, household2006_df, household2011_df, household2016_df]

# function to edit the columns name(trim the string), and add a columns (year)
def rename_and_replace_column(dataframe_list):
    # trim the space of the string and make the rows the columns
    language2006_df = dataframe_list[0].replace(' -   ',0).transpose()
    language2011_df = dataframe_list[1].replace(' -   ',0).transpose()
    language2016_df = dataframe_list[2].replace(' -   ',0).transpose()
    household2006_df = dataframe_list[3].replace(' -   ',0).transpose()
    household2011_df = dataframe_list[4].replace(' -   ',0).transpose()
    household2016_df = dataframe_list[5].replace(' -   ',0).transpose()
    # drop the last two column (total of people in vancouver)
    language2006_df.drop(language2006_df.tail(2).index, inplace=True)
    language2011_df.drop(language2011_df.tail(2).index, inplace=True)
    language2016_df.drop(language2016_df.tail(2).index, inplace=True)
    household2006_df.drop(household2006_df.tail(2).index, inplace=True)
    household2011_df.drop(household2011_df.tail(2).index, inplace=True)
    household2016_df.drop(household2016_df.tail(2).index, inplace=True)
    # trim all space in the columns' names and rows in census tables
    household2006_df.columns = household2006_df.columns.str.strip()
    household2011_df.columns = household2011_df.columns.str.strip()
    household2016_df.columns = household2016_df.columns.str.strip()
    household2006_df.index = household2006_df.index.str.strip()
    household2011_df.index = household2011_df.index.str.strip()
    household2016_df.index = household2016_df.index.str.strip()
    # trim all space in the columns' names and rows in mother tounge tables
    # add the year column in the table
    language2006_df.columns = language2006_df.columns.str.strip()
    language2006_df.index = language2006_df.index.str.strip()
    language2006_df['year'] = 2006
    language2011_df.columns = language2011_df.columns.str.strip()
    language2011_df.index = language2011_df.index.str.strip()
    language2011_df['year'] = 2011
    language2016_df.columns = language2016_df.columns.str.strip()
    language2016_df.index = language2016_df.index.str.strip()
    language2016_df['year'] = 2016
    return [language2006_df, language2011_df, language2016_df, household2006_df, household2011_df, household2016_df]

# function to merge the dataframe for ethinicity and number of people in a private household
def combine_data_per_year(dataframe_list):
    data2006 = pd.concat([dataframe_list[3],dataframe_list[0]],axis=1,sort=False)
    data2011 = pd.concat([dataframe_list[4],dataframe_list[1]],axis=1,sort=False)
    data2016 = pd.concat([dataframe_list[5],dataframe_list[2]],axis=1,sort=False)
    return data2006, data2011, data2016

# function to combine all the dataframe together
def combine_all_table(d2006, d2011, d2016):
    all_data = pd.concat([d2006,d2011],axis=0,sort=False)
    all_data = pd.concat([all_data,d2016],axis = 0,sort=False)
    return all_data

# function to read all dataframes from the pickle files
def extract_all_data():
    data2006 = pd.read_pickle('data2006.zip')
    data2011 = pd.read_pickle('data2011.zip')
    data2016 = pd.read_pickle('data2016.zip')
    all_data = pd.read_pickle('all_data.zip')

    common_list = []
    for col in data2006.columns:
        if col in data2011.columns:
            if col in data2016.columns:
                common_list.append(col)
    return data2006, data2011, data2016, all_data, common_list

# function to create pickle files for all dataframe
def make_all_data_file():
    raw_data = load_csv_files()
    df_array = rename_and_replace_column(raw_data)
    data2006, data2011, data2016 = combine_data_per_year(df_array)
    all_data = combine_all_table(data2006, data2011, data2016)
    data2006.to_pickle('./data2006.zip')
    data2011.to_pickle('./data2011.zip')
    data2016.to_pickle('./data2016.zip')
    all_data.to_pickle('./all_data.zip')

make_all_data_file()