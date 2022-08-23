import yfinance as yf
import pandas as pd
from labdocu_lib import store,lista,matriz
from datetime import datetime
from mf import history,value
import matplotlib.pyplot as plt

start="2001-01-01"
end="2022-08-10"

tablat=store.load_xlsx(r"C:\Users\Mbertelotti\Desktop\Modulo_MF\Tickers.xlsx")
tabla=matriz.transponer(tablat)
tickers_lista=tabla[0]



tickers=value.load_tickers(tickers_lista,show_progress=True)

store.save(tickers,r"C:\Users\Mbertelotti\Desktop\Modulo_MF\out\tickers_data.manu")
tickers=store.load(r"C:\Users\Mbertelotti\Desktop\Modulo_MF\out\tickers_data.manu")

pos=tickers_lista.index("AMZN")
resultados=value.load_ratios(tickers,show_progress=True)

header=["symbol","shortName","n_acciones","currentPrice","forwardPER","trailingPER","activo","pasivo","solvencia","fcf1","fcf2","fcf3","fcf4"]
store.save_xlsx(resultados,r"C:\Users\Mbertelotti\Desktop\Modulo_MF\out\tickers_data.xlsx",header=header)
