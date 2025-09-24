import pandas as pd

def build_dataset(df_jogos: pd.DataFrame, df_clima: pd.DataFrame) -> pd.DataFrame:
    # Junta clima diário com os jogos pela data
    df = df_jogos.merge(df_clima, left_on="data_formatada", right_on="Data", how="left")

    # Filtra colunas que não serão utilizadas

    # One-hot encoding aqui?

    return df
