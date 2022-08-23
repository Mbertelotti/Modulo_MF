import pickle
import pandas as pd
from . import matriz,text
import textract
from pdfminer import high_level
import PyPDF2
import warnings
import os
import win32com.client

#permite guardar en una variable en un archivo.
def save(variable,path):
    pickle.dump(variable,open(path,"wb"))

#permite cargar una variable desde un archivo
def load(path):
    variable=pickle.load(open(path,"rb"))
    return variable

#permite guardar una lista en un archivo de texto
def save_list(lista,path):
	archivo=open(path,"w",encoding="utf8")
	for elemento in lista:
		archivo.write(str(elemento)+"\n")
	archivo.close()

#permite cargar una lista desde un archivo de texto
def load_list(path_archivo):
	historia_file=open(path_archivo,"r",encoding="utf8")
	tabla=[]
	for linea in historia_file:
		columna=linea.replace("\n","")
		tabla.append(columna)
	return tabla

#permite cargar una matriz de datos desde el path de un archivo .csv
def load_csv(path_archivo):
	historia_file=open(path_archivo,"r")
	tabla=[]
	for linea in historia_file:
		linea=linea.replace("\n","")
		columna=linea.split(";")
		tabla.append(columna)
	return tabla


def save_csv(tabla,path):
	file=open(path,"w",encoding="utf8")
	for linea in tabla:
		texto=""
		for columna in linea:
			texto=texto+str(columna)+";"
		texto=texto[:-1]+"\n"
		file.write(texto)
	file.close()

def save_txt(text,path,encoding="utf8"):
	file=open(path,"w",encoding="utf8")
	file.write(text)
	file.close()

def load_xlsx(path,hoja="S/H"):
	if hoja=="S/H":
		df=pd.read_excel(path)
	else:
		df=pd.read_excel(path,sheet_name=hoja)
	header=list(df.columns.values)
	tabla=df.values.tolist()
	tabla=matriz.add_header(tabla,header)
	tabla=text.table_to_string(tabla)
	return tabla

def save_xlsx(tabla,path,header=[]):
	if header==[]:
		df=pd.DataFrame(tabla)
		df.to_excel(path,index=False,header=False)
	else:
		df=pd.DataFrame(tabla,columns=header)
		df.to_excel(path,index=False)

def load_docx(path):
    text = textract.process(path)
    text=text.decode("utf8")
    return text

def load_doc(path):
	doc = win32com.client.GetObject(path)
	text = doc.Range().Text
	return text

def load_text(path):
	file=open(path,"r")
	texto=""
	for linea in file:
		texto=texto+" "+linea
	return texto


#Toma un path de un pdf y devuelve una lista de cadenas de texto con el contenido de cada pagina
def load_pdf(input,devolver_paginas=False):
	with warnings.catch_warnings():#uso esta libreria para evitar advertencias sin sentido que se imprimen en pantalla
		warnings.simplefilter('ignore')#uso esta libreria para evitar advertencias sin sentido que se imprimen en pantalla
		extracted_text = high_level.extract_text(input)#para hacer que funcione con archivos protegidos (no extraibles), cambie a false la variable check_extractable de la funcion extract_text

		readpdf = PyPDF2.PdfFileReader(input)#utilizo pypdf2 para extraer el numero de paginas
		totalpages = readpdf.numPages#idem

		#extraigo las paginas una a una guardando el contenido en la cadena textos
		texto=""
		for n_pag in range(totalpages):
			extracted_text = high_level.extract_text(input,page_numbers=[n_pag])
			texto=texto+extracted_text+"\n ###nueva_pagina### \n"
		if devolver_paginas==True:
			cadena=texto.split("###nueva_pagina###")
			return cadena
		else:
			return texto

#toma el path de un archivo y si tiene una extensión compatible aplica la correspondiente funcion de extracción.
#devuelve las variables contenido, que contiene una lista con las paginas/lineas(matrices) del archivo y una variable status 
# que indica cuando no se pudo extraer el contenido por no ser compatible el formato 
# o devuelve el error generado por alguna de las funciones utilizadas
def auto_load(path):
	plower=path.lower()
	try:
		if plower.endswith(".docx"):
			texto=load_docx(path)
			contenido=texto
			status="Extraido: .docx"
			return contenido,status

		if plower.endswith(".doc"):
			texto=load_doc(path).replace("\r","\n")
			contenido=texto
			status="Extraido: .doc"
			return contenido,status

		elif plower.endswith(".xlsx") or plower.endswith(".xls"):
			contenido=load_xlsx(path)
			status="Extraido: .xlsx o .xls"
			return contenido,status

		elif plower.endswith(".csv"):
			texto=load_text(path)
			contenido=texto
			status="Extraido: .csv"
			return contenido,status

		elif plower.endswith(".txt"):
			texto=load_text(path)
			contenido=texto
			status="Extraido: .txt"
			return contenido,status

		elif plower.endswith(".pdf"):
			contenido=load_pdf(path)
			status="Extraido: .pdf"
			return contenido,status

		else:
			contenido="S/C"
			status="Error de carga: Formato incompatible"
			return contenido,status

	except Exception as e:
		contenido="S/C"
		status="Error de carga:"+str(e)
		return contenido,status