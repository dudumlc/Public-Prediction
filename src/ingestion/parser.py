from bs4 import BeautifulSoup 

class GameParser:
    def __init__(self, soup):
        self.soup = soup

    def get_dia_semana(self):
        return self.soup.find('b', string='Data:').next_sibling.strip()

    def get_ano(self):
        return self.soup.find('b', string='Data:').find_next_sibling().find_next_sibling().text.strip()

    def get_data(self):
        return self.soup.find('b', string='Data:').find_next_sibling().text.strip()

    def get_adversario(self):
        return self.soup.find('b', string='Placar').find_next_sibling().find_next_sibling().find_next_sibling().text.strip()

    def get_publico_pagante(self):
        tag = self.soup.find('b', string='Público pagante:')
        return tag.next_sibling.strip() if tag and tag.next_sibling else ""

    def get_publico_presente(self):
        tag = self.soup.find('b', string='Público Presente:')
        return tag.next_sibling.strip() if tag and tag.next_sibling else ""

    def get_renda_bruta(self):
        tag = self.soup.find('b', string='Renda Bruta:')
        return tag.next_sibling.strip() if tag and tag.next_sibling else ""

    def get_estadio(self):
        return self.soup.find('b', string='Estádio:').find_next_sibling().text.strip()

    def get_campeonato(self):
        camp_div = self.soup.find('div', class_='divFichaSessao')
        return camp_div.find('b').text.strip() if camp_div else ""

    def get_placar(self):
        placar_element = self.soup.find('div', class_='divFicha')
        return placar_element.find('b').text if placar_element else ""

    def get_horario(self):
        return self.soup.find('b', string='Data:').find_next_sibling().find_next_sibling().next_sibling.strip()

    def parse_all(self):
        """Retorna um dicionário com todos os campos de uma vez."""
        return {
            "dia_semana": self.get_dia_semana(),
            "ano": self.get_ano(),
            "data": self.get_data(),
            "adversario": self.get_adversario(),
            "publico_pagante": self.get_publico_pagante(),
            "publico_presente": self.get_publico_presente(),
            "renda_bruta": self.get_renda_bruta(),
            "estadio": self.get_estadio(),
            "campeonato": self.get_campeonato(),
            "placar": self.get_placar(),
            "horario": self.get_horario()
        }
