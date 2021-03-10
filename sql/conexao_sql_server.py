
# função para se conectar a um banco no sql server

import pyodbc

def connect(driver, server, user='', password='', db=''):
    strconn = 'DRIVER='+self.driver+';SERVER='+server+';PORT=1433;DATABASE='+db
    if user and password:
        return pyodbc.connect(strconn+';UID='+username+';PWD='+ password)
    else:
        return pyodbc.connect(strconn+';Trusted_Connection=yes;')
    
    


