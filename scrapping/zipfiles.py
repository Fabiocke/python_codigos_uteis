
# le um arquivo csv ou txt dentro  de um zip na internet e retorna um dataframe
def read_csv_from_zip(caminho, arquivo, sep=';'):
    import requests, zipfile, io, requests
    import pandas as pd
    r=requests.get(caminho, stream=True)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    arquivo=zf.open(arquivo)
    
    file = open(arquivo) if type(arquivo)==str else arquivo
    lines = file.readlines()
    if type(lines[0])==bytes: lines=[str(i.strip())[2:-1] for i in lines]
    file.close()
    values = [i.replace('\n','').strip().split(sep) for i in lines]
    df = pd.DataFrame(values[1:], columns=values[0])
    return df



# le um arquivo  xlsx dentro de um zip na internet e retorna um dataframe ou um excelfile
def read_csv_from_zip(caminho, arquivo, sep=';', excel_file=0):
    import requests, zipfile, io, requests
    import pandas as pd
    r=requests.get(caminho, stream=True)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    arquivo=zf.open(arquivo)
    
    df=pd.read_excel(arquivo) if not excel_file else pd.ExcelFile(arquivo)

    return df





