def txttolist(path_txt,encoding="utf-8"):
    list=[]
    try:
        archivo=open(path_txt,"r",encoding=encoding)
        for linea in archivo:
            linea_split=linea.replace("\n","").split(sep=" ")
            for string in linea_split:
                list.append(string)
    except:
        list.append("EXTRACCION FALLIDA")
    return list

def list_alfanumeric(list):
    new_list=[]
    for palabra in list:
        nueva_palabra=""
        for caracter in palabra:
            if caracter.isalpha() or caracter.isnumeric():
                nueva_palabra=nueva_palabra+caracter
            else:
                nueva_palabra=nueva_palabra+" "
        if nueva_palabra!="":
            if " " not in nueva_palabra:
                new_list.append(nueva_palabra)
            else:
                cadena=nueva_palabra.split(" ")
                for elemento in cadena:
                    if elemento!="":
                        new_list.append(elemento)
    return new_list

def to_string(num_list):
	stringueada=[]
	for x in num_list:
		stringueada.append(str(x))
	return stringueada

def table_to_string(table):
    tabla_string=[]
    for registro in table:
        reg_string=[]
        for campo in registro:
            reg_string.append(str(campo))
        tabla_string.append(reg_string)
    return tabla_string