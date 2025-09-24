import pandas as pd
import re
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()  # Evita alterar o original

    ## COLUNAS DE DADOS DE JOGOS ##

    def feature_nome_campeonato(self, coluna_origem='campeonato', coluna_destino='campeonato_ajustado') -> str:
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
    
    def feature_gols_jogo(self, coluna_gols_mandante='gols_mandante', coluna_gols_visitante='gols_visitante', coluna_gols_total='gols_total') -> int:
        
        self.df[coluna_gols_visitante] = self.df['placar'].str.split(' × ',expand=True).loc[:,0]
        self.df[coluna_gols_mandante] = self.df['placar'].str.split(' × ',expand=True).loc[:,1]
        self.df[coluna_gols_total] = self.df[coluna_gols_mandante].astype(int) + self.df[coluna_gols_visitante].astype(int)
        return self

    def feature_pontos_alcancados(self):
        condicoes = [
            (self.df['gols_mandante'] == self.df['gols_visitante']),
            (self.df['gols_mandante'] > self.df['gols_visitante']) & (self.df['adversario'] == 'Cruzeiro'),
            (self.df['gols_mandante'] > self.df['gols_visitante']) & (self.df['adversario'] != 'Cruzeiro'),
            (self.df['gols_mandante'] < self.df['gols_visitante']) & (self.df['adversario'] == 'Cruzeiro'),
            (self.df['gols_mandante'] < self.df['gols_visitante']) & (self.df['adversario'] != 'Cruzeiro'),
        ]

        pontos_alcancados = [1, 0, 3, 3, 0]

        self.df['pontos_alcancados'] = np.select(condicoes, pontos_alcancados, default=np.nan)
        return self

    def feature_resultado(self):
        condicoes = [
            (self.df['pontos_alcancados'] == 3),
            (self.df['pontos_alcancados'] == 1),
            (self.df['pontos_alcancados'] == 0),
        ]

        resultados = ['Vitoria', 'Empate', 'Derrota']

        self.df['resultado'] = np.select(condicoes, resultados, default='na')
        self.df['resultado'] = self.df['resultado'].replace('na', np.nan)
        return self
    
    def feature_aproveitamento_previo_temporada(self):
        self.df['aproveitamento_temporada_previo'] = 0.0  # Inicializa a coluna com float

        indice_primeiro_jogo_do_ano = 0
        ano_em_questao = None

        for i in range(len(self.df)):
            if i == 0:
                self.df.at[i, 'aproveitamento_temporada_previo'] = 0
                ano_em_questao = self.df.at[i, 'ano']

            elif self.df.at[i, 'ano'] != self.df.at[i - 1, 'ano']:
                self.df.at[i, 'aproveitamento_temporada_previo'] = 0
                indice_primeiro_jogo_do_ano = i
                ano_em_questao = self.df.at[i, 'ano']

            else:
                soma_pontos = self.df.loc[indice_primeiro_jogo_do_ano:i - 1, 'pontos_alcancados'].sum()
                jogos_anteriores = i - indice_primeiro_jogo_do_ano
                self.df.at[i, 'aproveitamento_temporada_previo'] = soma_pontos / (jogos_anteriores * 3)

        return self
    
    def feature_invencibilidade_previa_temporada(self):
        self.df['invencibilidade_temporada_previa'] = 0
        seq = 0

        for i in range(len(self.df)):
            if i == 0 or self.df.loc[i, 'ano'] != self.df.loc[i - 1, 'ano']:
                seq = 0
            elif self.df.loc[i - 1, 'resultado'] in ['Vitoria', 'Empate']:
                seq += 1
            else:
                seq = 0

            self.df.at[i, 'invencibilidade_temporada_previa'] = seq

        return self
    
    def feature_resultado_anterior_temporada(self):

        for i in range(len(self.df)):
            if i == 0 or self.df.loc[i, 'ano'] != self.df.loc[i - 1, 'ano']:
                self.df.at[i,'resultado_anterior'] = "Estreia"
            elif self.df.loc[i - 1, 'resultado'] == 'Vitoria':
                self.df.at[i,'resultado_anterior'] = 'Vitoria'
            elif self.df.loc[i - 1, 'resultado'] == 'Derrota':
                self.df.at[i,'resultado_anterior'] = 'Derrota'
            elif self.df.loc[i - 1, 'resultado'] == 'Empate':
                self.df.at[i,'resultado_anterior'] = 'Empate'
            else:
                self.df.at[i,'resultado_anterior'] = "ALGUM ERRO ACONTECEU"
        
        return self

    def feature_estreia(self):
        for i in range(len(self.df)):
            if i == 0:
                self.df.at[i, 'estreia'] = 1
            elif self.df.at[i, 'ano'] != self.df.at[i - 1, 'ano']:
                self.df.at[i, 'estreia'] = 1
            else:
                self.df.at[i, 'estreia'] = 0
        return self

    def feature_classico(self):
        for i in range(len(self.df)):
            if self.df.at[i, 'adversario'] == "Atlético-MG":
                self.df.at[i, 'classico'] = 1
            else:
                self.df.at[i, 'classico'] = 0
        return self
    
    def feature_capacidade_estadio(self):
        
        capacidade_estadio = [
            {"Estádio": "Arena do Jacaré", "Capacidade": 19998},
            {"Estádio": "Parque do Sabiá", "Capacidade": 39900},
            {"Estádio": "Ipatingão", "Capacidade": 22500},
            {"Estádio": "Arena do Calçado", "Capacidade": 10000},
            {"Estádio": "Melão", "Capacidade": 15471},
            {"Estádio": "Independência", "Capacidade": 23000},
            {"Estádio": "Mineirão", "Capacidade": 61927},
            {"Estádio": "Mané Garrincha", "Capacidade": 72788},
            {"Estádio": "Kléber Andrade", "Capacidade": 21152},
            {"Estádio": "Inter&Co Stadium", "Capacidade": 25500},
            {"Estádio": "Arena Pantanal", "Capacidade": 42968},
            {"Estádio": "Sesc Venda Nova", "Capacidade": 2000},
            ]
        
        self.df['capacidade_estadio'] = self.df['estadio'].map(
            lambda x: next((item['Capacidade'] for item in capacidade_estadio if item['Estádio'] == x), None))
        
        return self
    
    def feature_ocupacao_estadio(self):
        self.df['ocupacao_estadio'] =  self.df['publico_pagante'] / self.df['capacidade_estadio'] 
        return self
    
    def feature_dia_semana_numerico(self):
        
        ordem_dias_semana = {
        'domingo':7,
        'sábado':6,
        'quarta-feira':3,
        'terça-feira':2,
        'quinta-feira':4,
        'sexta-feira':5,
        'segunda-feira':1
        }

        self.df['dia_semana_int'] = self.df['dia_semana'].map(ordem_dias_semana)
        return self 
    
    def feature_lag_jogos(self, coluna):
        self.df[f'{coluna}_lag1jogos'] = self.df[coluna].shift(1)
        self.df[f'{coluna}_lag2jogos'] = self.df[coluna].shift(2)
        self.df[f'{coluna}_lag3jogos'] = self.df[coluna].shift(3)
        self.df[f'{coluna}_lag4jogos'] = self.df[coluna].shift(4)
        self.df[f'{coluna}_lag5jogos'] = self.df[coluna].shift(5)
        self.df[f'{coluna}_lag6jogos'] = self.df[coluna].shift(6)
        self.df[f'{coluna}_lag7jogos'] = self.df[coluna].shift(7)

        self.df[f'{coluna}_media_7jogos'] = self.df[[f'{coluna}_lag1jogos',f'{coluna}_lag2jogos',f'{coluna}_lag3jogos',f'{coluna}_lag4jogos',f'{coluna}_lag5jogos',f'{coluna}_lag6jogos',f'{coluna}_lag7jogos']].sum(axis=1,skipna=True) / 7
        self.df[f'{coluna}_media_6jogos'] = self.df[[f'{coluna}_lag1jogos',f'{coluna}_lag2jogos',f'{coluna}_lag3jogos',f'{coluna}_lag4jogos',f'{coluna}_lag5jogos',f'{coluna}_lag6jogos']].sum(axis=1,skipna=True) / 6
        self.df[f'{coluna}_media_5jogos'] = self.df[[f'{coluna}_lag1jogos',f'{coluna}_lag2jogos',f'{coluna}_lag3jogos',f'{coluna}_lag4jogos',f'{coluna}_lag5jogos']].sum(axis=1,skipna=True) / 5
        self.df[f'{coluna}_media_4jogos'] = self.df[[f'{coluna}_lag1jogos',f'{coluna}_lag2jogos',f'{coluna}_lag3jogos',f'{coluna}_lag4jogos']].sum(axis=1,skipna=True) / 4
        self.df[f'{coluna}_media_3jogos'] = self.df[[f'{coluna}_lag1jogos',f'{coluna}_lag2jogos',f'{coluna}_lag3jogos']].sum(axis=1,skipna=True) / 3
        self.df[f'{coluna}_media_2jogos'] = self.df[[f'{coluna}_lag1jogos',f'{coluna}_lag2jogos']].sum(axis=1,skipna=True) / 2

        return self
    
    def feature_lag_once(self, coluna):
        self.df[f'{coluna}_lag1'] = self.df[coluna].shift(1)
        return self

    ## COLUNAS DE DADOS DE CLIMA ##

    def feature_lag_clima(self, coluna):
        self.df[f'{coluna}_lag1'] = self.df[coluna].shift(1)
        self.df[f'{coluna}_lag2'] = self.df[coluna].shift(2)
        self.df[f'{coluna}_lag3'] = self.df[coluna].shift(3)
        self.df[f'{coluna}_lag4'] = self.df[coluna].shift(4)
        self.df[f'{coluna}_lag5'] = self.df[coluna].shift(5)
        self.df[f'{coluna}_lag6'] = self.df[coluna].shift(6)
        self.df[f'{coluna}_lag7'] = self.df[coluna].shift(7)

        self.df[f'{coluna}_media_7dias'] = self.df[[f'{coluna}_lag1',f'{coluna}_lag2',f'{coluna}_lag3',f'{coluna}_lag4',f'{coluna}_lag5',f'{coluna}_lag6',f'{coluna}_lag7']].sum(axis=1,skipna=True) / 7
        self.df[f'{coluna}_media_6dias'] = self.df[[f'{coluna}_lag1',f'{coluna}_lag2',f'{coluna}_lag3',f'{coluna}_lag4',f'{coluna}_lag5',f'{coluna}_lag6']].sum(axis=1,skipna=True) / 6
        self.df[f'{coluna}_media_5dias'] = self.df[[f'{coluna}_lag1',f'{coluna}_lag2',f'{coluna}_lag3',f'{coluna}_lag4',f'{coluna}_lag5']].sum(axis=1,skipna=True) / 5
        self.df[f'{coluna}_media_4dias'] = self.df[[f'{coluna}_lag1',f'{coluna}_lag2',f'{coluna}_lag3',f'{coluna}_lag4']].sum(axis=1,skipna=True) / 4
        self.df[f'{coluna}_media_3dias'] = self.df[[f'{coluna}_lag1',f'{coluna}_lag2',f'{coluna}_lag3']].sum(axis=1,skipna=True) / 3
        self.df[f'{coluna}_media_2dias'] = self.df[[f'{coluna}_lag1',f'{coluna}_lag2']].sum(axis=1,skipna=True) / 2

        return self

    ## MÉTODOS PADRÕES ENTRE DATASETS ##

    def ajustar_tipos_colunas(self, conversoes):

        for coluna, tipo in conversoes.items():
            if coluna in self.df.columns:
                if tipo == 'datetime64[ns]':
                    self.df[coluna] = self.df[coluna].str.replace('-','/')
                    self.df[coluna] = pd.to_datetime(self.df[coluna], errors='coerce', format=None)
                else:
                    self.df[coluna] = self.df[coluna].astype(tipo)

        return self

    def get_df(self):
        return self.df
