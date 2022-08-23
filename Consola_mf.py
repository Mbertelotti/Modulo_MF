import yfinance as yf
import pandas as pd
from labdocu_lib import store,lista,matriz
from datetime import datetime
from mf import history
import matplotlib.pyplot as plt

start="2001-01-01"
end="2022-08-10"

tablat=store.load_xlsx(r"C:\Users\Mbertelotti\Desktop\Modulo_MF\Tickers.xlsx")
tabla=matriz.transponer(tablat)
tickers=tabla[0]
historicos=history.multi_yahoo(tickers,start=start,end=end,show_progress=True)
store.save(historicos,r"C:\Users\Mbertelotti\Desktop\eco\historicos")
historicos=store.load(r"C:\Users\Mbertelotti\Desktop\eco\historicos")
lista.show(historicos)

# unidos=history.unificar(historicos)
# unidos.to_excel(r"C:\Users\Mbertelotti\Desktop\eco\historicos.xlsx")


# # store.save(unidos,r"C:\Users\Mbertelotti\Desktop\eco\unificados")
# unidos=store.load(r"C:\Users\Mbertelotti\Desktop\eco\unificados")



# filtrada=history.filtrar_fecha(unidos,desde="2020-01-01",hasta=end)
# correlaciones=history.tabla_correlaciones(filtrada)

# store.save(correlaciones,r"C:\Users\Mbertelotti\Desktop\eco\cedears_correlaciones")
# correlaciones=store.load(r"C:\Users\Mbertelotti\Desktop\eco\cedears_correlaciones")
# correlaciones.to_excel(r"C:\Users\Mbertelotti\Desktop\eco\cedears_correlaciones.xlsx",index=False)

# def variaciones(combo,desde,hasta):
#     combo=combo.loc[desde:hasta]
#     columnas=combo.columns
#     vars=[]
#     for columna in columnas[1:]:
#         primer=combo[columna].iloc[0]
#         ultimo=combo[columna].iloc[-1]
#         variacion=(ultimo-primer)/primer
#         vars.append(variacion)
#     variaciones=pd.DataFrame({
#         "ticker":columnas[1:],
#         "variaciones":vars
#     })
#     return(variaciones)

# var=variaciones(unidos,start,end)
# print(var)
# var.to_excel(r"C:\Users\Mbertelotti\Desktop\eco\variaciones.xlsx",index=False)

# cartera=[["HSBC",1],["EBR",4],["GOLD",1],["PEP",1]]
# def cartera_historica(cartera,combo):
#     PF=combo[["Date",cartera[0][0]]]
#     for valor in cartera[1:]:
#         ticker=valor[0]
#         for n in range(valor[1]):
#             PF=pd.merge(PF,combo[["Date",ticker]],on=["Date"])
#     PF["Suma"]=PF.iloc[:,1:].sum(axis=1)
#     return PF

# hist=cartera_historica(cartera,combo)
# hist.to_excel(r"C:\Users\Mbertelotti\Desktop\eco\cartera.xlsx",index=False)




# tabladf=tabla_correlaciones(correlaciones)
# print(tabladf)
# tabladf.to_excel(r"C:\Users\Mbertelotti\Desktop\eco\correlacion.xlsx",index=False)



# Merge admite un campo o varios como criterio de combinacion. 
# Por defecto el join es inner, es decir, elimina los registros sin coincidencia
# se puede usar on= cuando los dos dataframes contienen la misma columna o on_right= y on_left= cuando no
# how es el tipo de join, puede ser outer, inner, left o right
# https://www.youtube.com/watch?v=wzN1UyfRSWI
# nueva=pd.merge(XOM["Close"],AAPL["Close"],on=["Date"],suffixes=["_XOM","_AAPL"],how="outer")
# print(nueva.head(30))
# correlacion=nueva.corr(method="pearson")
