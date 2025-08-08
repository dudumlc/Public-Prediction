from preprocessing.data_cleaning import DataCleaner
import pandas as pd

def main():
    # Carrega o DataFrame original
    df_raw = pd.read_parquet('data/raw/df_raw.parquet',use_pandas_metadata=False, engine="pyarrow")

    # Cria uma instância do DataCleaner
    cleaner = DataCleaner(df_raw)

    # Define as conversões de tipos desejadas
    conversoes = {
            'dia_semana': 'string',    
            'ano': 'string',
            'adversario': 'string',
            'publico_pagante': 'Int64',
            'publico_presente': 'Int64',
            'renda_bruta': 'float',
            'estadio': 'string',
            'campeonato': 'string',
            'placar': 'string',
            'horario': 'string',
            'dia':'string',
            'mes':'string',
            'data_formatada': 'datetime64[ns]',
        }

    # Limpeza dos dados
    df_trusted = (
        cleaner
        .remove_virgulas('dia_semana')
        .formatar_coluna_data()
        .tratar_info_nao_disponivel('publico_presente')
        .tratar_divisor_milhar('publico_presente')
        .extrair_publico('publico_pagante')
        .tratar_info_nao_disponivel('renda_bruta')
        .tratar_renda('renda_bruta')
        .tratar_horario('horario')
        .ajustar_nome_estadio()
        .ajustar_tipos_colunas(conversoes)
        .get_df()
    )

    # Salva o DataFrame limpo
    df_trusted.to_parquet('data/trusted/df_trusted.parquet', engine='pyarrow', index=False)

if __name__ == "__main__":
    main()

