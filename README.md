# Estudo de Caso: Qualidade do Ar em Bogotá (RMCAB) 🌬️📈

Este repositório contém o material didático e experimental para a apresentação de **Mestrado na UFSC** sobre a biblioteca **Pandas**, focando na arquitetura padronizada de Ciência de Dados.

---

## 🏛️ Arquitetura do Projeto

Nosso fluxo de trabalho segue três fases fundamentais para projetos de cidades inteligentes:

### **Fase A: Explorar (Discovery & Feasibility)**
Identificação de fontes de dados, verificação de sensores e análise preliminar de viabilidade técnica da Rede de Monitoramento da Qualidade do Ar de Bogotá.

### **Fase B: Design (Preparação de Dados)**
*Foco da nossa apresentação.*
Utilizamos **Pandas** para ingerir, limpar, filtrar e preparar os dados brutos. Nesta fase, tratamos valores ausentes e preparamos as variáveis para modelos preditivos (ML).

### **Fase C: Implementar (Solução & Visualização)**
Implementação de modelos de Machine Learning (como KNN ou Redes Neurais) para imputação de dados e geração de visualizações de impacto, como o **Mapa de Calor de Poluição**.

---

## 🚀 Como Iniciar

### 1. Requisitos
*   Python 3.10+
*   Pandas, NumPy, Matplotlib, Seaborn
*   Folium (Para visualização de mapas)
*   Scikit-Learn (Para suporte de ML)

### 2. Google Colab (Interativo)
Para rodar a demonstração prática, faça o upload do arquivo `Intro_Pandas_Bogota.ipynb` no seu Google Drive e abra-o com o Google Colab.

### 3. Dataset de Exemplo
Utilizamos o arquivo `bogota_sensors_sample.csv` que contém uma amostra real das estações:
*   **USM** (Usme)
*   **KEN** (Kennedy)
*   **TUN** (Tunal)
*   **USQ** (Usaquén)

---

## 💡 Conteúdo Pandas abordado:
1.  **Ingestão:** `pd.read_csv`
2.  **Tratamento:** Limpeza e conversão de coordenadas (DMS para Decimal).
3.  **Filtragem:** `df[df['PM2.5'] > 50]` (Identificando alertas críticos).
4.  **Agrupamento:** `df.groupby('Station').mean()` (Insights por localidade).
5.  **ML Prep:** `pd.get_dummies` e conversão de tipos temporais.

---

## 🗺️ Resultado Visual
O notebook gera um **Mapa de Calor Interativo** baseado nas concentrações de poluição (PM2.5) registradas em tempo real em Bogotá.

---
*Este projeto faz parte da disciplina de IA na Borda do Mestrado UFSC.*
