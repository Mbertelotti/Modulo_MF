def show(lista):
	for x in lista:
		print(x)

def desduplicar(lista):
	seted=set(lista)
	lista=[]
	for x in seted:
		lista.append(x)
	return lista

def desduplicar2(lista):
	desduplicada=[]
	for x in lista:
		if x not in lista:
			desduplicada.append(x)
	return desduplicada

def invertir(lista):
	invertida=[]
	for iteracion in range(len(lista)):
		invertida.append(lista[len(lista)-iteracion-1])
	return invertida

def nueva(largo,contenido=""):
	lista_vacia=[]
	for x in range(largo):
		lista_vacia.append(contenido)
	return lista_vacia