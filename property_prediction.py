from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

proportion_columns = [
        '1 PERSON_PROPORTION',
        '2 PERSONS_PROPORTION',
        '3 PERSONS_PROPORTION',
        '4 OR MORE PERSONS_PROPORTION',
        'ATIKAMEKW_PROPORTION',
        'DENE_PROPORTION',
        'MI\'KMAQ_PROPORTION',
        'OJIBWAY_PROPORTION',
        'OJI-CREE_PROPORTION',
        'ITALIAN_PROPORTION',
        'PORTUGUESE_PROPORTION',
        'ROMANIAN_PROPORTION',
        'SPANISH_PROPORTION',
        'DANISH_PROPORTION',
        'DUTCH_PROPORTION',
        'GERMAN_PROPORTION',
        'NORWEGIAN_PROPORTION',
        'SWEDISH_PROPORTION',
        'YIDDISH_PROPORTION',
        'BOSNIAN_PROPORTION',
        'BULGARIAN_PROPORTION',
        'CROATIAN_PROPORTION',
        'CZECH_PROPORTION',
        'MACEDONIAN_PROPORTION',
        'POLISH_PROPORTION',
        'RUSSIAN_PROPORTION',
        'SERBIAN_PROPORTION',
        'SERBO-CROATIAN_PROPORTION',
        'SLOVAK_PROPORTION',
        'UKRAINIAN_PROPORTION',
        'LATVIAN_PROPORTION',
        'LITHUANIAN_PROPORTION',
        'ESTONIAN_PROPORTION',
        'FINNISH_PROPORTION',
        'HUNGARIAN_PROPORTION',
        'GREEK_PROPORTION',
        'ARMENIAN_PROPORTION',
        'TURKISH_PROPORTION',
        'AMHARIC_PROPORTION',
        'ARABIC_PROPORTION',
        'HEBREW_PROPORTION',
        'MALTESE_PROPORTION',
        'SOMALI_PROPORTION',
        'TIGRIGNA_PROPORTION',
        'BENGALI_PROPORTION',
        'GUJARATI_PROPORTION',
        'HINDI_PROPORTION',
        'KURDISH_PROPORTION',
        'PASHTO_PROPORTION',
        'PERSIAN (FARSI)_PROPORTION',
        'SINDHI_PROPORTION',
        'SINHALA (SINHALESE)_PROPORTION',
        'URDU_PROPORTION',
        'MALAYALAM_PROPORTION',
        'TAMIL_PROPORTION',
        'TELUGU_PROPORTION',
        'JAPANESE_PROPORTION',
        'KOREAN_PROPORTION',
        'CANTONESE_PROPORTION',
        'CHINESE, N.O.S._PROPORTION',
        'MANDARIN_PROPORTION',
        'LAO_PROPORTION',
        'KHMER (CAMBODIAN)_PROPORTION',
        'VIETNAMESE_PROPORTION',
        'ILOCANO_PROPORTION',
        'MALAY_PROPORTION',
        'TAGALOG (PILIPINO, FILIPINO)_PROPORTION',
        'AKAN (TWI)_PROPORTION',
        'SWAHILI_PROPORTION',
        'Break and Enter Commercial_PERCENT',
        'Break and Enter Residential/Other_PERCENT',
        'Mischief_PERCENT',
        'Other Theft_PERCENT',
        'Theft from Vehicle_PERCENT',
        'Theft of Bicycle_PERCENT',
        'Theft of Vehicle_PERCENT',
        'Vehicle Collision or Pedestrian Struck (with Fatality)_PERCENT',
        'Vehicle Collision or Pedestrian Struck (with Injury)_PERCENT'
        ]

# function to preprocess an input dataframe and return 
# the preprocessed dataframe
def preprocess_proportional_inf(df):
    max_droped_rows = 20000
    for col in proportion_columns:
        n_inf = np.count_nonzero(np.isinf(df[col]))
        if n_inf is not 0:
            if n_inf > max_droped_rows:
                df = df.drop(col, axis=1)
            else:
                df = df[~np.isinf(df[col])]
    return df

# return the dataframe that filter the outliers out
def drop_outliers(df, column):
    q1, q3 = df[column].quantile([0.25, 0.75]).values
    iqr = q3 - q1
    lower_bound, upper_bound = q1 - iqr*3, q3 + iqr*3
    return df[(lower_bound < df[column]) & (df[column] < upper_bound)]

# return all the features column those are planned to train
def list_proportion_cols(df):
    return [col for col in df.columns if col in proportion_columns]

# function to draw a heat map and save it as an Html file
def draw_prop_change_heatmap(df,name,drawing_value = 'Proportion of Change'):
    station_arr = df[['Latitude','Longitude',drawing_value]].values
    m = folium.Map([49.2827,-123.1207], zoom_start=10)
    vancouver_zoning_geojson = 'local-area-boundary.geojson'
    folium.GeoJson(
            vancouver_zoning_geojson,
            name='geojson',
            style_function=lambda feat: {
                'opacity': 0.3,
                'fillOpacity': 0,
                'weight': 2,
                'color': '#000000'
                }
            ).add_to(m)
    m.add_child(plugins.HeatMap(station_arr,radius=9))
    m.save(f'{name}.html')

# function to run LR on the data set combined-data-2006-2011-bound1200
# output:
#   train Mae & test Mae
def linear_regression():
    df = pd.read_pickle('combined-data-2006-2011-bound1200.zip')
    draw_prop_change_heatmap(df,'Propchange_2006_2011')
    df = preprocess_proportional_inf(df)
    df = drop_outliers(df, 'Proportion of Change')
    prop_change = df['Proportion of Change']
    df = df[list_proportion_cols]

    test_df = pd.read_pickle('combined-data-2011-2016-bound1200.zip')
    draw_prop_change_heatmap(test_df,'Propchange_2011_2016_real')

    test_df = preprocess_proportional_inf(test_df)
    test_df = drop_outliers(test_df, 'Proportion of Change')
    test_feature = test_df.drop('Proportion of Change',axis=1)
    test_prop_change = test_df['Proportion of Change']
    test_df = test_df[list_proportion_cols]

    reg = LinearRegression().fit(df,prop_change)
    y_pred = reg.predict(test_df)
    test_predict = test_feature.merge(pd.DataFrame(y_pred,columns=['Proportion of Change']),left_index=True, right_index=True)
    draw_prop_change_heatmap(test_predict,'Propchange_2011_2016_predicted')

    train_mae = mean_absolute_error(reg.predict(df),prop_change)
    test_mae = mean_absolute_error(test_prop_change, y_pred)
    print(f'train_mae = {train_mae}, test_mae = {test_mae}')

# function to run RF on the data combined-data-2006-2011-bound1200 set at trees = 10, 20, 30 ... , 90
# output:
#   train Mae & test Mae
def random_forest_regression():
    df = pd.read_pickle('combined-data-2006-2011-bound1200.zip')
    draw_prop_change_heatmap(df,'RF_Propchange_2006_2011')
    df = preprocess_proportional_inf(df)
    df = drop_outliers(df, 'Proportion of Change')
    prop_change = df['Proportion of Change']
    df = df[list_proportion_cols]

    test_df = pd.read_pickle('combined-data-2011-2016-bound1200.zip')
    draw_prop_change_heatmap(test_df,'RF_Propchange_2011_2016_real')

    test_df = preprocess_proportional_inf(test_df)
    test_df = drop_outliers(test_df, 'Proportion of Change')
    test_feature = test_df.drop('Proportion of Change',axis=1)
    test_prop_change = test_df['Proportion of Change']
    test_df = test_df[list_proportion_cols]

    train_mae_arr = []
    test_mae_arr = []
    n_tree = range(10,100,10)
    for i in n_tree:
        regressor = RandomForestRegressor(n_estimators = i, random_state=0,n_jobs=-1)
        regressor.fit(df,prop_change)
        y_pred = regressor.predict(test_df)
        test_predict = test_feature.merge(pd.DataFrame(y_pred,columns=['Proportion of Change']),left_index=True, right_index=True)
        draw_prop_change_heatmap(test_predict,'RF_Propchange_2011_2016_predicted')

        train_mae = mean_absolute_error(regressor.predict(df),prop_change)
        test_mae = mean_absolute_error(test_prop_change, y_pred)
        train_mae_arr.append(train_mae)
        test_mae_arr.append(test_mae)
        print(f'train_mae = {train_mae}, test_mae = {test_mae}')
    plt.plot(train_mae_arr,n_tree,color='green',marker="-",label="train mae")
    plt.plot(test_mae_arr,n_tree,color='orange',marker="-",label="test mae")
    plt.legend()
    plt.show()

prediction = pd.read_pickle('rf_prediction.zip')
draw_prop_change_heatmap(prediction,'prediction','Predicted Value Change')