
# PROJETO DE PREVISÃO DE PÚBLICO EM JOGOS DO CRUZEIRO

## Sobre o Projeto

O objetivo desse projeto é estruturar dados históricos de partidas do Cruzeiro Esporte clube, com intuito de estudar o comportamento das variáveis envolvidas e desenvolver um modelo para prever a quantidade de torcedores que irão ao jogo. 
.

O resultado desse projeto pode contribuir para uma melhor gestão do clube, visto que conseguirá estimar o possível público de um jogo com antecedência. Assim, planejaria com mais precisão as questões do jogo, reduzindo seus custos e trazendo cada vez mais benefício para a instituição.
.

⚠️ PROJETO AINDA EM DESENVOLVIMENTO ⚠️

## Etapas do Desenvolvimento

- WEB SCRAPING ✅
- LIMPEZA DOS DADOS ✅
- FEATURE ENGINEERING ✅
- EDA: EM DESENVOLVIMENTO... ⚙️
- FEATURE SELECTION 🕔
- TREINAMENTO E SELEÇÃO DE MODELOS 🕔
- VALIDAÇÃO E TUNAGEM DE HIPERPARÂMETROS 🕔
- TESTE 🕔
- DEPLOY DO MODELO 🕔

## Estrutura do Repositório

A estrutura de pastas deste repositório foi organizada para manter o projeto limpo e modular. Cada diretório principal contém um arquivo `README.md` que detalha seu propósito específico.

- `data/`: Contém os datasets brutos, processados e o dataset analítico usado para a modelagem. Estão organizados na medallion architecture, ou seja, camada raw, refined, trusted e machine_learning.
- `notebooks/`: Notebooks Jupyter para exploração de dados, modelagem e análise.
- `src/`: Código fonte, scripts e módulos reutilizáveis.
- 

## Como Começar

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:dudumlc/Public-Prediction.git
    
    ```

2.  **Restaure as dependências:**
    Por exemplo:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Execute o projeto:**
    Por exemplo:
    ```bash
    python main.py
    ```



