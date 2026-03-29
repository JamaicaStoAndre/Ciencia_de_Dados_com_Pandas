import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
import json
from shapely.geometry import shape, Point, Polygon
import folium
from colour import Color
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime


FACTOR = 1.032


def parse_dms(coor: str) -> float:
    ''' Transforms strings of degrees, minutes and seconds to a decimal value
    
    Args:
        coor (str): String containing degrees in DMS format
        
    Returns:
        dec_coord (float): coordinates as a decimal value
    '''
    parts = re.split('[^\d\w]+', coor)
    degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2]+'.'+parts[3])
    direction = parts[4]
    
    dec_coord = degrees + minutes / 60 + seconds / (3600)
    
    if direction == 'S' or direction == 'W':
        dec_coord *= -1
    
    return dec_coord


#-=-=--=Início: Criar grade com valores dos sensores
def predict_on_bogota(model: KNeighborsRegressor, n_points: int=64) -> Tuple[pd.DataFrame, float, float]:
    ''' Cria uma grade de valores previstos de poluentes com base nas estações vizinhas.
    
    Args:
        model (KNeighborsRegressor): Modelo a ser usado.
        n_points (int): Número de pontos na grade.
        
    Retorna:
        Tuple[pd.DataFrame, float, float]: Um DataFrame contendo tuplas de coordenadas e valor previsto,
                                           tamanho da grade em latitude e longitude.
    '''
    with open('data/bogota.json') as f:
        js = json.load(f)

    # Verifica cada polígono para ver se ele contém o ponto.
    polygon = Polygon(shape(js['features'][0]['geometry']))
    (lon_min, lat_min, lon_max, lat_max) = polygon.bounds

    # Calcula os incrementos de latitude e longitude para a grade.
    dlat = (lat_max - lat_min) / (n_points - 1)
    dlon = (lon_max - lon_min) / (n_points - 1)
    lat_values = np.linspace(lat_min - dlat, lat_max + dlat, n_points)
    lon_values = np.linspace(lon_min - dlon, lon_max + dlon, n_points)

    predictions = []

    # Itera sobre a grade para fazer previsões.
    for i in range(n_points):
        for j in range(n_points):
            if polygon.contains(Point(lon_values[j], lat_values[i])):
                point = [lat_values[i], lon_values[j]]
                # Remove os dados da mesma estação.
                pred = model.predict([point])
                predictions.append([lat_values[i], lon_values[j], pred[0][0]])

    # Converte as previsões para um DataFrame do Pandas.
    predictions_df = pd.DataFrame(predictions, columns=['Latitude', 'Longitude', 'Prediction'])

    return predictions_df, dlat, dlon

#-=-==-=FIM: Criar grade com valores dos sensores

#-=-=-=----Início do Heat Map
def create_heat_map(predictions_df, df_day: pd.DataFrame, dlat: float, dlon: float, target_pollutant='PM2.5', popup_plots=False) -> folium.Map:
    # Cria o mapa
    lat_center = np.average(predictions_df['Latitude'])
    lon_center = np.average(predictions_df['Longitude'])

    map_hooray = folium.Map(location=[lat_center, lon_center], zoom_start=11) 

    # Cria recursos retangulares para o mapa mostrando a poluição interpolada entre as estações
    for row in predictions_df.itertuples():
        # Aqui usamos os valores da linha do DataFrame
        lat, lon, prediction = row.Latitude, row.Longitude, row.Prediction
        color = color_producer(target_pollutant, prediction)
        folium.Rectangle(
            bounds=[
                (lat - dlat * FACTOR / 2, lon - dlon * FACTOR / 2),
                (lat + dlat * FACTOR / 2, lon + dlon * FACTOR / 2)
            ],
            color=color,
            stroke=False,
            fill=True,
            fill_color=color,
            fill_opacity=0.5,
            popup=f'{"{:.2f}".format(prediction)}'
        ).add_to(map_hooray)

    # Adiciona recursos circulares para mostrar as estações no mapa
    fg = folium.FeatureGroup(name='Stations')
    for index, station in df_day.iterrows():
        # Código para adicionar círculos para cada estação
        ...
    map_hooray.add_child(fg)

    return map_hooray

#-=-=------Fim do Heat Map

def calculate_mae_for_k(
    data: pd.core.frame.DataFrame,
    k: int=1,
    target_pollutant: str='PM2.5'
) -> float:
    ''' Calculates the MAE for k nearest neighbors
    
    Args:
        data (pd.core.frame.DataFrame): dataframe with data.
        k (int): number of neighbors to use for interpolation
        target_pollutant (str): pollutant for which to show the heatmap

    Returns:
        MAE (float): The MAE value
    '''    
    # Drop all the rows with the stations where the data imputation didnt perform well
    bad_stations = ['7MA', 'CSE', 'COL', 'MOV2']
    df2 = data.drop(data[data['Station'].isin(bad_stations)].index)

    # Drop all the rows where there is imputed data, so the calculation is only done on real data
    # df2 = data[data[[c for c in data.columns if 'flag' in c]].isnull().all(axis=1)]
    
    # Take a sample of the data (so that the notebook runs faster)
    df2 = df2.sample(frac=0.2, random_state=8765)
    df2.insert(0, 'time_discriminator', (df2['DateTime'].dt.dayofyear * 10000 + df2['DateTime'].dt.hour * 100).values, True)
    
    predictions = []
    stations = data['Station'].unique()
    for station in stations:
        df_day_station = df2.loc[df2['Station'] == station]
        if len(df_day_station) > 0:
            df_day_no_station = df2.loc[df2['Station'] != station]
            if len(df_day_no_station) >= k:
                neigh = KNeighborsRegressor(n_neighbors=k, weights = 'distance', metric='sqeuclidean')
                knn_model = neigh.fit(
                    df_day_no_station[['Latitude', 'Longitude', 'time_discriminator']],
                    df_day_no_station[[target_pollutant]]
                )
                prediction = knn_model.predict(df_day_station[['Latitude', 'Longitude', 'time_discriminator']])
                if len(predictions)==0:
                    predictions = np.array([df_day_station[target_pollutant].values, prediction[:,0]]).T
                else:
                    predictions = np.concatenate(
                        (predictions, np.array([df_day_station[target_pollutant].values, prediction[:,0]]).T),
                        axis=0
                    )

    predictions = np.array(predictions)
    MAE = mean_absolute_error(predictions[:,0],predictions[:,1])
    
    return MAE


#-=-Inicio heat Map date Range
def create_heat_map_with_date_range(
    df: pd.core.frame.DataFrame,
    start_date: datetime,
    end_date: datetime,
    k_neighbors: int=1,
    target_pollutant: str='PM2.5',
    distance_metric: str='sqeuclidean'
) -> folium.Map:
    ''' 
    Cria um mapa de calor com base nos valores preditos de poluentes das estações vizinhas.
    
    Args:
        df: DataFrame com os dados.
        start_date: Data de início para mostrar o mapa de calor.
        end_date: Data final para mostrar o mapa de calor.
        k_neighbors: Número de vizinhos para usar na interpolação.
        target_pollutant: Poluente para o qual mostrar o mapa de calor.
        distance_metric: Métrica para calcular a distância entre as estações.

    Retorna:
        Um mapa de calor no folium.Map.
    '''
    # Seleciona o intervalo de datas do DataFrame completo
    df_days = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date)]

    # Inicializa o modelo de regressão KNeighborsRegressor
    k_neighbors_model = KNeighborsRegressor(n_neighbors=k_neighbors, weights='distance', metric=distance_metric)

    # Lista para armazenar todas as features (elementos) da animação
    features = []

    # Itera sobre cada timestamp único dentro do intervalo de datas
    for timestamp in df_days['DateTime'].unique():
        # Filtra os dados para o dia e hora específicos
        df_day = df[df['DateTime'] == timestamp]
        day_hour = timestamp.strftime('%Y-%m-%dT%H:%M:%S')

        # Treina o modelo com os dados das estações, exceto a estação atual
        k_neighbors_model.fit(df_day[['Latitude', 'Longitude']], df_day[[target_pollutant]])

        # Gera previsões para a área de Bogotá e obtém dimensões da grade
        predictions_df, dlat, dlon = predict_on_bogota(k_neighbors_model, k_neighbors)

        # Cria retângulos para o mapa com base nas previsões
        for row in predictions_df.itertuples():
            rect = create_polygon(row, dlat, dlon, day_hour, target_pollutant)
            features.append(rect)

        # Cria círculos para as estações no mapa
        for index, station in df_day.iterrows():
            imputed_col = f'{target_pollutant}_imputed_flag'
            bg_color = 'black' if imputed_col in station and isinstance(station[imputed_col], str) else 'white'
            data = [station['Latitude'], station['Longitude'], station[target_pollutant]]
            circle = create_circle(data, day_hour, 13, target_pollutant, bg_color)
            features.append(circle)
            circle = create_circle(data, day_hour, 12, target_pollutant)
            features.append(circle)

    # Retorna a lista de features para serem adicionadas ao mapa
    return features

#-=-= Fim HeatMap

def color_producer(pollutant_type, pollutant_value):
    ''' This function returns colors based on the pollutant values to create a color representation of air pollution.    
    
    The color scale  for PM2.5 is taken from purpleair.com and it agrees with international guidelines
    The scale for other pollutants was created based on the limits for other pollutants to approximately
    correspond to the PM2.5 color scale. The values in the scale should not be taken for granted and
    are used just for the visualization purposes.
    
    Args:
        pollutant_type (str): Type of pollutant to get the color for
        pollutant_value (float): Value of polutant concentration
        
    Returns:
        pin_color (str): The color of the bucket
    '''
    all_colors_dict = {
        'PM2.5': {0: 'green', 12: 'yellow', 35: 'orange', 55.4: 'red', 150: 'black'},
        'PM10': {0: 'green', 20: 'yellow', 60: 'orange', 110: 'red', 250: 'black'},
        'CO': {0: 'green', 4: 'yellow', 10: 'orange', 20: 'red', 50: 'black'},
        'OZONE': {0: 'green', 60: 'yellow', 100: 'orange', 200: 'red', 300: 'black'},
        'NOX': {0: 'green', 40: 'yellow', 80: 'orange', 160: 'red', 300: 'black'},
        'NO': {0: 'green', 40: 'yellow', 80: 'orange', 160: 'red', 300: 'black'},
        'NO2': {0: 'green', 20: 'yellow', 40: 'orange', 80: 'red', 200: 'black'},
    }
    
    # Select the correct color scale, if it is not available, choose PM2.5
    colors_dict = all_colors_dict.get(pollutant_type, all_colors_dict['PM2.5'])
    thresholds = sorted(list(colors_dict.keys()))
    
    previous = 0
    for threshold in thresholds:
        if pollutant_value < threshold:
            bucket_size = threshold - previous
            bucket = (pollutant_value - previous) / bucket_size
            colors = list(Color(colors_dict[previous]).range_to(Color(colors_dict[threshold]), 11))
            pin_color = str(colors[int(np.round(bucket*10))])
            return pin_color
        previous = threshold


def create_polygon(
    p: List[float],
    dlat: float,
    dlon: float,
    time: datetime,
    pollutant: str
) -> Dict[str, Any]:
    ''' Given the parameters it creates a dictionary with information for the polygon feature.
    
    Args:
        p (List[float]): list of coordinates 
        dlat (float): latitude size of grid
        dlon (float): longitudinal size of grid
        time (datetime): time for which the polygon is valid
        pollutant (str): pollutant which the polygon represents
        
    Returns:
        feature (Dict[str, Any]): dictionary of the feature properties.
    '''
    # Create a polygon feature for the map
    feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[p[1] - dlon * FACTOR / 2, p[0] - dlat * FACTOR / 2], 
                                [p[1] - dlon * FACTOR / 2, p[0] + dlat * FACTOR / 2],  
                                [p[1] + dlon * FACTOR / 2, p[0] + dlat * FACTOR / 2],  
                                [p[1] + dlon * FACTOR / 2, p[0] - dlat * FACTOR / 2], 
                                [p[1] - dlon * FACTOR / 2, p[0] - dlat * FACTOR / 2]]],

            },
            'properties': {
                'times': [time], 
                'style': {
                    'color': color_producer(pollutant, p[2]), 
                    'stroke': False,
                    'fillOpacity': 0.4
                }
            }
    }
    return feature


def create_circle(
    p: List[float],
    day_hour: datetime,
    radius: float,
    pollutant: str,
    color: Optional[str]=None
) -> Dict[str, Any]:
    ''' Given the parameters it creates a dictionary with information for the circle feature.
    
    Args:
        p (List[float]): list of coordinates 
        day_hour (datetime): time for which the polygon is valid
        radius (float): size of the circle
        pollutant (str): pollutant which the polygon represents
        color (Optional[str]): color of the circle
        
    Returns:
        feature (Dict[str, Any]): dictionary of the feature properties.
    '''
    if color is None:
        color = color_producer(pollutant, p[2])
    
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [p[1], p[0]],
        },
        'properties': {
            'time': day_hour,
            'icon': 'circle',
            'iconstyle': {
                'fillColor': color,
                'fillOpacity': 1,
                'stroke': 'false',
                'radius': radius,
            },
            'style': {'weight': 0},
        },
    }
    return feature
