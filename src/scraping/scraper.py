import re
import requests
from bs4 import BeautifulSoup 
import numpy as np
import pandas as pd

class WebScraper:
    BASE_URL = 'https://cruzeiropedia.org'

    def __init__(self,ano_inicio: int, ano_final: int):
        self.ano_inicio = ano_inicio
        self.ano_final = ano_final        

    def _get_lista_temporadas(self):
        
        """

        Pega todos as temporadas selecionadas e retorna uma lista.

        """

        response = requests.get(f"{self.BASE_URL}/Categoria:Temporadas")
        soup = BeautifulSoup(response.content, "html.parser")

        # Monta a lista de títulos esperados de acordo com o intervalo de anos
        titulos = [f"Categoria:Temporada {ano}" for ano in range(self.ano_inicio, self.ano_final + 1)]

        temporadas = soup.find_all("a", {"title": titulos})
        return temporadas
    
    
    def _get_lista_jogos(self, temporada):

        """
        
        Pega todos os jogos que tiveram na página de cada temporada e retorna uma lista.

        """

        # obtém o link da temporada
        link_temporada = temporada.get('href')
        
        # faz a requisição HTTP para a página da temporada
        response_temporada = requests.get(self.BASE_URL + link_temporada)
        
        # faz o parsing do HTML da página da temporada
        soup_temporada = BeautifulSoup(response_temporada.content, 'html.parser')
        
        # pega todos os jogos da temporada
        jogos = soup_temporada.find_all('a', {'title': re.compile(r'(.+) (\d+)x(\d+) (.+) - (\d{2}/\d{2}/\d{4})')})

        return jogos


    def _get_jogo(self, jogo):
        
        """
        
        Pega cada um dos jogos e retorna o soup da página do jogo.
        
        """
        
        # obtém o link do jogo
        link_jogos = jogo.get('href')

        #if "Slovan" in link_jogos:
        #    continue

        #elif "Tr%C3%ADplice" in link_jogos:
        #    continue
    
        # faz a requisição HTTP para a página do jogo
        response_jogos = requests.get('https://cruzeiropedia.org' + link_jogos)
        # faz o parsing do html da página do jogo
        soup_jogos = BeautifulSoup(response_jogos.content, 'html.parser')

        return soup_jogos
        