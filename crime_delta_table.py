from math import sin, cos, sqrt, atan2, radians
import math
import numpy as np
import pandas as pd
from pyproj import Proj

##Read in crime data
crime_data = pd.read_csv("crimedata_csv_all_years.csv")
crime_data = crime_data[['TYPE','YEAR','HUNDRED_BLOCK','X','Y']]

##Drop rows that contain an a non-number value, these columns are essential
crime_data.dropna(0, inplace = True)

##2006/2011/2016 are the only years census data was released, therefore only crimes are only considered if they are in these years
in_relevant_years = crime_data['YEAR'].isin([2006, 2011, 2016])
crime_data = crime_data.loc[in_relevant_years]

##Grab the coordinates of each crime, they are in the UTM format
utmxy = crime_data[['X','Y']]

##Convert UTM coordinates to regular coordinates
myProj = Proj("+proj=utm +zone=10K, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

lon, lat = myProj(utmxy['X'].values, utmxy['Y'].values, inverse=True)

##Recreate crime dataframe with regular coordinates
crime_data_relevant = crime_data[['TYPE','YEAR','HUNDRED_BLOCK']]
crime_data_relevant['X'] = lon
crime_data_relevant['Y'] = lat



##Rename year to match property tax report column name for year
crime_data_relevant.rename(columns = {'YEAR': 'TAX_ASSESSMENT_YEAR'}, inplace=True)

##Filter out crimes that have a "hidden" location, these usually involved homicide type crimes
not_hidden_crimes = ~crime_data['Y'].isin([0.0, 0])
crime_data_relevant = crime_data_relevant.loc[not_hidden_crimes]

##Convienience variable to hold the types of crime in dataset
categories_of_crime = crime_data_relevant['TYPE'].unique()

##Read in property tax report data
property_coords = pd.read_pickle('../prop_tax_ml/prop_tax_proj/data/3.geocoded-data.zip')


##Variables involved in converting meters to longitude/latitude changes
meter_to_coord = 111111
vancouver_city_block = 1600
print("Creating boundaries...")

##Create boundaries around the properties in the tax report, these boundaries will define if a crime "belongs" to a property
##Columns include property ID, longitude boundaries, latitude boundaries, year, street name, and civic number
property_coords_with_boundaries = pd.DataFrame(property_coords['PID'])
property_coords_with_boundaries['Longitude 1'] = property_coords['Longitude'] - (vancouver_city_block/(meter_to_coord * np.cos(property_coords['Latitude'])))
property_coords_with_boundaries['Longitude 2'] = property_coords['Longitude'] + (vancouver_city_block/(meter_to_coord * np.cos(property_coords['Latitude'])))
property_coords_with_boundaries['Latitude 1'] = property_coords['Latitude'] - (vancouver_city_block/meter_to_coord)
property_coords_with_boundaries['Latitude 2'] = property_coords['Latitude'] + (vancouver_city_block/meter_to_coord)
property_coords_with_boundaries['TAX_ASSESSMENT_YEAR'] = property_coords['TAX_ASSESSMENT_YEAR']
property_coords_with_boundaries['STREET_NAME'] = property_coords['STREET_NAME']
property_coords_with_boundaries['TO_CIVIC_NUMBER'] = property_coords['TO_CIVIC_NUMBER']
##Initialize every property to have 0 crimes of all types in the crime dataset, this also creates for each property a column of every category of crime
for category_of_crime in categories_of_crime:
  property_coords_with_boundaries[category_of_crime] = np.zeros(property_coords_with_boundaries.shape[0])
for category_of_crime in categories_of_crime:
  property_coords_with_boundaries[category_of_crime + "_PERCENT"] = np.zeros(property_coords_with_boundaries.shape[0])

print("Done creation")

print("Starting boundaries...")

##Determine which property every crime "belongs" to based on longitude and latitude of crime falling into longitude latitude boundaries of property
for prop_index, prop_row in property_coords_with_boundaries.iterrows():
  relevant_crimes = crime_data_relevant[(crime_data_relevant['TAX_ASSESSMENT_YEAR'] == prop_row['TAX_ASSESSMENT_YEAR']) &
                                        (crime_data_relevant['X'] >= prop_row['Longitude 1']) &
                                        (crime_data_relevant['X'] <= prop_row['Longitude 2']) &
                                        (crime_data_relevant['Y'] >= prop_row['Latitude 1']) &
                                        (crime_data_relevant['Y'] <= prop_row['Latitude 2'])]
  ##If the property has crimes, count how many of each type happened and overwrite the 0 value
  if not relevant_crimes.empty:
    relevant_crimes_value_counts = relevant_crimes['TYPE'].value_counts()
    for type_of_crime, count in relevant_crimes_value_counts.iteritems():
      property_coords_with_boundaries.at[prop_index, type_of_crime] = count

##Now that we have counts of crimes of each type for each property, we create deltas of crime, because we are interested in the delta of property value
##We group properties by the necessary columns to constitute unique identity, some properties have the same PID but different locations, creating
##very different evaluations thus we ensure that each evaluation of a property is exactly the same property by combining address as well.
##After grouping every item in crime_sections will be a property and its deltas for crime for 2006/2011/2016

crime_sections = property_coords_with_boundaries.groupby(['PID','STREET_NAME', 'TO_CIVIC_NUMBER'])
print("Finished boundaries")
print("Starting deltas...")
crime_deltas_2006_2011 = []
crime_deltas_2011_2016 = []
crime_deltas_2006_2011_percentages = []
crime_deltas_2011_2016_percentages = []
for key, item in crime_sections:
    ##For each property grab the row assosicated with each relevant year, so for property 1, we grab its row for 2006, for 2011, and for 2016
    item2006 = item.loc[item['TAX_ASSESSMENT_YEAR'] == 2006]
    item2011 = item.loc[item['TAX_ASSESSMENT_YEAR'] == 2011]
    item2016 = item.loc[item['TAX_ASSESSMENT_YEAR'] == 2016]
    ##Every property is guaranteed to have a value for 2011, 2006 and 2016 may not have values
    val2011 = np.array([item2011[category].values[0] for category in categories_of_crime])
    if not item2006.empty:
        val2006 = np.array([item2006[category].values[0] for category in categories_of_crime])
        delta_2006_2011 = val2011-val2006
        delta_2006_2011_percent = (val2011-val2006)/val2006
        delta_row = [item2011['PID'].values[0], item2011['Longitude 1'].values[0], item2011['Longitude 2'].values[0], item2011['Latitude 1'].values[0], item2011['Latitude 2'].values[0], item2011['TAX_ASSESSMENT_YEAR'].values[0], item2011['STREET_NAME'].values[0], item2011['TO_CIVIC_NUMBER'].values[0], *delta_2006_2011, *delta_2006_2011_percent]
        crime_deltas_2006_2011.append(delta_row)
    if not item2016.empty:
        val2016 = np.array([item2016[category].values[0] for category in categories_of_crime])
        delta_2011_2016 = val2016-val2011
        delta_2011_2016_percent = (val2016-val2011)/val2011 
        delta_row = [item2011['PID'].values[0], item2011['Longitude 1'].values[0], item2011['Longitude 2'].values[0], item2011['Latitude 1'].values[0], item2011['Latitude 2'].values[0], item2011['TAX_ASSESSMENT_YEAR'].values[0], item2011['STREET_NAME'].values[0], item2011['TO_CIVIC_NUMBER'].values[0], *delta_2011_2016, *delta_2011_2016_percent]

        crime_deltas_2011_2016.append(delta_row)

print("Finished deltas")

crime_deltas_df_2006_2011 = pd.DataFrame(crime_deltas_2006_2011, columns= property_coords_with_boundaries.columns)
crime_deltas_df_2011_2016 = pd.DataFrame(crime_deltas_2011_2016, columns= property_coords_with_boundaries.columns)
print(crime_deltas_df_2006_2011.to_string())
print(crime_deltas_df_2011_2016.to_string())
print("Pickling...")
crime_deltas_df_2006_2011.to_pickle('./crime_deltas_2006_2011_1600_new.zip')
crime_deltas_df_2011_2016.to_pickle('./crime_deltas_2011_2016_1600_new.zip')


