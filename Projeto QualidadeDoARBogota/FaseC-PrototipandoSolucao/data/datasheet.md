# Folha de dados: *Dados do sensor RMCAB* Laboratório 3

Autor: DeepLearning.AI (DLAI)

Arquivos:
dados_completos_com_valores_imputados.csv

## Motivação

O conjunto de dados é uma coleção de medições de vários poluentes em diversas estações de medição em Bogotá, Colômbia. O conjunto de dados é baseado em dois arquivos (RMCAB_air_quality_sensor_data.csv,stations_loc.csv).

Os conjuntos de dados foram baixados do portal público do site da Red de Monitoreo de Calidad del Aire de Bogotá (RMCAB).
http://201.245.192.252:81/home/map e a equipe da RMCAB também deram permissão explícita para que os dados fossem usados para pesquisas acadêmicas.

Os dois conjuntos de dados foram modificados e mesclados em um único arquivo no laboratório anterior deste curso (Qualidade do ar: projete sua solução) e os valores faltantes foram imputados usando diversas técnicas.


## Composição

O conjunto de dados contém as medições de várias estações em Bogotá ao longo de 2021. O conjunto de dados inclui as seguintes colunas: DataHora, Estação, Latitude, Longitude, PM2.5, PM10, NO, NO2, NOX, CO, OZONE, PM2.5_imputed_flag, PM10_imputed_flag, NO_imputed_flag, NO2_imputed_flag, NOX_imputed_flag, CO_imputed_flag, OZONE_imputed_flag.

As colunas DateTime, Station, Latitude e Longitude são totalmente preenchidas com dados originais e representam metadados (hora e local) para cada medição (linha). Cada linha representa uma única medição na estação e horário determinados.

As colunas de poluentes (PM2,5, PM10, NO, NO2, NOX, CO, OZONE) também são totalmente preenchidas, onde algumas das linhas incluem dados originais (brutos), enquanto outras linhas têm dados imputados com interpolação ou com um neural. rede. Cada coluna de poluente tem sua coluna de sinalização correspondente (colunas que terminam com "imputed_flag") onde cada linha informa independentemente se o valor do poluente na linha dada é imputado ou original e qual método foi usado para imputação. Caso a coluna da bandeira esteja vazia, os dados da coluna do poluente correspondente são originais.

O conjunto de dados tem 166.441 linhas no total.