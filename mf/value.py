from unittest import result
import yfinance as yf
from datetime import date
from tb import lista,matriz



#wa0090
def load_tickers(tickers_lista,show_progress=False):
    tickers=[]
    for ticker in tickers_lista:
        datos=yf.Ticker(ticker)
        tickers.append(datos)
        if show_progress==True:
            print(ticker+" - Cargado")
    return tickers

def load_ratios(tickers,show_progress=True):
    resultados=[]
    today = date.today()
    for ticker in tickers:
        try:

            balance=ticker.balance_sheet
            activo=balance.loc["Total Assets"].tolist()[0]
            pasivo=balance.loc["Total Liab"].tolist()[0]
            solvencia=activo/pasivo



            cash=ticker.cashflow
            op=lista.invertir(cash.loc["Total Cash From Operating Activities"].tolist())
            capex=lista.invertir(cash.loc["Capital Expenditures"].tolist())
            fcf=[]
            for a,b in zip(op,capex):
                fcf.append(a+b)
            
            info=ticker.info
            history=ticker.history()
            currentPrice=info['currentPrice']
            symbol=info['symbol']
            shortName=info['shortName']
            n_acciones=info['sharesOutstanding']
            forwardEps=info['forwardEps']
            trailingEps=info['trailingEps']
            # priceToBook=info['priceToBook']
            # beta=info['beta']
            # pegRatio=info['pegRatio']
            forwardPER=currentPrice/forwardEps
            trailingPER=currentPrice/trailingEps
            # returnOnAssets=info['returnOnAssets']
            # returnOnEquity=info['returnOnEquity']
            # debtToEquity=info['debtToEquity']
            #resultado=[symbol,shortName,n_acciones,forwardEps,trailingEps,priceToBook,beta,pegRatio,forwardPER,trailingPER,returnOnAssets,returnOnEquity,debtToEquity]
            resultado=[symbol,shortName,n_acciones,currentPrice,forwardPER,trailingPER,activo,pasivo,solvencia,fcf[0],fcf[1],fcf[2],fcf[3]]
            #print(resultado)
            if show_progress==True:
                print(symbol+" - Cargado")
            resultados.append(resultado)
        except:
            continue
    return resultados
