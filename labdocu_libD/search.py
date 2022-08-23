from . import store,matriz,lista

def estructurar_archivo(text,separar_palabras=False):
    if isinstance(text,list):
        estructurado=text

    else:
        text_paginas=text.split("###nueva_pagina###")
        estructurado=[]
        for pagina in text_paginas:
            lineas=pagina.split("\n")
            estructurado.append(lineas)

    if separar_palabras==True:
        estructurado_splited=[]
        for pagina in estructurado:
            pagina2=[]
            for linea in pagina:
                linea2=linea.split(" ")
                pagina2.append(linea2)
            estructurado_splited.append(pagina2)
        estructurado=estructurado_splited

    return estructurado

def estructurar_archivos(paths_archivos,imprimir_progreso=False):
    archivos=[]
    for n_file,file in enumerate(paths_archivos):
        if imprimir_progreso==True:
            print("estructurado "+str(n_file)+"/"+str(len(paths_archivos))+": "+file)
        contenido,status=store.auto_load(file)
        estruct=estructurar_archivo(contenido,separar_palabras=True)
        archivos.append([file,estruct,status])
    return archivos

#genera a partir de la lista de archivos estructurados de la funcion anterior un indice con la siguiente estructura:
#[palabra,archivos,paginas,lineas,posiciones]
def indexar(archivos,imprimir_progreso=False):
    indice=[[],[],[],[],[]]
    for n_archivo,archivo in enumerate(archivos):
        contenido=archivo[1]
        for n_pagina,pagina in enumerate(contenido):
            for n_linea,linea in enumerate(pagina):
                for n_palabra,palabra in enumerate(linea):
                    if palabra in indice[0]:
                        p_palabra=indice[0].index(palabra)
                        if n_archivo in indice[1][p_palabra]:
                            p_archivo=indice[1][p_palabra].index(n_archivo)
                            if n_pagina in indice[2][p_palabra][p_archivo]:
                                p_pagina=indice[2][p_palabra][p_archivo].index(n_pagina)
                                if n_linea in indice[3][p_palabra][p_archivo][p_pagina]:
                                    p_linea=indice[3][p_palabra][p_archivo][p_pagina].index(n_linea)
                                    if n_palabra in indice[4][p_palabra][p_archivo][p_pagina][p_linea]:
                                        continue
                                    else:
                                        indice[4][p_palabra][p_archivo][p_pagina][p_linea].append(n_palabra)
                                else:
                                    indice[3][p_palabra][p_archivo][p_pagina].append(n_linea)
                                    indice[4][p_palabra][p_archivo][p_pagina].append([n_palabra])
                            else:
                                indice[2][p_palabra][p_archivo].append(n_pagina)
                                indice[3][p_palabra][p_archivo].append([n_linea])
                                indice[4][p_palabra][p_archivo].append([[n_palabra]])                     
                        else:
                            indice[1][p_palabra].append(n_archivo)
                            indice[2][p_palabra].append([n_pagina])
                            indice[3][p_palabra].append([[n_linea]])
                            indice[4][p_palabra].append([[[n_palabra]]])
                    else:
                        indice[0].append(palabra)
                        indice[1].append([n_archivo])
                        indice[2].append([[n_pagina]])
                        indice[3].append([[[n_linea]]])
                        indice[4].append([[[[n_palabra]]]])
        if imprimir_progreso==True:
            print("Indexado "+str(n_archivo)+"/"+str(len(archivos))+": "+archivo[0])
    indicet=matriz.transponer(indice)
    indicet.sort()
    indice=matriz.transponer(indicet)
    return indice

#busqueda binaria. Devuelve la posicion en una lista del arreglo buscado. Si no la encuentra, devuelve -1
def binaria(arreglo, busqueda):
    izquierda, derecha = 0, len(arreglo) - 1
    while izquierda <= derecha:
        indiceDelElementoDelMedio = (izquierda + derecha) // 2
        elementoDelMedio = arreglo[indiceDelElementoDelMedio]
        if elementoDelMedio == busqueda:
            return indiceDelElementoDelMedio
        if busqueda < elementoDelMedio:
            derecha = indiceDelElementoDelMedio - 1
        else:
            izquierda = indiceDelElementoDelMedio + 1
    return -1

def leven_ponderado(str1, str2):
  mayor=max([len(str1),len(str2)])
  if mayor==0:
     mayor=1
	 
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
   
  return (((d[len(str1)][len(str2)])/mayor)*100)

def levenshtein(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]

#Toma el indice y la palabra a buscar, opcionalmente aplica levenshtein ponderado. 
# Devuelve una matriz con la palabra, archivo, pagina y posicion (el numero)
def buscar_palabra(indice,palabra,levenponderado=0):
    resultados=[]
    if levenponderado==0:
        posicion=binaria(indice[0],palabra)
        if posicion!=-1:
            resultado=[indice[0][posicion],indice[1][posicion],indice[2][posicion],indice[3][posicion],indice[4][posicion]]
            resultados.append(resultado)
    else:
        for posicion,p_indice in enumerate(indice[0]):
            if leven_ponderado(p_indice,palabra)<=levenponderado:
                resultado=[indice[0][posicion],indice[1][posicion],indice[2][posicion],indice[3][posicion],indice[4][posicion]]
                resultados.append(resultado)

    return resultados

#a partir de la matriz de resultados y la cadena de archivos estructurados genera una matriz de resultados donde el numero de archivo se
#reemplaza por el nombre real y se agrega en una columna la linea completa como referencia
def index_to_matrix(resultados):
    #matrix=[["palabra","n_archivo","n_pagina","n_linea","n_posicion","linea"]]
    matrix=[]
    for resultado in resultados:
        palabra=resultado[0]
        for n_archivo,archivo in enumerate(resultado[1]):
            for n_pagina,pagina in enumerate(resultado[2][n_archivo]):
                for n_linea,linea in enumerate(resultado[3][n_archivo][n_pagina]):
                    for n_posicion, posicion in enumerate(resultado[4][n_archivo][n_pagina][n_linea]):
                        caso=[palabra,archivo,pagina,linea,posicion]
                        matrix.append(caso)
    return matrix


#se explica solo
def palabra_individual(indice,palabra,estructurado,levenponderado=0):
    resultados=buscar_palabra(indice,palabra,levenponderado)
    matrix=index_to_matrix(resultados,estructurado)
    return matrix




def orientada(indice,palabras,estructurado,levenponderado=0,palabras_faltantes=0,ordenadas=True,saltos=0):
    matrix=[]
    palabras_buscadas=palabras.split(" ")#separacion de palabras a buscar


    for palabra in palabras_buscadas:
        pivot=buscar_palabra(indice,palabra,levenponderado)
        matrix_pivot=index_to_matrix(pivot)
        #lista.show(matrix_pivot)

        for pivot in matrix_pivot:
            n_archivo=pivot[1]
            n_pagina=pivot[2]
            n_linea=pivot[3]
            n_palabra=pivot[4]
            archivo=estructurado[n_archivo][0]
            pagina=estructurado[n_archivo][1][n_pagina]
            linea=estructurado[n_archivo][1][n_pagina][n_linea]
            

            ##### AGREGADO DE LINEAS ANTERIORES Y POSTERIORES
            largo_pagina=len(estructurado[n_archivo][1][n_pagina])-1
            largo_archivo=len(estructurado[n_archivo][1])
            #Agregado de linea previa
            if n_linea==0:#si es la primer linea de la pagina
                if n_pagina==0:#si es la primer pagina
                    linea_previa=[]
                else:#sino
                    largo_pagina_previa=len(estructurado[n_archivo][1][n_pagina-1])-1
                    linea_previa=estructurado[n_archivo][1][n_pagina-1][largo_pagina_previa]
            else:#si no es la primer linea de la pagina
                linea_previa=estructurado[n_archivo][1][n_pagina][n_linea-1]

            #Agregado de linea posterior
            if n_linea==largo_pagina:#si es la ultima linea de la pagina
                if n_pagina==largo_archivo:#si es la ultima pagina del archivo
                    linea_posterior=[]
                else:
                    linea_posterior=estructurado[n_archivo][1][n_pagina+1][0]
            else:
                linea_posterior=estructurado[n_archivo][1][n_pagina][n_linea+1]

            #Generacion de fragmento de busqueda
            multilinea=linea+linea_posterior
            l_multilinea=len(multilinea)
            posicion=len(linea_previa)+n_palabra
            n_palabras=len(palabras_buscadas)

            if posicion+(n_palabras)+saltos>l_multilinea-1:
                p_final=l_multilinea-1
            else:
                p_final=posicion+(n_palabras)+saltos
            
            fragmento=(multilinea[posicion:p_final])

            #busqueda de posiciones
            posiciones=[]
            for buscada in palabras_buscadas:
                if levenponderado==0:
                    print(buscada)
                    if buscada in fragmento:
                        p_fragmento=fragmento.index(buscada)
                        posiciones.append(p_fragmento+posicion)
                else:
                    for p_fragmento,palabra in enumerate(fragmento):
                        if leven_ponderado(buscada,palabra)<levenponderado:
                            posiciones.append(p_fragmento+posicion)
                        else:
                            continue
            posiciones.sort()

            #chequeo de numero de palabras
            if len(posiciones)>=n_palabras-palabras_faltantes:
                #chequeo de orden
                if ordenadas==True:
                    check=1
                    for pre,pos in enumerate(posiciones[1:]):
                        #print(str(pos)+"   "+str(posiciones[pre]))
                        if posiciones[pre]<pre:
                            continue
                        else:
                            check=0
                    if check==1:
                        resultado_fragmento=posiciones
                    else:
                        resultado_fragmento=[]

                else:
                    resultado_fragmento=posiciones
            else:
                resultado_fragmento=[]

            registro=[palabras,archivo,n_pagina,n_linea,resultado_fragmento," ".join(multilinea)]
            if resultado_fragmento!=[] and not registro in matrix:
                matrix.append(registro)
    return matrix