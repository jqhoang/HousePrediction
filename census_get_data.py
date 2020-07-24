import pandas as pd
import combine_census_data as cc_data
import math

# get all 3 years census dataframe
def get_data_year_all():
    data2006, data2011, data2016, all_data, common_list = cc_data.extract_all_data()
    all_data['region'] = all_data.index
    common_list.append('region')
    return all_data.loc[:,common_list]

# get 2006 census dataframe
def get_data_year_2006():
    data2006, data2011, data2016, all_data, common_list = cc_data.extract_all_data()
    return data2006.loc[:,common_list]

# get 2011 census dataframe
def get_data_year_2011():
    data2006, data2011, data2016, all_data, common_list = cc_data.extract_all_data()
    return data2011.loc[:,common_list]

# get 2016 census dataframe
def get_data_year_2016():
    data2006, data2011, data2016, all_data, common_list = cc_data.extract_all_data()
    return data2016.loc[:,common_list]

def get_data_year(year):
    data2006, data2011, data2016, all_data, common_list = cc_data.extract_all_data()
    if year==2006:
        return data2006.loc[:,common_list]
    elif year==2011:
        return data2011.loc[:,common_list]
    return data2016.loc[:,common_list]

# get delta census dataframe between year 2006 and 2011
def get_delta_year_2006_2011(flat):
    data_year_2006 = get_data_year_2006().apply(pd.to_numeric)
    data_year_2011 = get_data_year_2011().apply(pd.to_numeric)
    suffix = ""
    if flat:
        result = ((data_year_2011 - data_year_2006)).drop(['year'],axis=1)
        suffix = "_FLAT"
    else:
        result = ((data_year_2011 - data_year_2006)/data_year_2006).drop(['year'],axis=1).replace([math.nan,math.inf],[0,math.nan])
        suffix = "_PROPORTION"
    result.columns = (result.columns + suffix).str.upper() 
    result['REGION'] = result.index
    return result

# get delta census dataframe between year 2011 and 2016
def get_delta_year_2011_2016(flat):
    data_year_2011 = get_data_year_2011().apply(pd.to_numeric)
    data_year_2016 = get_data_year_2016().apply(pd.to_numeric)
    suffix = ""
    if flat:
        result = ((data_year_2016 - data_year_2011)).drop(['year'],axis=1)
        suffix = "_FLAT"
    else:    
        result = ((data_year_2016 - data_year_2011)/data_year_2011).drop(['year'],axis=1).replace([math.nan,math.inf],[0,math.nan])
        suffix = "_PROPORTION"
    result.columns = (result.columns + suffix).str.upper() 
    result['REGION'] = result.index
    return result
# get delta census dataframe between year 2006 and 2016
def get_delta_year_2006_2016(flat):
    data_year_2006 = get_data_year_2011().apply(pd.to_numeric)
    data_year_2016 = get_data_year_2016().apply(pd.to_numeric)
    if flat:
        result = ((data_year_2016 - data_year_2006)).drop(['year'],axis=1)
        suffix = "_FLAT"
    else:
        result = ((data_year_2016 - data_year_2006)/data_year_2006).drop(['year'],axis=1).replace([math.nan,math.inf],[0,math.nan])
        suffix = "_PROPORTION"
    result.columns = (result.columns + suffix).str.upper() 
    result['region'] = result.index
    return result

def get_delta_year(year,flat=False):
    if year == 2006:
        return get_delta_year_2006_2011(flat)
    else:
        return get_delta_year_2011_2016(flat)
