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
*   `df['PM2.5'] > 50`: Cria uma máscara booleana (True/False).
*   `df[...]`: Aplica essa máscara ao DataFrame original para retornar apenas as linhas que atendem ao critério.

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
*   `.groupby('Station')`: Organiza os dados em grupos baseados no nome da estação.
*   `['PM10'].mean()`: Aplica a função de média apenas à coluna de poluição PM10 dos grupos.
*   `.reset_index()`: Transforma o resultado de volta em um DataFrame padrão para fácil visualização.

---

## ✨ Dica Pro (Avançado)
Se quiser filtrar apenas a estação **Kennedy (KEN)** e ver a média dela separadamente:

```python
# Filtro + Média
media_kennedy = df[df['Station'] == 'KEN']['PM2.5'].mean()
print(f"Média PM2.5 em Kennedy: {media_kennedy:.2f} µg/m³")
```
