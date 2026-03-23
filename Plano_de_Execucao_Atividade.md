# Plano de Execução: Atividade de Pandas (Projeto Bogotá) 🚀

Este plano foi estruturado para garantir que sua apresentação de 8 minutos seja dinâmica, fluida e tenha um encerramento impactante para os alunos de mestrado.

---

## 📂 Arquivos Necessários (Lista de Upload)

Para que tudo funcione, você deve colocar estes 2 arquivos **na mesma pasta** (seja no Google Drive ou GitHub):

1.  **`Intro_Pandas_Bogota.ipynb`**: O coração da aula. Já contém as instruções e o código pronto.
2.  **`bogota_sensors_sample.csv`**: O dataset de sensores com as coordenadas reais de Bogotá.

### Onde estão os arquivos?
Eles já foram gerados e estão na sua pasta local em:
`.../Documentos/Mestrado UFSC/IA na Borda/Ciencia_de_Dados_Padronizado/DocumentosBase/`

---

## ⏱️ Roteiro da Apresentação (8 Minutos)

### 1. Início: Contexto & Arquitetura (0:00 - 2:00)
- **Ação:** Mostre o primeiro slide ou a introdução do Notebook.
- **Fala:** "O projeto Bogotá segue o padrão de 3 fases (A, B, C). Hoje focaremos na **Fase B (Design)**, onde o Pandas é nossa principal ferramenta para limpar e estruturar os dados para os modelos de IA."
- **Objetivo:** Estabelecer a importância do Pandas no ciclo de vida do projeto.

### 2. Live Demo: O Poder do Pandas (2:00 - 5:00)
- **Ação:** Abra o Notebook no Colab e execute as células.
- **Destaque:** Mostre como é fácil ler o CSV e realizar o **GroupBy** (Média de poluição por estação).
- **Interação:** Mencione o exercício de **Filtro** (PM2.5 > 50) como um caso real de alerta de saúde pública.
- **Dica:** Não tente explicar cada detalhe do código, foque no **resultado prático**.

### 3. Conexão com IA: Fase B ➡️ C (5:00 - 6:30)
- **Ação:** Mostre rapidamente a célula de "ML Prep" (One-Hot Encoding).
- **Fala:** "Aqui o Pandas prepara os dados para as Redes Neurais que usamos na Fase C para prever valores ausentes."
- **Objetivo:** Mostrar que o Pandas não é apenas para tabelas, mas a base de qualquer modelo sério de IA.

### 4. Gran Finale: O Mapa de Risco (6:30 - 8:00)
- **Ação:** Gere o **Mapa de Calor (Heatmap)** ao vivo.
- **Fala:** "Tratamos os dados com Pandas, interpolamos o que faltava na Fase B e agora vemos o resultado: um mapa dinâmico de risco respiratório em Bogotá."
- **Encerramento:** Deixe o link do GitHub para os alunos "brincarem" com o código depois.

---

## 🛠️ Dicas para os Alunos (No GitHub)

No seu `README.md`, adicione estas instruções simples para que eles possam reproduzir:
1.  Clique no botão "Open in Colab".
2.  Arraste o arquivo `bogota_sensors_sample.csv` para a aba de arquivos (pasta) à esquerda no Colab.
3.  Execute todas as células (`Ctrl + F9`).

---
**Deseja que eu tente carregar o conteúdo do notebook diretamente no seu link do Colab agora?**
