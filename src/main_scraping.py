from ingestion.scraper import WebScraper
from ingestion.parser import GameParser
import pandas as pd

def main():
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
    df_raw = pd.DataFrame(dados)
    df_raw.to_parquet('data/raw/df_raw_jogos.parquet', index=False, engine='pyarrow')

if __name__ == "__main__":
    main()