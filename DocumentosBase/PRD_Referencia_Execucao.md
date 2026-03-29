# PRD: Apresentação Ciência de Dados - Sensores de Qualidade do Ar em Bogotá

## 1. Visão Geral do Projeto
Este projeto apresenta a arquitetura padronizada de Ciência de Dados (Fases A, B e C) utilizando o caso de estudo da Rede de Monitoramento da Qualidade do Ar de Bogotá (RMCAB). O foco principal desta etapa é a **Introdução à Biblioteca Pandas**, servindo como base para o tratamento de dados no ciclo de vida do projeto.

## 2. Público-Alvo
*   **Perfil:** Estudantes de Mestrado em uma Universidade Federal (UFSC).
*   **Nível:** Avançado em conceitos acadêmicos, mas necessitando de clareza prática e didática em ferramentas de codificação (Python/Pandas).

## 3. Objetivos de Aprendizagem (Parte 5 da Tarefa)
Ao final da apresentação de 8 minutos, os alunos deverão compreender:
1.  A diferença entre **Series** e **DataFrames**.
2.  Como carregar dados de fontes externas (**CSV e Excel**).
3.  Operações essenciais: **Filtros, Agrupamentos (GroupBy) e Estatísticas descritivas**.
4.  Como o Pandas se encaixa na **Fase B (Design/Preparação)** do projeto Bogotá.

## 4. Estratégia da Apresentação (8 Minutos)

| Tempo | Seção | Conteúdo |
|---|---|---|
| 0:00 - 1:00 | **Introdução & Contexto** | Apresentação do Projeto Bogotá e a Arquitetura (Fases A, B, C). |
| 1:00 - 2:30 | **Pandas 101** | Estruturas de Dados: Series vs DataFrame com dados de sensores (PM2.5, NO2). |
| 2:30 - 4:00 | **Ingestão de Dados** | Leitura de CSV/Excel (Simulação do início da Fase B). |
| 4:00 - 6:00 | **Manipulação de Dados** | Filtros de poluição alta, Agrupamento por Estação, Estatísticas básicas. |
| 6:00 - 7:00 | **Proposta de Exercícios** | Proposição de 2 exercícios práticos baseados no dataset Bogotá. |
| 7:00 - 8:00 | **Encerramento & ML** | Demonstração do Resultado Final: Mapa de Calor (Fase C) interpolado com KNN. |

## 5. Requisitos Técnicos
*   **Google Colab:** Ambiente interativo para demonstração.
*   **GitHub:** Repositório com `README.md`, Notebooks e Datasets de exemplo.
*   **Dataset:** Amostra real baseada na RMCAB (21 estações, poluentes: PM2.5, PM10, CO, O3).

## 6. Exercícios Propostos (Práticos)
1.  **Filtro de Emergência:** Filtrar todas as leituras de PM2.5 superiores a 50 µg/m³ (nível de alerta).
2.  **Média por Localidade:** Calcular a média de PM10 agrupada por estação de monitoramento.

## 7. Roteiro dos Slides (Apresentação de 8 Minutos)

| Slide | Título | Conteúdo Visual | Fala do Apresentador |
|---|---|---|---|
| 1 | **Cidades Inteligentes: Qualidade do Ar em Bogotá** | Foto de Bogotá + Logo do Projeto (RMCAB) | "Boa noite. Vamos apresentar o projeto de monitoramento de poluição em Bogotá, focado na arquitetura padronizada de DS." |
| 2 | **Arquitetura Padronizada: Fases A, B e C** | Fluxograma: Explorar ➔ Design ➔ Implementar | "Nosso projeto passa pela Fase A (viabilidade), B (design/prep) e C (ML). Hoje focaremos na **Fase B** usando Pandas." |
| 3 | **Pandas: O Motor da Fase B** | Código simples: Series vs DataFrame | "O Pandas é essencial para manipular o fluxo de dados dos 21 sensores espalhados por Bogotá." |
| 4 | **Ingestão de Dados** | Captura de tela do `pd.read_csv()` | "Lemos os dados brutos (CSV/Excel) diretamente da rede RMCAB para iniciar o tratamento." |
| 5 | **Filtros e Alertas de Saúde** | Código de filtro: `df[df['pm2_5'] > 35]` | "Identificamos áreas de alerta respiratório rapidamente através de filtros booleanos." |
| 6 | **Estatísticas e Agrupamento** | Tabela de `groupby` por localidade | "Agrupamos as médias de poluição por localidade para gerar insights territoriais." |
| 7 | **Hands-On: Desafios Práticos** | 💡 Exercícios: Filtro O3 e Média Kennedy | "Proponho aqui estes dois exercícios para consolidar o uso do Pandas no contexto de Bogotá." |
| 8 | **Resultado Final: Mapa de Calor** | 🗺️ Mapa Interativo (Fase C) | "Finalizamos com os dados tratados no Pandas alimentando o modelo KNN para gerar o mapa de risco em tempo real." |

## 8. Critérios de Sucesso
*   Clareza didática.
*   Conexão fluida entre Pandas e o resultado final de ML.
