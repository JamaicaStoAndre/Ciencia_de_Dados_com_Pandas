# <div align="center">🌍 Projeto Qualidade do Ar: Monitoramento RMCAB Bogotá</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/JamaicaStoAndre/Ci-ncia-de-dados-com-Pandas/master/bogota_air_quality_banner.png" alt="Banner" width="100%">
</div>
---

## 🏛️ Sobre o Projeto

- Este projeto visa lincar a disciplina de IA na Borda com a disciplina de Ciência de Dados com Pandas.

- Este repositório apresenta um estudo de caso prático utilizando a biblioteca **Pandas** para o monitoramento da qualidade do ar na cidade de Bogotá (Rede RMCAB). O projeto é estruturado conforme a arquitetura padronizada de Ciência de Dados (**Fase A, B e C**), servindo como base didática para o mestrado **IA na Borda (UFSC)**.

### Tópicos abordados

- Leitura de Arquivos (CSV)
- Operações básicas (filtros, agrupamentos, estatísticas)
- Ponte Didática: Uso de **NumPy** para geração de gráficos (Matplotlib)
- Criação de Séries, DataFrame e Visualização do resultado

### 🏛️ As Três Fases do Projeto

1. **Fase A - Explorar (Discovery)**:
   - **Objetivo**: Avaliar a viabilidade técnica e entender o domínio dos dados de sensores.
   - **Ação**: Identificar se os sensores estão ativos e se os dados são acessíveis e confiáveis.

2. **Fase B - Design (Preparação)**:
   - **Objetivo**: Limpar, transformar e estruturar os dados brutos para alimentar modelos de IA.
   - **Ação**: Tratamento de nulos, filtros, agrupamentos e engenharia de variáveis usando **Pandas** e **NumPy**.

3. **Fase C - Implementar (Prototipagem)**:
   - **Objetivo**: Criar a solução final, modelos de predição e visualizações de impacto.
   - **Ação**: Geração de mapas de calor geoespaciais e implementação de modelos como KNN ou Redes Neurais.

---

### QR Code para acesso ao repositório

<div align="center">
  <img src="./QRCode_Github.png" alt="QRCode" width="82" height="82">
</div>

## 🚀 Como Iniciar

### Option 1: Google Colab (Recomendado)

Você pode rodar toda a atividade sem instalar nada clicando no botão abaixo:

<a href="https://colab.research.google.com" target="_blank" rel="noopener noreferrer">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">
</a>

> **Nota:** Se estiver rodando no Colab, certifique-se de fazer o upload do arquivo `bogota_sensors_sample.csv` para a barra lateral de arquivos.

### Option 2: Local (Via Git)

```bash
git clone https://github.com/JamaicaStoAndre/Ciencia_de_Dados_com_Pandas.git
cd Ciencia_de_Dados_com_Pandas
# Instale as dependências
pip install pandas folium seaborn matplotlib
```

---

## 📊 Estrutura dos Dados

O dataset de exemplo (`bogota_sensors_sample.csv`) contém leituras coletadas de sensores reais, incluindo:

- **PM2.5 / PM10:** Matérias particuladas (indicadores de saúde).
- **CO / O3:** Gases poluentes.
- **Latitude / Longitude:** Metadados geográficos das estações.
- **Estações:** Kennedy (KEN), Usme (USM), Tunal (TUN), entre outras.

---

## 🗺️ Visualização de Impacto

No final do notebook, geramos um **Mapa de Calor Interativo** que permite visualizar a dispersão da poluição na malha urbana de Bogotá, facilitando a tomada de decisão em políticas de saúde pública.

---

# Suporte: Exercícios Práticos de Pandas (Projeto Bogotá) 🧠🔍

Este guia fornece as soluções detalhadas para os dois exercícios propostos na apresentação de 8 minutos. Ideal para compartilhar com os alunos via GitHub.

---

## Exercício 1: Filtro de Alerta de Saúde

**Objetivo:** Identificar leituras críticas de PM2.5 superiores a 50 µg/m³ (Nível de Emergência).

### Código em Pandas:

```python
# Filtrando o DataFrame para PM2.5 > 50
df_alertas = df[df['PM2.5'] > 50]

# Exibindo o número de alertas encontrados
print(f"Total de alertas críticos: {len(df_alertas)}")

# Visualizando as primeiras linhas filtradas
display(df_alertas.head())
```

### Explicação Didática:

- `df['PM2.5'] > 50`: Cria uma máscara booleana (True/False).
- `df[...]`: Aplica essa máscara ao DataFrame original para retornar apenas as linhas que atendem ao critério.

---

## Exercício 2: Média de Poluição por Estação (GroupBy)

**Objetivo:** Calcular a concentração média de PM10 para cada estação de monitoramento.

### Código em Pandas:

```python
# Agrupando por Estação e calculando a média do PM10
media_estacao = df.groupby('Station')['PM10'].mean().reset_index()

# Ordenando do maior para o menor nível de poluição
media_estacao = media_estacao.sort_values(by='PM10', ascending=False)

# Exibindo o resultado final formatado
display(media_estacao)
```

### Explicação Didática:

- `.groupby('Station')`: Organiza os dados em grupos baseados no nome da estação.
- `['PM10'].mean()`: Aplica a função de média apenas à coluna de poluição PM10 dos grupos.
- `.reset_index()`: Transforma o resultado de volta em um DataFrame padrão para fácil visualização.

---

## ✨ Dica Pro (Avançado)

Se quiser filtrar apenas a estação **Kennedy (KEN)** e ver a média dela separadamente:

```python
# Filtro + Média
media_kennedy = df[df['Station'] == 'KEN']['PM2.5'].mean()
print(f"Média PM2.5 em Kennedy: {media_kennedy:.2f} µg/m³")
```
