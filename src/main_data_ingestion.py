from ingestion.scraper import WebScraper
from ingestion.parser import GameParser
from ingestion.loader import load_excel
import pandas as pd

def scrape_games_data():
    scraper = WebScraper(2011, 2025)

    dados = []
    for temporada in scraper._get_lista_temporadas():
        print(f'Analisando a temporada {temporada}')
        for jogo_tag in scraper._get_lista_jogos(temporada):

            if "Slovan" in jogo_tag.text:
                continue
            elif "Tríplice Coroa" in jogo_tag.text:
                continue

            soup_jogo = scraper._get_jogo(jogo_tag)
            parser = GameParser(soup_jogo)
            dados.append(parser.parse_all())

    # converte para DataFrame
    df_raw_jogos = pd.DataFrame(dados)
    df_raw_jogos.to_parquet('data/raw/df_raw_jogos.parquet', index=False, engine='pyarrow')
    print('[DATA INGESTION] Dados de jogos extraídos e dataset criado com sucesso. ✅')

def load_climate_data():
    df_raw_clima = load_excel('data/raw/climate_data')
    df_raw_clima.to_parquet('data/raw/df_raw_clima.parquet', index=False, engine='pyarrow')
    print('[DATA INGESTION] Dataset de clima carregados e empilhados com sucesso. ✅')

def main():
    scrape_games_data()
    load_climate_data()

if __name__ == "__main__":
    main()