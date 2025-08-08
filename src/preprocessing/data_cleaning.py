import pandas as pd
import re

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()  # Evita alterar o original

    def remove_virgulas(self, coluna):
        self.df[coluna] = self.df[coluna].str.strip(', ')
        return self

    def formatar_coluna_data(self):
        """
        Converte a coluna 'data' (ex: '10 de julho') e 'ano' para datetime
        Cria a nova coluna 'data_formatada'
        """
        self.df[['dia', 'mes']] = self.df['data'].str.split(' de ', expand=True)

        meses_para_numeros = {
            'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
            'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
            'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
        }

        self.df['mes'] = self.df['mes'].map(meses_para_numeros)

        self.df['data'] = (
            self.df['dia'].astype(str) + "/" +
            self.df['mes'].astype(str) + "/" +
            self.df['ano'].astype(str)
        )

        self.df['data_formatada'] = pd.to_datetime(self.df['data'], format='%d/%m/%Y', errors='coerce')

        self.df = self.df.drop('data', axis=1)
        return self

    def tratar_divisor_milhar(self, coluna):
        self.df[coluna] = self.df[coluna].str.replace('.', '', regex=False)
        self.df[coluna] = self.df[coluna].str.replace(',', '.', regex=False)
        return self

    def tratar_renda(self, coluna):
        self.tratar_divisor_milhar(coluna)
        self.df[coluna] = self.df[coluna].str.strip('R$ ')
        return self

    def tratar_info_nao_disponivel(self, coluna):
        self.df[coluna] = self.df[coluna].replace('Não disponível', None)
        self.df[coluna] = self.df[coluna].replace('Não informado', None)
        return self

    def extrair_publico(self, coluna_origem, coluna_destino=None):
        def extrair(valor):
            if pd.isna(valor):
                return None
            match = re.search(r'[\d\.]+', valor)
            if match:
                return match.group().replace('.', '')
            return None

        destino = coluna_destino or coluna_origem
        self.df[destino] = self.df[coluna_origem].apply(extrair)
        return self
    
    def ajustar_nome_campeonato(self, coluna_origem='campeonato', coluna_destino='camp_ajustado'):
        mapa = {
            'Mineiro': 'Campeonato Mineiro',
            'Libertadores': 'Libertadores',
            'Copa do Brasil': 'Copa do Brasil',
            'Brasileiro': 'Brasileirão',
            'Primeira Liga': 'Primeira Liga',
            'Sul-Americana': 'Sul-Americana',
            'Inconfidência': 'Inconfidência',
            'Sul-Minas-Rio': 'Copa Sul-Minas-Rio',
            'Amistoso': 'Amistoso',
        }

        def identificar_campeonato(texto):
            for chave, valor in mapa.items():
                if chave in str(texto):
                    return valor
            return 'nao'

        self.df[coluna_destino] = self.df[coluna_origem].apply(identificar_campeonato)
        return self

    def tratar_horario(self, coluna):
        self.df[coluna] = self.df[coluna].str.strip('às ')
        self.df[coluna] = self.df[coluna].str.replace('h', ':00', regex=False)
        self.df[coluna] = self.df[coluna].str.replace(';', ':', regex=False)
        self.df[coluna] = self.df[coluna].str.replace(r'(\d{1,2}):(\d{1})$', r'\1:0\2', regex=True)
        return self

    def ajustar_tipos_colunas(self, conversoes):

        for coluna, tipo in conversoes.items():
            if coluna in self.df.columns:
                if tipo == 'datetime64[ns]':
                    self.df[coluna] = pd.to_datetime(self.df[coluna], errors='coerce')
                else:
                    self.df[coluna] = self.df[coluna].astype(tipo)

        return self
    
    def ajustar_nome_estadio(self,coluna='estadio'):
        self.df[coluna] = self.df[coluna].replace({"Arena Buser": "Arena do Jacaré"})
        return self

    def get_df(self):
        return self.df
