import yfinance as yf
import pandas as pd
from tb import store,list
from datetime import datetime

def multi_yahoo(tickers,start,end):
    cotizaciones=[]
    for ticker in tickers:
        datos=yf.Ticker(ticker)
        historico=datos.history(start=start,end=end)
        reg=[ticker,historico]
        cotizaciones.append(reg)
        print(ticker)
    return cotizaciones

def unificar(cotizaciones):
    #combinado=cotizaciones[0][1]["Close"]
    combinado=pd.DataFrame(cotizaciones[0][1].index)
    #print(combinado)
    for cotizacion in cotizaciones:#[1:]:
        historico=cotizacion[1]["Close"]
        ticker=cotizacion[0]
        combinado=pd.merge(combinado,historico,on=["Date"],suffixes=["","_"+ticker],how="outer")
        combinado.rename(columns = {'Close_'+ticker:ticker}, inplace = True)
        combinado.rename(columns = {'Close':ticker}, inplace = True)
        
    combinado.set_index("Date", inplace=True)
    combinado.sort_values(by=['Date'], inplace=True)
    #combinado.drop('Close', inplace=True, axis=1)
    return(combinado)

def filtrar_multi_fecha(cotizaciones,desde,hasta):
    for cotizacion in cotizaciones:
        cotizacion[1]=cotizacion[1].loc[desde:hasta]
    return(cotizaciones)

def filtrar_fecha(cotizaciones,desde,hasta):
    cotizaciones=cotizaciones.loc[desde:hasta]
    return(cotizaciones)

def tabla_correlaciones(unificado):
    correlaciones=unificado.corr(method="pearson")
    #correlaciones.to_excel(r"E:\Scripts\eco\BA\debug.xlsx")
    columnas=correlaciones.columns
    tabla=[]
    for n1,columna1 in enumerate(columnas):
        for n2,columna2 in enumerate(columnas):#[n1+1:]):
            #print(columna1+" - "+columna2)
            registro=[columna1,columna2,correlaciones[columna1][columna2]]
            tabla.append(registro)
    tabladf=pd.DataFrame(tabla,columns=("columna1","columna2","correlacion"))
    return tabladf

def variaciones(combo,desde,hasta):
    combo=combo.loc[desde:hasta]
    columnas=combo.columns
    vars=[]
    for columna in columnas:
        primer=combo[columna].iloc[0]
        ultimo=combo[columna].iloc[-1]
        variacion=(ultimo-primer)/primer
        vars.append(variacion)
    variaciones=pd.DataFrame({
        "ticker":columnas,
        "variaciones":vars
    })
    return(variaciones)