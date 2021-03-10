# função para gerar uma conexão com um banco oracle
        
import cx_Oracle

def connect(caminho, port, server, user, password)
    dsn_tns = cx_Oracle.makedsn(caminho, port, service_name=server) #SINACOR XP
    return cx_Oracle.connect(user=user, password=password, dsn=dsn_tns, encoding = "UTF-8", nencoding = "UTF-8")
