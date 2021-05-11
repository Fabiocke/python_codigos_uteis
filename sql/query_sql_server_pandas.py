
# Executa querys no sql muito mais rápido que o pandas
def read_sql(query, cnn, fetc = 50000, to_dev=False):
    datatypes = {"<class 'decimal.Decimal'>":float,
		"<class 'float'>":float,
		"<class 'datetime.date'>":'datetime64[ns]',
		"<class 'int'>":int,
		"<class 'datetime.datetime'>":'datetime64[ns]',
        "<class 'datetime.time'>":object}
    cursor = cnn.cursor()
    res = cursor.execute(query)
    descs = [i for i in res.description if str(i[1])!="<class 'str'>"]
    dicttypes = dict(zip([i[0] for i in descs],[datatypes[str(i[1])] for i in descs]))
    df=[]
    n=0
    print('linhas carregadas: 0'+' '*10, end='\r')
    while True:
        res1 = res.fetchmany(fetc)
        res1 = [list(i) for i in res1]
        res1 = pd.DataFrame(res1, columns=[i[0] for i in cursor.description])
        res1 = res1.astype(dicttypes)
        # exporta para dev
        if to_dev:
            export_dev_bp(to_dev[0], res1, to_dev[1])
            to_dev[1]='append'
        else:
            df.append(res1)
            n+=len(res1)
            print('linhas carregadas: '+str(n)+' '*10, end='\r')
        if not len(res1):
            break
    if not to_dev:
        dfs=pd.concat(df).reset_index(drop=True)
        return dfs



