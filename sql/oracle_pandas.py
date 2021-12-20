import pandas as pd
## função usada para importar tabelas entre do oracle para o pandas
## de forma muito mais rápida que o método original do pandas


def read_sql(query, cnn, fetc = 50000, to_dev=False):
    datatypes = {"(<class 'cx_Oracle.NUMBER'>, (1,))":'float',
                 "(<cx_Oracle.DbType DB_TYPE_NUMBER>, (1,))":'float',
		"(<class 'cx_Oracle.DATETIME'>, (1,))":'datetime64[ns]',
        "(<class 'cx_Oracle.DATETIME'>, (0,))":'datetime64[ns]',
		"(<class 'cx_Oracle.NUMBER'>, (0,))":'int',
       "(<cx_Oracle.DbType DB_TYPE_NUMBER>, (0,))":'int',
		"(<class 'cx_Oracle.DATE'>, (0,))":'datetime64[ns]',
        "(<class 'cx_Oracle.TIME'>, (0,))":'object',
        "(<cx_Oracle.DbType DB_TYPE_DATE>, (0,))":'datetime64[ns]',
        "(<cx_Oracle.DbType DB_TYPE_DATE>, (1,))":'datetime64[ns]'}
    cursor = cnn.cursor()
    res = cursor.execute(query)
    df=[]
    n=0
    descs = [[i[0], str((i[1], i[-1:]))] for i in res.description if str((i[1], i[-1:])) 
            not in ("(<class 'cx_Oracle.FIXED_CHAR'>, (0,))", "(<class 'cx_Oracle.STRING'>, (0,))", 
                "(<class 'cx_Oracle.FIXED_CHAR'>, (1,))", "(<class 'cx_Oracle.STRING'>, (1,))",
                "(<class 'cx_Oracle.DATETIME'>, (1,))", "(<class 'cx_Oracle.DATETIME'>, (0,))",
                "(<class 'cx_Oracle.DATE'>, (0,))", "(<class 'cx_Oracle.TIME'>, (0,))",
                    '(<cx_Oracle.DbType DB_TYPE_VARCHAR>, (1,))', '(<cx_Oracle.DbType DB_TYPE_VARCHAR>, (0,))',
                   '(<cx_Oracle.DbType DB_TYPE_CHAR>, (0,))', '(<cx_Oracle.DbType DB_TYPE_CHAR>, (1,))')]
    dicttypes = dict(zip([i[0] for i in descs], [datatypes[i[1]] for i in descs]))
    print('linhas carregadas: 0'+' '*10, end='\r')
    while True:
        res1 = res.fetchmany(fetc)
        res1 = [list(i) for i in res1]
        res1 = pd.DataFrame(res1, columns=[i[0] for i in cursor.description])
        res1 = res1.astype(dicttypes)
        # exporta para dev
        if to_dev:
            bp.export_dev_bp(to_dev[0], res1, to_dev[1])
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


