import json

import gpxpy.gpx

import json
import mpu
from geopy.distance import geodesic

#EL JSON GUARDA MUCHOS DATOS, LOS QUE NECESITABAMOS EN SI SON:
#1) DistanciaKmTotalRecorridaHastaEstePunto (seria nuestro X de km)
#2) DesnivelPuntoActualConAnterior (si es negativo bajo, si es positivo subio). (seria nuestro Y de altura "desnivel")
#3) El desnivelAcumuladoTotal = desnivelTotalActualPositivo - desnivelActualNegativo  DEL ULTIMO

#leemos el archivo.
gpx_file = open('files/ruta.gpx', 'r')

#lo parseamos.

gpx = gpxpy.parse(gpx_file)


#recorremos los registros del ruta.gpx
for track in gpx.tracks:
    latitudAnterior = 0
    longitudAnterior = 0
    elevationAnterior = 0
    distanciaTotal = 0
    desnivelTotalActualNegativo = 0
    desnivelTotalActualPositivo = 0
    idJson = 1
    data = []
    for segment in track.segments:
        for point in segment.points:
            #print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
            if latitudAnterior != 0:
                #print("Elevacion Anterior: " + str(elevationAnterior))
                #print("Elevacion Actual: " + str(point.elevation))
                origen = (latitudAnterior, longitudAnterior)
                destino = (point.latitude, point.longitude)
                distanciaActual = geodesic(origen, destino).kilometers
                distanciaTotal = distanciaTotal + distanciaActual
                #print("Distancia en KM entre 2 Puntos: "+str(distanciaActual)+" Kilometros")
                #desnivelCalculado = sqrt(distanciaActual ** 2 + point.elevation ** 2)  # hipotenusa
                if elevationAnterior > point.elevation: #significa que bajo
                    #print("BAJO:")
                    elevacionDiferencia = point.elevation - elevationAnterior
                    desnivelTotalActualNegativo = elevacionDiferencia + desnivelTotalActualNegativo
                else: #significa que subio
                    #print("SUBIO")
                    elevacionDiferencia = elevacionDiferencia + point.elevation
                    desnivelTotalActualPositivo = elevacionDiferencia + desnivelTotalActualPositivo
                #print("Desnivel entre el punto actual y el anterior: "+str(elevacionDiferencia) +" metros")
                #print("Desnivel Negativo Total: " + str(desnivelTotalActualNegativo) +" metros")
                #print("Desnivel Positivo Total: " + str(desnivelTotalActualPositivo) +" metros")
                #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                #construimos el json
                item = {"id": idJson}
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
                data.append(item)
                jsonData = json.dumps(data)
                idJson = idJson + 1
            latitudAnterior = point.latitude
            longitudAnterior = point.longitude
            elevationAnterior = point.elevation
        print("Distancia Total de la Ruta: "+str(distanciaTotal) +" Kilometros")
        print(jsonData)
        item = {"totalRecorrido": distanciaTotal}
        item["DesnivelAcumuladoTotal"] = desnivelTotalActualPositivo - desnivelTotalActualNegativo
        item["DesnivelAcumuladoTotalNegativo"] = desnivelTotalActualNegativo
        item["DesnivelAcumuladoTotalPositivo"] = desnivelTotalActualPositivo
        data.append(item)
        jsonData = json.dumps(data)
        #Construimos el archivo.json
        jsonFile = open("data.json", "w")
        jsonFile.write(jsonData)
        jsonFile.close()






