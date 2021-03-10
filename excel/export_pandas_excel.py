# função para exportar dataframes do pandas para o excel
	
def export_excel(local, dfs, plans=False):
    if '\\' not in local:
        import os
        local = os.environ['USERPROFILE'] + '\Desktop\\'+local
    
    dfs = dfs if type(dfs) == list else [dfs]
    writer = pd.ExcelWriter(local, engine='xlsxwriter', date_format='dd/mm/yyyy',
                           datetime_format='dd/mm/yyyy hh:mm:ss')
    workbook  = writer.book
    # Formato das celulas numericas
    integer = workbook.add_format({'num_format': '0'})
    decimal = workbook.add_format({'num_format': '#,##0.00'})

    for x, plan in enumerate(dfs):
        #nomeia as sheets
        try:
            nomesheet=plans[x]
        except:
            nomesheet = 'plan'+str(x+1)
        # Converte o dataframe para XlsxWriter Excel object.
        plan.to_excel(writer, sheet_name=nomesheet, index=False)
        worksheet = writer.sheets[nomesheet]
        # adiciona os formatos as colunas
        for j,i in enumerate(plan.dtypes):
            if i=='float':
                worksheet.set_column(j, j, None, decimal) 

            elif i=='int32' or i=='int64':
                worksheet.set_column(j, j, None, integer) 
    writer.save()




