from preprocessing.feature_engineering import FeatureEngineer
import pandas as pd

def feature_engineering_jogos():
    # Carrega o DataFrame original
    df_trusted_jogos = pd.read_parquet('data/trusted/df_trusted_jogos.parquet',use_pandas_metadata=False, engine="pyarrow")

    conversoes ={
    'campeonato_ajustado':'string',
    'gols_visitante':'Int64',
    'gols_mandante':'Int64',
    'gols_total':'Int64',
    'pontos_alcancados':'Int64',
    'resultado':'string',
    'aproveitamento_temporada_previo':'float',
    'jogos_invencibilidade_previo':'Int64',
    'estreia':'boolean',
    'classico':'boolean',
    'capacidade_estadio':'Int64',
    'ocupacao_estadio':'float',
    'dia_semana_int':'Int64'
    }

        # Limpeza dos dados
    df_refined_jogos = (
        FeatureEngineer(df_trusted_jogos)
        .feature_nome_campeonato()
        .feature_gols_jogo()
        .feature_pontos_alcancados()
        .feature_resultado()
        .feature_aproveitamento_previo_temporada()
        .feature_invencibilidade_previa()
        .feature_estreia()
        .feature_classico()
        .feature_capacidade_estadio()
        .feature_ocupacao_estadio()
        .feature_dia_semana_numerico()
        .ajustar_tipos_colunas(conversoes)
        .get_df()
    )
    
    df_refined_jogos.to_parquet('data/refined/df_refined_jogos.parquet', index=False, engine='pyarrow')
    print('[FEATURE ENGINEERING] Novas features de jogos criadas com sucesso.✅ ')

def main():
    feature_engineering_jogos()

if __name__ == "__main__":
    main()