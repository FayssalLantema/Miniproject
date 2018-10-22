import requests
import xmltodict
import time
from tkinter import *
import NS_Monteur_Monteurslijst as Monteurs
import NS_Monteur_Tkinter as Bot

mapquest_api_key = "6G3oGijGWO6n95FXytpvpeumV2vsog6m"
mapquest_api_geo_url = "http://www.mapquestapi.com/geocoding/v1/reverse?outFormat=xml&key=" + mapquest_api_key + "&location="
mapquest_api_route_url = "http://www.mapquestapi.com/directions/v2/route?outFormat=xml&key=" + mapquest_api_key + "&from="

ns_api_inlog = ("kevin.spelt@student.hu.nl", "srGdP4aL3qFdT7yebQ44N5jNPoUpi8TCaFgBOSTZ2fPl00C94xatBg")
ns_api_response = requests.get("http://webservices.ns.nl/ns-api-stations-v2",auth=ns_api_inlog)
ns_api_xml = xmltodict.parse(ns_api_response.text)
ns_api_stations = ns_api_xml["Stations"]["Station"]

def tijd(uur):
    if uur >= 18 and uur <= 24 or uur >= 0 and uur <= 8:
        return True
    return False

def clicked():

    defect_station = stationentry.get()
    avond = str(tijd(int(time.strftime("%H"))))
    code = codeentry.get()

    for x in range(0,len(ns_api_stations)):

        ns_api_namen = ns_api_stations[x]["Namen"]

        if ns_api_namen["Kort"] == defect_station or ns_api_namen["Middel"] == defect_station or ns_api_namen["Lang"] == defect_station:
            defect_station_lat = ns_api_stations[x]["Lat"]
            defect_station_lon = ns_api_stations[x]["Lon"]

            mapquest_api_geo_response = requests.get(mapquest_api_geo_url + defect_station_lat + "," + defect_station_lon)
            mapquest_api_geo_xml = xmltodict.parse(mapquest_api_geo_response.text)

            defect_station_xml_locatie = mapquest_api_geo_xml["response"]["results"]["result"]["locations"]["location"]

            defect_station_straat = defect_station_xml_locatie["street"]
            defect_station_stad = defect_station_xml_locatie["adminArea5"]["#text"]
            defect_station_provincie = defect_station_xml_locatie["adminArea3"]["#text"]

            defect_station_locatie = defect_station_straat + ", " + defect_station_stad + ", " + defect_station_provincie

    defect_tot_monteur_afstanden = list()
    defect_tot_monteur_dict = dict()

    for monteur in Monteurs.monteurs:
        mapquest_api_route_response = requests.get(mapquest_api_route_url + defect_station_locatie + "&to=" + monteur.adres)
        mapquest_api_route_xml = xmltodict.parse(mapquest_api_route_response.text)
        defect_tot_monteur_afstand = mapquest_api_route_xml["response"]["route"]["distance"]
        defect_tot_monteur_afstanden.append(float(defect_tot_monteur_afstand))
        defect_tot_monteur_dict[monteur] = float(defect_tot_monteur_afstand)

    defect_tot_monteur_afstanden.sort()

    for x in range(0, len(defect_tot_monteur_afstanden)):
        for y in defect_tot_monteur_dict:
            if defect_tot_monteur_dict[y] == defect_tot_monteur_afstanden[x] and avond == y.beschikbaar:
                geschikte_monteur_naam = y.vollenaam
                geschikte_monteur_afstand = defect_tot_monteur_afstanden[x]
                stationlabel["text"] = "De dichtstbijzijnde monteur is {}, hij is op {} kilometer afstand".format(geschikte_monteur_naam,geschikte_monteur_afstand)
                Bot.send_message(y.chat_id, "Hallo, {} \nJe wordt verwacht op treinstation {}, om de kaartjesmachine "
                                            "met code {} te repareren, de afstand tot het treinstation is {} km\n{}, {}, {}".format(geschikte_monteur_naam,
                                                                                                                                    stationentry.get(),
                                                                                                                                    code,
                                                                                                                                    geschikte_monteur_afstand,
                                                                                                                                    defect_station_straat,
                                                                                                                                    defect_station_stad,
                                                                                                                                    defect_station_provincie))
                return


root = Tk()

root.configure(background="#FCC63F")
root.title("Wachtdienst NS")

textlabel = Label(master=root,
                 text='Op welk station is er een defect?',
                 font=('Calibri',20),
                 background="#FCC63F")

codelabel = Label(master=root,
                  text="Wat is de code van de kapotte kaartjesautomaat?",
                  font=("Calibri",20),
                  background="#FCC63F")

stationlabel = Label(master=root,
                     text="",
                     font=('Calibri',20),
                     background="#FCC63F")

stationentry = Entry(master=root)
codeentry = Entry(master=root)
button = Button(master=root, text="Bevestigen", command=clicked)


textlabel.pack()
stationentry.pack()
codelabel.pack()
codeentry.pack()
button.pack(pady=10)
stationlabel.pack()


root.mainloop()