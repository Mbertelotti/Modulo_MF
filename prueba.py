import yfinance as yf
from tb import matriz,lista

ticker=yf.Ticker("AMZN")
# cash=ticker.cashflow
# op=lista.invertir(cash.loc["Total Cash From Operating Activities"].tolist())
# capex=lista.invertir(cash.loc["Capital Expenditures"].tolist())
# fcf=[]
# for a,b in zip(op,capex):
#     fcf.append(a+b)


# balance=ticker.balance_sheet
# activo=balance.loc["Total Assets"].tolist()[0]
# pasivo=balance.loc["Total Liab"].tolist()[0]

resultados=ticker.financials
beneficios=resultados.loc["Net Income Applicable To Common Shares"].tolist()[0]

info=ticker.info
n_acciones=info['sharesOutstanding']
print(n_acciones)
currentPrice=info['currentPrice']
print(currentPrice)
eps=beneficios/n_acciones
print(eps)