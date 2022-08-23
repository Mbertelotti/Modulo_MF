from tb import csv
import pandas as pd

def new_table(columnas):
	new=[[]]
	for columna in columnas:
		new=add_col(new,columna)
	return(new)

def add_row(table,row):
	table.append(row)
	return list

def add_col(table,col):
	transp_tabla=transponer(table)
	transp_tabla.append(col)
	table=transponer(transp_tabla)
	return table

def del_col(tabla,col):
	nueva_tabla=[]
	for linea in tabla:
		nueva_linea=[]
		for id_col,elemento in enumerate(linea):
			if id_col==col:
				continue
			else:
				nueva_linea.append(elemento)
		nueva_tabla.append(nueva_linea)
	return nueva_tabla

def crear_columna_fija(table,valor_fijo):
	columna_nueva=[]
	for x in range(len(table)):
		columna_nueva.append(valor_fijo)

	table=add_col(table,columna_nueva)
	return table

def move(lista,pos1,pos2):
	if pos1>pos2:
		row=lista[pos1]
		lista.pop(pos1)
		lista.insert(pos2,row)
	else:
		row=lista[pos1]
		lista.pop(pos1)
		lista.insert(pos2,row)
	return lista

def move_row(tabla,pos1,pos2):
	pos1=pos1-1
	pos2=pos2-1
	tabla=move(tabla,pos1,pos2)
	return tabla

def move_col(tabla,pos1,pos2):
	transpuesta=transponer(tabla)
	transpuesta=move(transpuesta,pos1,pos2)
	tabla=transponer(transpuesta)
	return tabla

def extraer_columna(tabla,numero_columna):
	columna=[]
	for x in tabla:
		columna.append(x[numero_columna])
	return columna

def split(tabla,columna):
	guia=[]
	splited=[]
	for row in tabla:
		if row[columna] in guia:
			pos=guia.index(row[columna])
			splited[pos].append(row)
		else:
			splited.append([row])
			guia.append(row[columna])

	return splited

def transponer(tabla):
	transpuesta=[]
	for n_col in range(len(tabla[0])):
		nueva_fila=[]
		for fila in tabla:
			try:
				nueva_fila.append(fila[n_col])
			except:
				nueva_fila.append("")
		transpuesta.append(nueva_fila)
	return transpuesta

def generar_ids(lista):
	ids=[]
	largo=len(lista)
	for num in range(largo):
		ids.append(num)
	return ids

def buscarv_lista(lista,tabla,columna):
	tabla_t=transponer(tabla)
	resultados=[]
	for x in lista:
		if x!="" and x in tabla_t[0]:
			posicion=tabla_t[0].index(x)
			resultados.append(tabla_t[columna-1][posicion])
		else:
			resultados.append("")
	return resultados

def buscarv(elemento,tabla,columna):
	tabla_t=transponer(tabla)
	if elemento!="" and elemento in tabla_t[0]:
		posicion=tabla_t[0].index(elemento)
		resultado=tabla_t[columna-1][posicion]
	else:
		resultado=""
	return resultado

def buscarv_rapido(elemento,tabla_transpuesta,columna_buscada,columna_resultado):
	if elemento!="" and elemento in tabla_transpuesta[columna_buscada]:
		posicion=tabla_transpuesta[columna_buscada].index(elemento)
		resultado=tabla_transpuesta[columna_resultado][posicion]
	else:
		resultado=""
	return resultado

def filter(tabla,columna,criterio):
	nueva_tabla=[]
	for linea in tabla:
		if linea[columna-1]==str(criterio):
			nueva_tabla.append(linea)
	return nueva_tabla

def filter_head(csv,columna,criterio):
	header=csv[0]
	filtrado=filter(csv,columna,criterio)
	tabla=[]
	tabla.append(header)
	for linea in filtrado:
		tabla.append(linea)
	return tabla


def split_header(tabla):
	header=tabla[0]
	tabla=tabla[1:]
	return header,tabla

def add_header(tabla,header):
	nueva_tabla=[header]
	for linea in tabla:
		nueva_tabla.append(linea)
	return nueva_tabla

# estallar toma una matriz de datos con cabecera y un numero de columna (n_columna) como parametros obligatorios 
# y la divide en varias matrices tomando como parametro de división los datos de la columna aportada.
#El parametro opcional incluir_header puede usarse para indicar si las tablas resultantes de la division deben contener cabecera
# o solamente los datos
def estallar(tabla,n_columna,contiene_header=False,incluir_header=False):
	if contiene_header==True:
		header=tabla[0]
		tabla=tabla[1:]
	else:
		pass

	tablas=[]
	guia=[]
	for linea in tabla:
		if linea[n_columna] in guia:
			pos_guia=guia.index(linea[n_columna])
			tablas[pos_guia].append(linea)
		else:
			guia.append(linea[n_columna])
			if incluir_header==False:
				tablas.append([linea])
			else:
				tablas.append([header,linea])
	
	return tablas

def unificar(tablas):
	tabla_total=[]
	for tabla in tablas:
		for linea in tabla:
			tabla_total.append(linea)
	return tabla_total

def ordenarpor(tabla,columna,orden="ascendente"):
	tabla=move_col(tabla,columna,0)
	tabla.sort()
	tabla=move_col(tabla,0,columna)
	return tabla

def concatenar(tabla,n_col1,n_col2,separador=" "):
	tablat=transponer(tabla)
	col1=tablat[n_col1]
	col2=tablat[n_col2]
	col_concatenada=[]
	for d1,d2 in zip(col1,col2):
		valor=str(d1)+separador+str(d2)
		col_concatenada.append(valor)
	tabla2=add_col(tabla,col_concatenada)
	return tabla2

def dftotabla(dataframe):
    tabla=dataframe.values.tolist()
    return tabla

def tablatodf(tabla):
    dataframe=pd.DataFrame(tabla)
    return dataframe

def media(lista):
	suma=0
	for x in lista:
		suma=suma+x
	media=suma/len(lista)
	return media

def media_movil(lista,numero):
	media_movil=[]
	for n,elemento in enumerate(lista):
		if n<numero:
			media_movil.append(media(lista[:n+1]))
		if n>=numero:
			media_movil.append(media(lista[n+1-numero:n+1]))
	return media_movil

def variacion(lista):
	variaciones=[]
	for n,elemento in enumerate(lista):
		if n==0:
			variaciones.append(0)
		if n>0:
			elemento_anterior=lista[n-1]
			variaciones.append((elemento-elemento_anterior)/elemento_anterior)
	return variaciones