from preprocessing.feature_engineering import FeatureEngineer
import pandas as pd

def main():
    # Carrega o DataFrame original
    df_trusted = pd.read_parquet('data/trusted/df_trusted_jogos.parquet',use_pandas_metadata=False, engine="pyarrow")

        # Limpeza dos dados
    df_refined = (
        FeatureEngineer(df_trusted)
        .feature_nome_campeonato()
        .feature_gols_jogo()
        .feature_pontos_alcancados()
        .feature_resultado()
        .feature_aproveitamento_previo_temporada()
        .feature_invencibilidade_previa()
        .feature_estreia()
        .feature_classico()
        .feature_capacidade_estadio()
        .get_df()
    )
    
    df_refined.to_parquet('data/refined/df_refined_jogos.parquet', index=False, engine='pyarrow')

if __name__ == "__main__":
    main()