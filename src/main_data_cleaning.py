from ingestion.loader import load_excel
from preprocessing.data_cleaning import DataCleaner
import pandas as pd


def clean_games_data():
    # Carrega o DataFrame original
    df_raw_jogos = pd.read_parquet('data/raw/df_raw_jogos.parquet',use_pandas_metadata=False, engine="pyarrow")

    # Cria uma instância do DataCleaner
    cleaner = DataCleaner(df_raw_jogos)

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
    df_trusted_jogos = (
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
    df_trusted_jogos.to_parquet('data/trusted/df_trusted_jogos.parquet', engine='pyarrow', index=False)


def clean_climate_data():
    df_raw_clima = pd.read_parquet('data/raw/df_raw_clima.parquet',use_pandas_metadata=False, engine="pyarrow")

    conversoes_ = {
            'Data': 'datetime64[ns]',
            'Hora UTC': 'string',    
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'float',
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'float',
            'TEMPERATURA DO PONTO DE ORVALHO (°C)': 'float',
            'VENTO, VELOCIDADE HORARIA (m/s)': 'float',
        }

    cleaner = DataCleaner(df_raw_clima)

    df_trusted_clima = (
        cleaner
        .tratar_divisor_milhar('TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)')
        .tratar_divisor_milhar('TEMPERATURA DO PONTO DE ORVALHO (°C)')
        .tratar_decimal('VENTO, VELOCIDADE HORARIA (m/s)')
        .tratar_decimal('PRECIPITAÇÃO TOTAL, HORÁRIO (mm)')
        .ajustar_tipos_colunas(conversoes_)
        .get_df()
        )
    
    # Salva o DataFrame limpo
    df_trusted_clima.to_parquet('data/trusted/df_trusted_clima.parquet', engine='pyarrow', index=False)


def main():
    clean_games_data()
    clean_climate_data()

if __name__ == "__main__":
    main()

