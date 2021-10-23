import gpxpy.gpx
import json
from geopy.distance import geodesic

#EL JSON GUARDA MUCHOS DATOS, LOS QUE NECESITABAMOS EN SI SON:
#1) DistanciaKmTotalRecorridaHastaEstePunto (seria nuestro X de km)
#2) DesnivelPuntoActualConAnterior (si es negativo bajo, si es positivo subio). (seria nuestro Y de altura "desnivel")




def buildRoute():
    item = {"totalRecorrido": distanciaTotal}
    item["DesnivelAcumuladoTotal"] = desnivelTotalActualPositivo - desnivelTotalActualNegativo
    item["DesnivelAcumuladoTotalNegativo"] = desnivelTotalActualNegativo
    item["DesnivelAcumuladoTotalPositivo"] = desnivelTotalActualPositivo
    return item


def buildJson(puntos):
    total = {}
    total = buildRoute()
    # construimos el json final
    jsonFinal = {"Ruta": total, "Puntos": puntos}
    jsonData = json.dumps(jsonFinal)
    # Construimos el archivo.json
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonData)
    jsonFile.close()

#recorremos los registros del ruta.gpx
def buildPunto():
    item = {}
    item["id"] = idJson
    item["latitudAnterior"] = latitudAnterior
    item["longitudAnterior"] = longitudAnterior
    item["latitudActual"] = point.latitude
    item["longitudActual"] = point.longitude
    item["elevacionAnterior"] = elevationAnterior
    item["elevacionActual"] = point.elevation
    item["distanciaKmEntrePuntos"] = distanciaActual
    item["distanciaTotalRecorridaHastaEstePunto"] = distanciaTotal
    item["desnivelPuntoActualConAnterior"] = elevacionDiferencia
    item["desnivelTotalActualNegativo"] = desnivelTotalActualNegativo
    item["desnivelTotalActualPositivo"] = desnivelTotalActualPositivo
    return item



#AQUI EMPIEZA EL CODIGO LOGICAMENTE

#leemos el archivo con el nombre ruta.gpx.

gpx_file = open('files/ruta.gpx', 'r')

#lo parseamos.

gpx = gpxpy.parse(gpx_file)


for track in gpx.tracks:
    latitudAnterior = 0
    longitudAnterior = 0
    elevationAnterior = 0
    distanciaTotal = 0
    desnivelTotalActualNegativo = 0
    desnivelTotalActualPositivo = 0
    idJson = 1
    puntos = []
    for segment in track.segments:
        for point in segment.points:
            if latitudAnterior != 0:
                origen = (latitudAnterior, longitudAnterior)
                destino = (point.latitude, point.longitude)
                distanciaActual = geodesic(origen, destino).kilometers
                distanciaTotal = distanciaTotal + distanciaActual
                if elevationAnterior > point.elevation: #significa que bajo
                    elevacionDiferencia = point.elevation - elevationAnterior
                    desnivelTotalActualNegativo = elevacionDiferencia + desnivelTotalActualNegativo
                else: #significa que subio
                    elevacionDiferencia = elevacionDiferencia + point.elevation
                    desnivelTotalActualPositivo = elevacionDiferencia + desnivelTotalActualPositivo
                #construimos el array para el json de Puntos
                item = buildPunto()
                puntos.append(item)
                idJson = idJson + 1
            #Guardamos las variables para el siguiente punto.
            latitudAnterior = point.latitude
            longitudAnterior = point.longitude
            elevationAnterior = point.elevation
        buildJson(puntos)






