import os
import pandas as pd

def load_excel(path):

    arquivos = os.listdir(path)

    # Lista para armazenar os dfs
    df_stacked = None
    colunas = None
    # Loop sobre os arquivos na pasta
    for n, arquivo in enumerate(arquivos):
        # Verifica se o arquivo é um arquivo CSV
        if arquivo.endswith('.CSV'):

            # Constrói o caminho completo para o arquivo
            caminho_arquivo = os.path.join(path, arquivo)
            
            # Leitura do arquivo CSV e pula as primeiras 8 linhas
            df = pd.read_csv(caminho_arquivo, encoding='latin-1', delimiter=';', header=None, skiprows=8)
            filtered_df = df[[0,1,2,7,8,18]]

            if n == 0:
                filtered_df.columns = filtered_df.iloc[0]
                colunas = filtered_df.columns
                filtered_df = filtered_df.drop(index=0)
                df_stacked = filtered_df.copy()
            else:
                filtered_df.columns = colunas
                filtered_df = filtered_df.drop(index=0)
                df_stacked = pd.concat([df_stacked, filtered_df], ignore_index=True)
    
    return df_stacked
