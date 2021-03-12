
# ler um arquivo txt ou csv direto da web retornando um pandas
def read_txt_web(url, sep=';'):
    import pandas as pd
    import requests
    r=requests.get(url).text
    l=[i.strip().split(sep) for i in r.split('\n')]
    df=pd.DataFrame(l[1:], columns=l[0])
    return df





