# função para exportar dataframes do pandas para o excel
	
import openpyxl
from io import BytesIO
import pandas as pd

class Excel:
    def __init__(self, dfs, plans=None):
        self.dfs = dfs if type(dfs) == list else [dfs]
        self.plans=plans
        self.w=self.__plan()

    def __plan(self):
        b=BytesIO()
        writer = pd.ExcelWriter(b, engine='openpyxl', date_format='dd/mm/yyyy',
                               datetime_format='dd/mm/yyyy hh:mm:ss')
        #workbook  = writer.book
        # Formato das celulas numericas
        #integer = workbook.add_format({'num_format': '0'})
        #decimal = workbook.add_format({'num_format': '#,##0.00'})
        
        for x, plan in enumerate(self.dfs):
            #nomeia as sheets
            try:
                nomesheet=self.plans[x]
            except:
                nomesheet = 'plan'+str(x+1)

            # Converte o dataframe para XlsxWriter Excel object.
            index = True if isinstance(plan.columns, pd.MultiIndex) else False

            plan.to_excel(writer, sheet_name=nomesheet, index=index)
            worksheet = writer.sheets[nomesheet]
            # adiciona os formatos as colunas
            if isinstance(plan.columns, pd.MultiIndex):
                worksheet.delete_cols(1)
                worksheet.delete_rows(len(plan.columns[0])+1)

        
        writer.save()
        w=openpyxl.load_workbook(b)
        
        return w


        
    def tobytes(self):
        w=openpyxl.writer.excel.save_virtual_workbook(self.w)
        return w

    
    def save(self, local):
        self.w.save(local)
        
        
    

