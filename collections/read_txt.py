
# le um arquivo txt ou csv em um dataframe

def read_txt(arquivo, sep='\t'):
    file = open(arquivo) if type(arquivo)==str else arquivo
    lines = file.readlines()
    if type(lines[0])==bytes: lines=[str(i)[2:] for i in lines]
    file.close()
    values = [i.replace('\n','').split(sep) for i in lines]
    df = pd.DataFrame(values[1:], columns=values[0])
    return df


