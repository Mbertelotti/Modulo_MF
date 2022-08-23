from tb import csv,list
from haversine import inverse_haversine,Direction
from math import pi


def cuerpo(estilos,folders,nombre_documento="Sin Nombre",formas=""):
  if formas!="":
    folder_formas=f"""
    <Folder>
      <name>Formas</name>
      {formas}
    </Folder>"""
  else:
    pass
  text=f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{nombre_documento}</name>
    <description/>
    {estilos}
    {folders}
    {formas}
  </Document>
</kml>
  """
  return text

def create_placemark(row,header):
    #####  excluyo el campo folder ############
    placemark_row=[]
    placemark_header=[]
    for dat,head in zip(row,header):
        if head!="Folder":
            placemark_row.append(dat)
            placemark_header.append(head)
        else:
            pass
          
    ###### Ubicacion de parametros generales ########
    pos_name=placemark_header.index("Name")
    pos_modelo=placemark_header.index("modelo_icono")
    pos_color=placemark_header.index("color_icono")
    pos_fecha=placemark_header.index("Fecha")
    pos_hora=placemark_header.index("Hora")

    name=placemark_row[pos_name]

    modelo=placemark_row[pos_modelo]
    color=placemark_row[pos_color]
    style=generar_style_id(color,modelo)

    latitud=placemark_row[placemark_header.index("Latitud")]
    longitud=placemark_row[placemark_header.index("Longitud")]
    ################ generacion de description y data ###############
    datas=""
    descripcion=""
    for pos_zip,(dat,head) in enumerate(zip(placemark_row,placemark_header)):
        if (pos_zip!=pos_name) and (pos_zip!=pos_modelo) and (pos_zip!=pos_color):
            data=f"""
          <Data name=\"{head}\">
            <value>{dat}</value>
          </Data>"""
            datas=datas+data
            descrip=f"{head}: {dat}<br>"
        else:
            continue
    
    hora=placemark_row[pos_hora]
    fecha=placemark_row[pos_fecha]
    descripcion=descripcion[:len(descripcion)-4]
    fecha_s=fecha.split("/")
    if len(fecha_s)==3:
      fecha=fecha_s[2]+"-"+fecha_s[1]+"-"+fecha_s[0]
    else:
      pass
    placemark_body=f"""
      <Placemark>
        <TimeStamp>
          <when>{fecha}T{hora}</when>
        </TimeStamp>
        <name>{name}</name>
        <description><![CDATA[{descripcion}]]></description>
        <styleUrl>#{style}</styleUrl>
        <ExtendedData>
        {datas}
        </ExtendedData>
        <Point>
          <coordinates>
            {longitud},{latitud}
          </coordinates>
        </Point>
      </Placemark>"""
    
    icon_style=f"""
    <Style id="{style}-normal">
      <IconStyle>
        <color>ff468442</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>

    <Style id="{style}-highlight">
      <IconStyle>
        <color>ff4f0e88</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>

    <StyleMap id="{style}">
      <Pair>
        <key>normal</key>
        <styleUrl>#{style}-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#{style}-highlight"</styleUrl>
      </Pair>
    </StyleMap>"""
    return placemark_body,icon_style

def crear_placemarks(tabla,header):
  placemarks=""
  estilos=""
  for linea in tabla:
    placemark,estilo=create_placemark(linea,header)
    placemarks=placemarks+placemark
    estilos=estilos+estilo
  return placemarks,estilos

def crear_linea_placemark(coordenadas1,coordenadas2,fecha="",hora=""):
  if fecha!="":
    #print(fecha)
    fecha_s=fecha.split("/")
    fecha=fecha_s[2]+"-"+fecha_s[1]+"-"+fecha_s[0]
  else:
    pass

  placemark_linea=f"""
      <Placemark>
        <TimeStamp>
          <when>{fecha}T{hora}</when>
        </TimeStamp>
        <name>.</name>
        <styleUrl>#line-000000-1200-nodesc</styleUrl>
        <LineString>
          <tessellate>1</tessellate>
          <coordinates>
            {coordenadas1[1]},{coordenadas1[0]}
            {coordenadas2[1]},{coordenadas2[0]}
          </coordinates>
        </LineString>
      </Placemark>
  """
  return placemark_linea

def crear_folders(tabla,header,formas=""):
  tablas_folder=csv.estallar(tabla,header.index("Folder"))
  folders=""
  styles=""
  for tabla_folder in tablas_folder:

    nombre_folder=tabla_folder[0][header.index("Folder")]
    placemarks,style=crear_placemarks(tabla_folder,header)
    folder=f"""
    <Folder>
      <name>{nombre_folder}</name>
      {placemarks}
      {formas}
    </Folder>
    """
    folders=folders+folder
    styles=styles+style
  
  return folders,styles

def area_cobertura(tabla,header):
  #extraccion de posiciones de columnas
  n_puntos=40
  pos_lat=header.index("Latitud")
  pos_lon=header.index("Longitud")
  pos_azimuth=header.index("Azimuth")
  pos_radio=header.index("Radio Cobertura en KM o Metros")

  placemark_areas=""#variable que va a contener la cadena de placemarks
  tabla=csv.concatenar(tabla,pos_lat,pos_lon)
  n=len(tabla[0])-1
  tablas=csv.estallar(tabla,n)

  for n,tabla in enumerate(tablas):#para cada tabla

    if tabla[0][pos_radio]=="":
      radio=float(1)
    else:
      radio=float(tabla[0][pos_radio])

    if tabla[0][pos_azimuth]=="":
      azimuth=0
      apertura=360
    else:
      azimuth=float(tabla[0][pos_azimuth])
      apertura=60

    angulo_inicio=(azimuth-apertura/2)
    angulo_base=(apertura/n_puntos)

    latitud=float(tabla[0][pos_lat])
    longitud=float(tabla[0][pos_lon])
    coordenadas=(latitud,longitud)
    if apertura==360:
      puntos=f""
    else:
      puntos=f"""
                {longitud},{latitud},0"""
    for numero in range(n_puntos):
      angulo=(angulo_inicio+(angulo_base*numero))*pi/180
      coordenadas_nuevas=inverse_haversine(coordenadas,radio,angulo)
      lat_nueva=str(coordenadas_nuevas[0])
      lon_nueva=str(coordenadas_nuevas[1])
      punto=f"""
                {lon_nueva},{lat_nueva},0"""
      puntos=puntos+punto
    placemark=f"""
    <Placemark>
      <name>Polígono sin título</name>
      <styleUrl>#poly-FF0000-1000-8-nodesc</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <tessellate>1</tessellate>
            <coordinates>
              {puntos}
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>"""
    placemark_areas=placemark_areas+placemark
    #print(n)
  estilo_areas="""
    <Style id="poly-FF0000-1000-8-nodesc-normal">
      <LineStyle>
        <color>ff0000ff</color>
        <width>1</width>
      </LineStyle>
      <PolyStyle>
        <color>080000ff</color>
        <fill>1</fill>
        <outline>1</outline>
      </PolyStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="poly-FF0000-1000-8-nodesc-highlight">
      <LineStyle>
        <color>ff0000ff</color>
        <width>1.5</width>
      </LineStyle>
      <PolyStyle>
        <color>080000ff</color>
        <fill>1</fill>
        <outline>1</outline>
      </PolyStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="poly-FF0000-1000-8-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#poly-FF0000-1000-8-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#poly-FF0000-1000-8-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
  """
  return placemark_areas,estilo_areas

############### ESTILOS ###############################

def generar_style_id(color,modelo_icono):
  try:
    modelos={"lugar":"icon-1899","cel":"icon-1647","auto":"icon-1538","Antena":"icon-1895","moto":"icon-1754","auto_llave":"icon-1741","camara":"icon-1535","linea":"line-000000"}
    codigo_icono=modelos[modelo_icono]
    style_id=f"{codigo_icono}-{color}-labelson"
  except:
    style_id="icon-1899-0288D1-nodesc-normal"
  return style_id

def listar_estilos(tabla,headers):
  modelos=csv.extraer_columna(tabla,headers.index("modelo_icono"))
  colores=csv.extraer_columna(tabla,headers.index("color_icono"))
  style_ids=[]
  for modelo,color in zip(modelos,colores):
    style_id=generar_style_id(color,modelo)
    style_ids.append(style_id)
  return style_ids

def traducir_estilos(tabla,headers):
  estilos=listar_estilos(tabla,headers)
  #borro columna color
  pos_color=headers.index("color_icono")
  tabla=csv.del_col(tabla,pos_color)
  del headers[pos_color]

  #borro columna modelo
  pos_modelo=headers.index("modelo_icono")
  tabla=csv.del_col(tabla,pos_modelo)
  del headers[pos_modelo]

  #agrego la columna estilo
  tabla=csv.add_col(tabla,estilos)
  headers.append("Estilo")
  return tabla,headers

def crear_estilos(tabla,headers):
    estilos_kml=""
    icono_antenas="""
    <Style id="icon-1895-880E4F-nodesc-normal">
      <IconStyle>
        <color>ff4f0e88</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <Style id="icon-1895-880E4F-nodesc-highlight">
      <IconStyle>
        <color>ff4f0e88</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>
    <StyleMap id="icon-1895-880E4F-nodesc">
      <Pair>
        <key>normal</key>
        <styleUrl>#icon-1895-880E4F-nodesc-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#icon-1895-880E4F-nodesc-highlight</styleUrl>
      </Pair>
    </StyleMap>
    """
    id_icono="x"

    estilos=csv.extraer_columna(tabla,headers.index("Estilo"))
    estilos=list.desduplicar(estilos)
    for estilo in estilos:
      icono_cuerpo=f"""
    <Style id="{estilo}-normal">
      <IconStyle>
        <color>ff468442</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>0</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>

    <Style id="{estilo}-highlight">
      <IconStyle>
        <color>ff4f0e88</color>
        <scale>1</scale>
        <Icon>
          <href>https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <scale>1</scale>
      </LabelStyle>
      <BalloonStyle>
        <text><![CDATA[<h3>$[name]</h3>]]></text>
      </BalloonStyle>
    </Style>

    <StyleMap id="{estilo}">
      <Pair>
        <key>normal</key>
        <styleUrl>#{estilo}-normal</styleUrl>
      </Pair>
      <Pair>
        <key>highlight</key>
        <styleUrl>#{estilo}-highlight"</styleUrl>
      </Pair>
    </StyleMap>"""    
      estilos_kml=estilos_kml+icono_cuerpo
    return estilos_kml

###############   DISTRIBUCION DE PUNTOS ##########################

def distribuir_antenas(tabla,header):
  #extraccion de posiciones de columnas
  pos_lat=header.index("Latitud")
  pos_lon=header.index("Longitud")
  pos_azimuth=header.index("Azimuth")
  pos_radio=header.index("Radio Cobertura en KM o Metros")

  placemark_lineas=""#variable que va a contener la cadena de placemarks


  tabla=csv.concatenar(tabla,pos_lat,pos_lon)
  n=len(tabla[0])-1
  tablas=csv.estallar(tabla,n)
  for n,tabla in enumerate(tablas):#para cada tabla

    if tabla[0][pos_radio]=="":
      radio=float(1)
    else:
      radio=float(tabla[0][pos_radio])
    
    radio=0.1 ################# PROVISORIO #############################

    if tabla[0][pos_azimuth]=="":
      azimuth=0
      apertura=360
    else:
      azimuth=float(tabla[0][pos_azimuth])
      apertura=60

    angulo_inicio=(azimuth-apertura/2)
    angulo_base=(apertura/len(tabla))

    latitud=float(tabla[0][pos_lat])
    longitud=float(tabla[0][pos_lon])
    coordenadas=(latitud,longitud)

    antena=list.nueva(len(tabla[0]),"S/D")
    antena[pos_lat]=latitud
    antena[pos_lon]=longitud
    antena[header.index("color_icono")]="468442"
    antena[header.index("modelo_icono")]="Antena"
    antena[header.index("Folder")]=tabla[0][header.index("Folder")]
    antena[header.index("Name")]="Antena"
    antena[header.index("Dirección celda")]=tabla[0][header.index("Dirección celda")]
    antena[header.index("Azimuth")]=tabla[0][header.index("Azimuth")]
    antena[header.index("Radio Cobertura en KM o Metros")]=tabla[0][header.index("Radio Cobertura en KM o Metros")]

    for numero_linea,linea in enumerate(tabla):
      angulo=(angulo_inicio+(angulo_base*numero_linea))*pi/180
      coordenadas_nuevas=inverse_haversine(coordenadas,radio,angulo)
      lat_nueva=str(coordenadas_nuevas[0])
      lon_nueva=str(coordenadas_nuevas[1])
      linea[pos_lat]=lat_nueva
      linea[pos_lon]=lon_nueva
      
      fecha=linea[header.index("Fecha")]
      hora=linea[header.index("Hora")]
      if len(tabla)<10:
        placemark_lineas=placemark_lineas+crear_linea_placemark(coordenadas,coordenadas_nuevas,fecha,hora)
      else:
        continue
    tabla.append(antena)

  tabla=csv.unificar(tablas)
  tabla=csv.del_col(tabla,len(tabla[0])-1)

  return tabla,placemark_lineas

def distribuir_camaras(tabla,header):
  pos_lat=header.index("Latitud")
  pos_lon=header.index("Longitud")
  placemark_lineas=""
  #Concatenacion de lat y lon y separacion en tablas por fuente de captura
  tabla=csv.concatenar(tabla,pos_lat,pos_lon)
  n=len(tabla[0])-1
  tablas=csv.estallar(tabla,n)

  #generacion de distribucion para cada camara
  for tabla in tablas:#para cada tabla
    latitud=float(tabla[0][pos_lat])
    longitud=float(tabla[0][pos_lon])
    coordenadas=(latitud,longitud)
    punto_inicio=inverse_haversine(coordenadas, 0.05*len(tabla)/5,Direction.EAST)
    punto_inicio=inverse_haversine(punto_inicio, 0.01*len(tabla)/2,Direction.NORTH)

    camara=list.nueva(len(tabla[0]),"S/D")
    camara[pos_lat]=latitud
    camara[pos_lon]=longitud
    camara[header.index("color_icono")]="E16605"
    camara[header.index("modelo_icono")]="camara"
    camara[header.index("Folder")]=tabla[0][header.index("Folder")]
    camara[header.index("Name")]="Camara"

    count=0
    for numero_linea,linea in enumerate(tabla):
      if (numero_linea % 2) == 0:#si es par
        count=-count
      else:
        count=-count+1
      movimiento=0.01*numero_linea
      coordenadas_nuevas=inverse_haversine(punto_inicio, movimiento,Direction.SOUTH)
      lat_nueva=str(coordenadas_nuevas[0])
      lon_nueva=str(coordenadas_nuevas[1])
      linea[pos_lat]=lat_nueva
      linea[pos_lon]=lon_nueva
      placemark_lineas=placemark_lineas+crear_linea_placemark(coordenadas,coordenadas_nuevas)
    tabla.append(camara)

  #unificacion de los datos en una sola tabla y eliminacion de la concatenacion de lat y lon
  tabla=csv.unificar(tablas)
  tabla=csv.del_col(tabla,len(tabla[0])-1)
  return tabla,placemark_lineas