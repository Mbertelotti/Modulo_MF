import os
import shutil

############################ LISTADO DE ARCHIVOS EN CARPETA ###############################################

#toma un path raiz como parametro y genera una lista de los paths de archivos contenidos en esa raiz
def list_dir(input):
	dires=[]
	for root,dirs,files in os.walk(input):
		for archivo in files:
			dires.append(root+"\\"+archivo)
	return dires

#toma una lista de archivos y devuelve una lista desduplicada de las extensiones
def list_ext(paths_archivos):
    extensiones=[]
    for path in paths_archivos:
        archivo,extension=os.path.splitext(path)
        if extension in extensiones:
            continue
        else:
            extensiones.append(extension)
    return extensiones

#recibir listas de palabra y categorias




############################################# DATOS DE CARPETA ##############################################
#toma una lista de archivos y devuelve el conteo de los mismos
def count_files(input):
	count=0
	for root,dirs,files in os.walk(input):
		for archivo in files:
			count=count+1
	return count

#toma una lista de paths de archivos y devuelve una lista que contiene el numero de archivos, el numero de carpetas, el peso total y las unidades de peso, en ese orden
def stats_folder(input):
	file_count=0
	size=0
	folder_count=-1
	for root,dirs,files in os.walk(input):
		folder_count=folder_count+1
		for archivo in files:
			sizefile = os.stat(root+"\\"+archivo).st_size
			size=size+sizefile
			file_count=file_count+1

	if size/(1024*1024*1024)>1:
		size=size/(1024*1024*1024)
		units="GB"
	elif size/(1024*1024)>1:
		size=size/(1024*1024)
		units="MB"
	elif size/(1024)>1:
		size=size/(1024)
		units="KB"
	else:
		units="Bytes"
	
	return([file_count,folder_count,size,units])

def print_dir(input):
	dires=[]
	for root,dirs,files in os.walk(input):
		for archivo in files:
			print(root+"\\"+archivo)

#recibe un path raiz y una lista de extensiones y devuelve una lista de paths de archivos correspondientes a esas extensiones
def filtrar_ext(input,extensiones):
	dires=[]
	for root,dirs,files in os.walk(input):
		for archivo in files:
			for extension in extensiones:
				if archivo.upper().endswith(extension.upper()):
					dires.append(root+"\\"+archivo)
				else:
					continue
	return dires



def multi_dir(raices):
	multipaths=[]
	for raiz in raices:
		lista=list_dir(raiz)
		multipaths.append(lista)
	return multipaths

def list_basenames(paths):
	basenames=[]
	for path in paths:
		basename=os.path.basename(path)
		basenames.append(basename)
	return basenames

def multi_func(lista,func):
	nueva_lista=[]
	for elemento in lista:
		nuevo_elemento=eval(func)
		nueva_lista.append(nuevo_elemento)
	return nueva_lista


####################################### COPIADO DE ARCHIVOS #################################################


def copy_files(paths,destinos,imprimir="NO"):
	estado=[]
	for path,destino in zip(paths,destinos):
		try:
			shutil.copy2(path,destino)
			x="exito"
		except:
			x="fallido"
		estado.append(x)
		if imprimir=="SI":
			print(destino+" - "+x)
		else:
			continue
	return estado

def copy_treefiles(paths,destino):
	estado=[]
	for path,destino in zip(paths,destino):
		try:
			#shutil.copy2(path,destino)
			shutil.copytree(path,destino) 
			estado.append("exito")
		except:
			estado.append("fallido")
	return estado

def nuevos_path(paths,carpeta_destino):
	nuevos_path=[]
	for idx,path in enumerate(paths):
		if path!="":
			nombre=os.path.basename(path)
			nuevo_nombre=nombre
			nuevo_path=os.path.join(carpeta_destino,nuevo_nombre)
			nuevos_path.append(nuevo_path)
		else:
			nuevos_path.append("")
	return nuevos_path

def nuevos_path_tree(paths,carpeta_destino):
	nuevos_path=[]
	for idx,path in enumerate(paths):
		if path!="":
			nombre=os.path.basename(path)
			nuevo_nombre=nombre
			nuevo_path=os.path.join(carpeta_destino,nuevo_nombre)
			nuevos_path.append(nuevo_path)
		else:
			nuevos_path.append("")
	return nuevos_path

def nuevos_path_conID(paths,carpeta_destino):
	nuevos_path=[]
	for idx,path in enumerate(paths):
		if path!="":
			nombre=os.path.basename(path)
			nuevo_nombre=str(idx)+"-"+nombre
			nuevo_path=os.path.join(carpeta_destino,nuevo_nombre)
			nuevos_path.append(nuevo_path)
		else:
			nuevos_path.append("")
	return nuevos_path

def copy(input,carpeta_destino,imprimir="NO"):
	paths=list_dir(input)
	nuevos=nuevos_path(paths,carpeta_destino)
	estados=copy_files(paths,nuevos,imprimir)
	resultados=[paths,nuevos,estados]
	return resultados

def copy_tree(input,carpeta_destino):
	paths=list_dir(input)
	estados=copy_treefiles(paths,carpeta_destino)
	resultados=[paths,estados]
	return resultados