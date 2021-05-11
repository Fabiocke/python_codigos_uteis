

## Classe usada para importar e exportar tabelas entre o sql server e o pandas
## de forma muito mais rápida que o método original do pandas

import numpy as np
import pandas as pd
import decimal
from datetime import datetime, date

class Sqlx:
    def __init__(self, cnn):
        
        self.cnn = cnn
        self.chunk = 10000
        self.cursor()
        self.formato_sql = {
            'int':'bigint',
            'object':'varchar(max)',
            'float':'decimal(18,2)',
            'datetime[ns]':'datetime',
        }

    def cursor(self):
        self.cursor = self.cnn.cursor()

    def close(self):
        self.cnn.close()

    # Cria a tabela no sql
    def create_table(self, campos, valores, nome, tipos):
        
        # cria a tabela com os formatos corretos
        cols = ['['+campos[n]+'] ' + self.formato_sql[i] for n, i in enumerate(tipos)]
        cols = ', '.join(cols)
        query = f'CREATE TABLE {nome} ({cols})'
        self.cursor.execute(query)

    # Insere na tabela no sql
    def insert_into(self, nome, valores):
        self.cursor.execute(f"select * from {nome}")
        cols = list(map(lambda x: x[0], self.cursor.description))
        
        query = f"insert into {nome} ([{'], ['.join(cols)}]) values ({', '.join(['?' for i in cols])})"
        vals = [tuple(i) for i in valores]
        vals = [vals[i:i+self.chunk] for i in range(0,len(vals),self.chunk)]
        self.cursor.fast_executemany = True
        n=0
        for val in vals:
            self.cursor.executemany(query, val)
            self.cnn.commit()
#            except IndexError as err:
#                print(err)
#                self.cnn.commit()
#                return
            n+=len(val)
            print('linhas inseridas: '+str(n)+' '*10, end='\r')
        self.cursor.fast_executemany = False


    # Verifica se a tabela existe
    def table_exist(self, nome):
        nome = nome if not nome[:2]=='##' else 'tempdb..'+nome
        self.cursor.execute(f"IF OBJECT_ID ('{nome}') IS NOT NULL SELECT 1 AS res ELSE SELECT 0 AS res")
        return self.cursor.fetchone()[0]


    # Exporta para o sql
    def to_sql(self, nome, tabela, seexiste='fail', chunk=10000):
        self.chunk=chunk
        if isinstance(tabela, pd.DataFrame):
            tipos = [''.join([j for j in i.name if not j.isdigit()]) for i in tabela.dtypes]
            tabela = tabela.replace({pd.NaT:None})
            tab = [list(tabela),tabela.values]

        campos, valores = tab[0], np.array(tab[1])
        
        valores = valores.tolist()  
        
        if self.table_exist(nome):
            if seexiste == 'replace':
                self.cursor.execute('drop table ' + nome)  
                self.cnn.commit()
                self.create_table(campos, valores, nome, tipos)
                self.insert_into(nome, valores)
            elif seexiste == 'append':
                self.insert_into(nome, valores)
            elif seexiste == 'fail':
                print('ERRO: A tabela já existe')
        else:
            self.create_table(campos, valores, nome, tipos)
            self.insert_into(nome, valores)

                


## Exporta um dataframe muito grande para um banco no sql server usando a classe Sqlx
def export_sql(nome, df, con, existe = 'fail', chunk=100000):
    dfs = [df[i:i+chunk] for i in range(0,len(df),chunk)]
    for i in dfs:
        Sqlx(con).to_sql(nome,i,existe)
        existe='append'









