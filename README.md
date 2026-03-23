# <div align="center">🌍 Projeto Qualidade do Ar: Monitoramento RMCAB Bogotá</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/JamaicaStoAndre/Ci-ncia-de-dados-com-Pandas/master/bogota_air_quality_banner.png" alt="Banner" width="100%">
</div>

---

## 🏛️ Sobre o Projeto
Este repositório apresenta um estudo de caso prático utilizando a biblioteca **Pandas** para o monitoramento da qualidade do ar na cidade de Bogotá (Rede RMCAB). O projeto é estruturado conforme a arquitetura padronizada de Ciência de Dados (**Fase A, B e C**), servindo como base didática para o mestrado **IA na Borda (UFSC)**.

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

## 🚀 Como Iniciar

### Option 1: Google Colab (Recomendado)
Você pode rodar toda a atividade sem instalar nada clicando no botão abaixo:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JamaicaStoAndre/Ciencia_de_Dados_com_Pandas/blob/master/Intro_Pandas_Bogota.ipynb)

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

## 🎓 Desafio Prático
Preparamos dois exercícios ao final do notebook para que os alunos possam consolidar os conceitos de **Filtro** e **Estatísticas Agrupadas**. O código de resolução também está incluído no final do notebook como gabarito.

---
<div align="center">
  <sub>Desenvolvido como parte do programa de Mestrado UFSC - IA na Borda</sub>
</div>
