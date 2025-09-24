import pandas as pd
from modeling.dataset_builder import build_dataset

def main():
    # Carrega refined
    df_jogos = pd.read_parquet("data/refined/df_refined_jogos.parquet")
    df_clima = pd.read_parquet("data/refined/df_refined_clima.parquet")

    # Constrói dataset final para ML
    df_ml = build_dataset(df_jogos, df_clima)

    #FILTRAR APENAS AS COLUNAS A SEREM USADAS NO MODELO


    # Salva dataset pronto para modelagem
    df_ml.to_parquet("data/machine_learning/df_ml.parquet", engine="pyarrow", index=False)

if __name__ == "__main__":
    main()
