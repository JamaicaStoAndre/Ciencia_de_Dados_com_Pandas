import numpy as np
import pandas as pd
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns

import ipywidgets as widgets
from ipywidgets import interact
import folium 
from colour import Color
from collections import defaultdict

from typing import List


# This is a list of categorical variables
categorical_variables = ['Station']
# This is a list of all pollutants
pollutants_list = ['PM2.5', 'PM10',  'NO', 'NO2', 'NOX', 'CO', 'OZONE']

FONT_SIZE_TICKS = 12
FONT_SIZE_TITLE = 20
FONT_SIZE_AXES = 16


# Functions below are directly called in the notebook

def create_correlation_matrix(
    raw_data: pd.core.frame.DataFrame,
    pollutants_list: List[str],
):
    """Creates a correlation matrix of the features.

    Args:
        raw_data (pd.core.frame.DataFrame): The data used.
        pollutants_list (List[str]): List of features to include in the plot.
    """
    plt.figure(figsize=(10,10))
    sns.heatmap(
        raw_data[pollutants_list].corr(),
        square=True,
        annot=True,
        cbar=False,
        cmap="RdBu",
        vmin=-1,
        vmax=1
    )
    plt.title('Correlation Matrix of Variables')

    plt.show()


def fix_dates(df: pd.core.frame.DataFrame, date_column: str) -> List[str]:
    '''Fixes the date format in the dataframe.

    Args:
        df (pd.core.frame.DataFrame): The dataframe.
        date_column (str): Column with dates
        
    Returns:
        fixed_dates (List[str]): list of corrected dates to be put into the dataframe
    '''
    dates = df[date_column]
    fixed_dates = []
    for row in dates:
        line = list(row)
        hour = int(''.join(line[11:13])) - 1
        fixed_dates.append("".join(line[:11] + [str(int(hour/10)) + str(int(hour % 10))] + line[13:]))
    return fixed_dates


def create_histogram_plot(df: pd.core.frame.DataFrame, bins: int):
    '''Creates an interactive histogram
    
    Args:
        df (pd.core.frame.DataFrame): The dataframe with the data.
        bins (int): number of bins for the histogram.
    
    '''
    def _interactive_histogram_plot(station, pollutant):
        data = df[df.Station==station]
        x = data[pollutant].values 
        try:
            plt.figure(figsize=(12,6))
            plt.xlabel(f'{pollutant} concentration', fontsize=FONT_SIZE_AXES)
            plt.ylabel('Number of measurements', fontsize=FONT_SIZE_AXES)
            plt.hist(x, bins=bins)
            plt.title(f'Pollutant: {pollutant} - Station: {station}', fontsize=FONT_SIZE_TITLE)
            plt.xticks(fontsize=FONT_SIZE_TICKS)
            plt.yticks(fontsize=FONT_SIZE_TICKS)
            plt.show()
        except ValueError:
            print('Histogram cannot be shown for selected values as there is no data')
    
    # Widget for picking the city
    station_selection = widgets.Dropdown(
        options=df.Station.unique(),
        description='Station'
    )

    # Widget for picking the continuous variable
    pollutant_selection = widgets.Dropdown(
        options=pollutants_list,
        description='Pollutant',
    )
    
    # Putting it all together
    interact(_interactive_histogram_plot, station=station_selection, pollutant=pollutant_selection);


def create_boxplot(df: pd.core.frame.DataFrame):
    '''Creates a boxplot of pollutant values for each sensor station
    
    Args:
        df (pd.core.frame.DataFrame): The dataframe with the data.
    
    '''
    labels = df[categorical_variables[0]].unique()
    
    def _interactive_boxplot(cat_var):
        medians = []
        for value in df[categorical_variables[0]].unique():
            median = 1000
            try:
                rows = df[cat_var].loc[df[categorical_variables[0]]==value]
                if rows.isnull().sum() != rows.shape[0]:
                    median = rows.median()
            except:
                print('Wrong')
            medians.append(median)
        orderInd = np.argsort(medians) 
        
        plt.figure(figsize=(17,7))
        scale = 'linear'
        plt.yscale(scale)
        sns.boxplot(data=df, y=cat_var, x='Station', order=labels[orderInd], color="seagreen")
        plt.title(f'Distributions of {cat_var}', fontsize=FONT_SIZE_TITLE)
        plt.xlabel('Station', fontsize=FONT_SIZE_AXES)
        plt.ylabel(f'{cat_var} concentration', fontsize=FONT_SIZE_AXES)
        plt.xticks(fontsize=FONT_SIZE_TICKS)
        plt.yticks(fontsize=FONT_SIZE_TICKS)
        plt.show()
        
    # Widget for picking the continuous variable
    cont_widget_histogram = widgets.Dropdown(
        options=pollutants_list,
        description='Pollutant',
    )
        
    interact(_interactive_boxplot, cat_var=cont_widget_histogram)


def create_scatterplot(df: pd.core.frame.DataFrame):
    '''Creates a scatterplot for pollutant values.
    The pollutants on the x and y axis can be chosen with a dropdown menu.
    
    Args:
        df (pd.core.frame.DataFrame): The dataframe with the data.
    
    '''
    df = df[pollutants_list]  # Take only the pollutants to scatter
    df_clean = df.dropna(inplace=False)

    def _interactive_scatterplot(var_x, var_y):
        x = df_clean[var_x].values
        y = df_clean[var_y].values        
        bins = [200, 200] # number of bins

        hh, locx, locy = np.histogram2d(x, y, bins=bins)
        z = np.array([hh[np.argmax(a<=locx[1:]),np.argmax(b<=locy[1:])] for a,b in zip(x, y)])
        idx = z.argsort()
        x2, y2, z2 = x[idx], y[idx], z[idx]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        s = ax.scatter(x2, y2, c=z2, cmap='jet', marker='.', s = 1)  
        
        ax.set_xlabel(f'{var_x} concentration', fontsize=FONT_SIZE_AXES)
        ax.set_ylabel(f'{var_y} concentration', fontsize=FONT_SIZE_AXES)

        ax.set_title(f'{var_x} vs. {var_y} (color indicates density of points)', fontsize=FONT_SIZE_TITLE)
        ax.tick_params(labelsize=FONT_SIZE_TICKS)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)

        fig.colorbar(
            s,
            cax=cax,
            cmap='jet',
            values=z2,
            orientation="vertical"
        )
        plt.show()
    cont_x_widget = widgets.Dropdown(
        options=pollutants_list,
        description='X-Axis'
    )
    cont_y_widget = widgets.Dropdown(
        options=pollutants_list,
        description='Y-Axis',
        value="PM10"
    )
    
    interact(_interactive_scatterplot, var_x=cont_x_widget, var_y=cont_y_widget)
        

def plot_pairplot(
    raw_data: pd.core.frame.DataFrame,
    pollutants_list: List[str],
):
    '''Creates a pairplot of the features.

    Args:
        raw_data (pd.core.frame.DataFrame): The data used.
        pollutants_list (List[str]): List of features to include in the plot.
    '''

    with sns.plotting_context(rc={"axes.labelsize": FONT_SIZE_AXES}):
        sns.pairplot(raw_data[pollutants_list], kind="hist")
    plt.show()

    
def create_time_series_plot(df: pd.core.frame.DataFrame, start_date: str, end_date: str):
    '''Creates a time series plot, showing the concentration of pollutants over time.
    The pollutant and the measuring station can be selected with a dropdown menu.
    
    Args:
        df (pd.core.frame.DataFrame): The dataframe with the data.
        start_date (str): minimum date for plotting.
        end_date (str): maximum date for plotting.
    
    '''
    def _interactive_time_series_plot(station, pollutant, date_range):
        data = df[df.Station==station]
        data = data[data.DateTime > date_range[0]]
        data = data[data.DateTime < date_range[1]]
        plt.figure(figsize=(12, 6))
        plt.plot(data["DateTime"],data[pollutant], '-')
        plt.title(f'Temporal change of {pollutant}', fontsize=FONT_SIZE_TITLE)
        plt.ylabel(f'{pollutant} concentration', fontsize=FONT_SIZE_AXES)
        plt.xticks(rotation=20, fontsize=FONT_SIZE_TICKS)
        plt.yticks(fontsize=FONT_SIZE_TICKS)
        plt.show()
    
    # Widget for picking the station
    station_selection = widgets.Dropdown(
        options=df.Station.unique(),
        description='Station'
    )

    # Widget for picking the pollutant
    pollutant_selection = widgets.Dropdown(
        options=pollutants_list,
        description='Pollutant',
    )

    dates = pd.date_range(start_date, end_date, freq='D')

    options = [(date.strftime(' %d/%m/%Y '), date) for date in dates]
    index = (0, len(options)-1)
    
    # Slider for picking the dates
    selection_range_slider = widgets.SelectionRangeSlider(
        options=options,
        index=index,
        description='Dates',
        orientation='horizontal',
        layout={'width': '500px'}
    )

    # Putting it all together
    interact(_interactive_time_series_plot, station=station_selection, pollutant=pollutant_selection, date_range=selection_range_slider);


def add_extra_features(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    '''Adds new columns to the dataframe by joining it with another dataframe
    
    Args:
        df (pd.core.frame.DataFrame): The dataframe with the data.
    
    Returns:
        df (pd.core.frame.DataFrame): The updated dataframe with new columns.
    '''
    stations = pd.read_csv('data/stations_loc.csv')
    stations = stations[['Sigla', 'Latitud', 'Longitud']]
    stations = stations.rename(columns={'Sigla': 'Station', 'Latitud': 'Latitude', 'Longitud': 'Longitude'})

    # This cell will convert the values in the columns 'Latitud' and 'Longitud' to 'float64' (decimal) datatype
    stations['Latitude'] = stations['Latitude'].apply(parse_dms)
    stations['Longitude'] = stations['Longitude'].apply(parse_dms)

    df = pd.merge(df, stations, on='Station', how='inner')

    # This cell will extract information from the 'datetime' column and generate months, day or week and hour columns
    df['day_of_week'] = pd.DatetimeIndex(df['DateTime']).day_name()
    df['hour_of_day'] = pd.DatetimeIndex(df['DateTime']).hour
    df.loc[df['hour_of_day']==0,'hour_of_day'] = 24
    return df


######----Início - Visualize os dados em uma representação de mapa

def create_map_with_plots(full_data: pd.DataFrame, x_variable: str, y_variable: str='PM2.5') -> folium.Map:
    '''
    Cria um mapa para visualizar pontos geográficos. O popup exibirá um gráfico de dispersão com as médias diárias/horárias das emissões.
    
    Argumentos:
        full_data: DataFrame com os dados.
        x_variable: Variável x no gráfico do popup (pode ser 'day_of_week' ou 'hour_of_day').
        y_variable: Poluente a ser mostrado no eixo y (padrão 'PM2.5').
    '''

    # Prepara os dados para agrupamento
    data = full_data[['Latitude', 'Longitude', y_variable, 'Station', x_variable]]

    # Agrupa os dados por estação e variável x, calculando a média e o desvio padrão
    data_grouped = data.groupby(['Station', x_variable]).agg(({y_variable: ['mean', 'std']}))
    ymin = data_grouped[y_variable]['mean'].min()
    ymax = data_grouped[y_variable]['mean'].max()

    # Dicionários para armazenar as médias e desvios padrões agrupados
    grouped_means = defaultdict(dict)
    grouped_stds = defaultdict(dict)

    # Processa os dados agrupados para preparar para a visualização
    for index, row in data_grouped.iterrows():
        grouped_means[index[0]][index[1]] = row.iloc[0]
        grouped_stds[index[0]][index[1]] = row.iloc[1]

    # Caminho absoluto onde as imagens são salvas
    img_path = '/media/maykon/Arquivos/4-ProjetoQualidadeDoAr/FaseA_ExploracaoDados/img/tmp/'

    # Gera um gráfico para cada estação e salva como imagem PNG
    for key in grouped_means:
        # Define os rótulos para o eixo x com base na variável x
        if (x_variable == 'day_of_week'):
            keys = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            label = 'daily average'
        else:
            keys = list(grouped_means[key].keys())
            label = 'hourly average'

        # Prepara os valores e desvios padrões para o gráfico
        values = [grouped_means[key][subkey] for subkey in keys]
        stds = [grouped_stds[key][subkey] for subkey in keys]

        # Cria o gráfico
        plt.plot(keys, values, '-o', label=label)
        plt.fill_between(keys, np.array(values) - np.array(stds), np.array(values) + np.array(stds), alpha=0.2)
        if y_variable == 'PM2.5':
            plt.plot(keys, [12]*len(keys), '--g', label='recommended level')
        plt.ylim(ymin, ymax)
        plt.title(f'Station {key} avg. {y_variable} / {x_variable.split("_")[0]}')
        plt.ylabel(f'Avg. {y_variable} concentration')
        plt.xlabel(x_variable.capitalize().replace('_', ' '))
        plt.legend(loc="upper left")
        if (x_variable == 'day_of_week'):
            plt.xticks(rotation=20)

        # Salva o gráfico como uma imagem PNG
        plt.savefig(f'{img_path}/{key}.png')
        plt.clf()

    # Prepara os dados para o mapa
    data_grouped_grid = data.groupby('Station').agg({y_variable: 'mean', 'Latitude': 'min', 'Longitude': 'min'})
    data_grouped_grid_array = np.array([
        data_grouped_grid['Latitude'].values,
        data_grouped_grid['Longitude'].values,
        data_grouped_grid[y_variable].values,
        data_grouped_grid.index.values
    ]).T

    # Cria o mapa
    map3 = folium.Map(
        location=[data_grouped_grid_array[0][0], data_grouped_grid_array[0][1]],
        tiles='openstreetmap',
        zoom_start=11,
        width=1000,
        height=500
    )

    # Adiciona marcadores ao mapa 
    for lt, ln, pol, station in data_grouped_grid_array:
        #popup_html = f"<img src='file://{img_path}/{station}.png'>"
        popup_html = f"<img src='img/tmp/{station}.png' style='width:100%;'>"
        fg = folium.FeatureGroup(name="My Map")
        fg.add_child(folium.CircleMarker(
            location=[lt, ln],
            radius=15,
            popup=popup_html,
            fill_color=color_producer(y_variable, pol),
            color='',
            fill_opacity=0.5))
        map3.add_child(fg)

    return map3

######----Fim - Visualize os dados em uma representação de mapa

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
