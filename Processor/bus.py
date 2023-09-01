import pandas as pd
import numpy as np

class Bus:
    def get_buses_data(self, data, bus_number:str):
        bus_data = data[(data['mDescription'] == bus_number) & (data['p_total'] != 'N')] 
        array_of_passengers = pd.DataFrame(bus_data.loc[:, ['regId', 'mDescription', 'p_doorId', 'p_ingresos', 'p_salidas', 'p_bloqueos', 'p_station', 'gps_datetime']]).to_numpy()
        
        return array_of_passengers


    def get_passengers(self, passengers_list:list, travels_range_time:list):
        last_date = ''
        passengers = {}
        metro = ["049 - Metro", "051 - Metro", "052 - Metro", "057 - Metro", "058", "059", "064", "067 - Metro", "62 Metro"]
        black_stations = ["Terminal Arrieritas", "Terminal arrieritas", "Respaldo"]


        for i in passengers_list:
            date = str(i[7][0:10])
            is_range = False
            time = i[7][11:19].replace(':', '')

            for range_time in travels_range_time:
                if (time >= range_time[0]) and (time <= range_time[1]):
                    is_range = True

            if date != last_date:
                passengers[date] = {"bus": i[1], "p1": 0, "p2": 0, "debe": 0, "novedades": [], "descuento": 0}
                        

            if i[2] == 1 and ((i[6] != "Terminal Arrieritas") and (i[6] != "Terminal arrieritas") and (i[6] != "Respaldo")):
                    passengers[date]["p1"] += i[3]


            if i[2] == 2:
                if (i[6] in black_stations) or ((i[5] > 19) or (i[4] > 24) or (i[3] > 8)):
                    passengers[date]["descuento"] += i[3]
                    continue

                if (i[3] > 4) or (i[5] > 4 and i[3] > 0) or ((i[4] > 1) and (i[3] > 0)) or not(is_range):
                    passengers[date]["novedades"].append({"p2": i[3], "bloqueos": i[5],"salidas": i[4], "fecha": i[7], "lugar": i[6]})
                            

                if  (i[5] < 20 and i[4] < 25) and (i[6] not in black_stations) and (i[3] < 9):
                    passengers[date]["p2"] += i[3]
                        
            last_date = str(i[7][0:10])


        for value in passengers.values():
            if value["bus"] in metro:
                if value["p1"] >= 300 and value["p2"] > 20:
                    value["debe"] = value["p2"] - 20
                if value["p1"] <= 299 and value["p2"] > 10:
                    value["debe"] = value["p2"] - 10
            else:
                if value["p1"] >= 250 and value["p2"] > 20:
                    value["debe"] = value["p2"] - 20
                if value["p1"] <= 249 and value["p2"] > 10:
                    value["debe"] = value["p2"] - 10
            

        return passengers
    

    def get_driver_data(self, drivers_data, bus_number):
        driver_data = drivers_data [(drivers_data['Vehículo'] == bus_number)]
        array_of_driver = pd.DataFrame(driver_data.loc[:, ["Vehículo", 'Fecha de Inicio', 'Conductor']]).to_numpy()
        return array_of_driver
    
    def get_driver_name(self, names_list: list):
        drivers = {}
        last_date = ''

        for i in names_list:
            date = str(i[1])[0:10]

            if date == 'nan':
                continue

            if date != last_date:
                drivers[date] = {"conductor": []}
            
            drivers[date]["conductor"].append(i[2])

            last_date = str(i[1])[0:10]

        for value in drivers.values():
            drivers_count = []
            for i in np.unique(value["conductor"]):
                drivers_count.append([i, value["conductor"].count(i)])

            last_value = {"count": 0, "name": ""}    
            for i in drivers_count:
                if last_value["count"] < i[1]:
                    value["conductor"] = i[0]
                    last_value["count"] = i[1]
                    last_value["name"] = i[0]
                else:
                    value["conductor"] = last_value["name"]

        return drivers
    

    def get_travels_data(self, data, bus_number:str):
        bus_data = data[(data['Vehículo'] == bus_number)]    
        travels_data = pd.DataFrame(bus_data.loc[:, ['Vehículo', 'Itinerario', 'Conductor', 'Fecha de Inicio', 'Fecha de Finalización', 'Tiempo de viaje(minutos)', 'Despachador']]).to_numpy()
        
        return travels_data
    
    def get_number_of_travels(self, travels_data:list):
        last_date = ''
        last_terminal = ''
        travel_number = 0
        travels = {}
        travels_range_time = []
        metro = ["049 - Metro", "051 - Metro", "052 - Metro", "057 - Metro", "058", "059", "064", "067 - Metro", "62 Metro"]
        minorista = ["Minorista - La 50", "Minorista - Variante", "Minorista - Tablaza Variante"]
        caldas = [ "Caldas - Medellin - Tablaza Variante", "Caldas - Medellin - Variante", "Caldas - Medellín - La 50", "Variante Miel Metro", "Variante tablaza Metro", "Metro La 50", "Circular"]
        medellin = [ "Variante Miel Caldas", "Variante Tablaza Caldas", "Medellin - Caldas" ]

        despacho_caldas = {"mañana": False, 'tarde': False}
        despacho_medellin = {"mañana": False, 'tarde': False}

        for travel in reversed(travels_data):
            jornada = "mañana" if int(travel[4][11:13]) < 12 else "tarde"
            if (travel[1] in caldas) or (travel[1] in minorista):
                despacho_caldas[jornada] = travel[6] if not despacho_caldas[jornada] else despacho_caldas[jornada]
            elif travel[1] in medellin:
                despacho_medellin[jornada] = travel[6] if not despacho_medellin[jornada] else despacho_medellin[jornada]

        for travel in reversed(travels_data):
            travels_range_time.append([travel[3][11:19].replace(':', ''), travel[4][11:19].replace(':', '')])
            date = str(travel[3])[0:10]
            current_terminal = 'Caldas' if travel[1] in caldas else 'Medellin'

            def filterTravels(x):
                if (str(x[3])[0:10] == date) and (not(x[1] in medellin)) and (x[5] > 30):
                    return True
                else:
                    return False
                

            if date != last_date:
                filtered = list(filter(filterTravels, travels_data))
                travel_number = len(filtered)

                travels[date] = {
                    "ida": 
                    { "c": 0, "vm": 0, "vt": 0, "m": 0, "cr": 0, "total": 0}, 
                    "vuelta": 
                    {"c": 0, "vm": 0, "vt": 0, "m": 0, "cr": 0, "total": 0},
                    "novedades": [],
                    "despachos": [],
                    "metro": False
                }
                last_terminal = ''
                

            jornada_despachador = "mañana" if int(travel[4][11:13]) < 12 else "tarde"

            if (last_terminal == '') and (travel[1] in caldas) and (not(travel[0] in metro)) and (travel[5] > 30) and (not(travel[1] in minorista)):
                jornada = "Mañana" if int(travel[4][11:13]) < 12 else "Tarde"
                travels[date]["despachos"].append({
                        "terminal": "Medellin",
                        "jornada": jornada,
                        "despachador": 'Desconocido' if not despacho_medellin[jornada_despachador] else despacho_medellin[jornada_despachador],
                        "empresa": "Arrieritas" if jornada == "Mañana" else "Mocatan",
                        "despachos": f'\nBUS {travel[0]}. no genero despacho en el {travel_number} viaje {travel[4][11:16]}'
                })

                travels[date]["novedades"].insert(0, f'BUS {travel[0]}. no genero despacho en el {travel_number} viaje {travel[4][11:16]}')


            if (last_terminal == current_terminal) and (not(travel[1] in minorista)) and (not(travel[0] in metro)) and (travel[5] > 30):

                if last_terminal == 'Caldas':
                    jornada = "Mañana" if int(travel[4][11:13]) < 12 else "Tarde"
                    travels[date]["despachos"].append({
                        "terminal": "Medellin",
                        "jornada": jornada,
                        "despachador": 'Desconocido' if not despacho_medellin[jornada_despachador] else despacho_medellin[jornada_despachador],
                        "empresa": "Arrieritas" if jornada == "Mañana" else "Mocatan",
                        "despachos": f'\nBUS {travel[0]}. no genero despacho en el {travel_number} viaje {travel[4][11:16]}'
                    })

                    travels[date]["novedades"].insert(0, f'BUS {travel[0]}. no genero despacho en el {travel_number} viaje {travel[4][11:16]}')
                    

                
                if last_terminal == 'Medellin':
                    jornada = "Mañana" if int(travel[4][11:13]) < 12 else "Tarde"
                    travels[date]["despachos"].append({
                        "terminal": "Terminal",
                        "jornada": jornada,
                        "despachador": 'Desconocido' if not despacho_caldas[jornada_despachador] else despacho_caldas[jornada_despachador],
                        "empresa": "Arrieritas",
                        "despachos": f'\nBUS {travel[0]}. no genero despacho en el {travel_number} viaje {travel[4][11:16]}'
                    })

                    travels[date]["novedades"].insert(0, f'BUS {travel[0]}. no genero despacho en el {travel_number} viaje {travel[4][11:16]}')
                    

            if travel[5] > 30:
                last_terminal = 'Medellin' if (travel[1] in medellin) else 'Caldas'
            


            if (travel[1] in caldas) or (travel[1] in minorista):
                travel_number -= 1
                print(travel_number)

                if ('Metro' in travel[1]) or (travel[1] == 'Circular'):
                    travels[date]["metro"] = True
                    if travel[1] == 'Variante Miel Metro' and (travel[5] > 40):
                        travels[date]["ida"]["vm"] += 1
                        travels[date]["ida"]["total"] += 1
                    if travel[1] == 'Variante tablaza Metro' and (travel[5] > 40):
                        travels[date]["ida"]["vt"] += 1
                        travels[date]["ida"]["total"] += 1
                    if travel[1] == 'Metro La 50' and (travel[5] > 40):
                        travels[date]["ida"]["c"] += 1
                        travels[date]["ida"]["total"] += 1
                    if travel[1] == 'Circular' and (travel[5] > 40):
                        travels[date]["ida"]["cr"] += 1
                        travels[date]["ida"]["total"] += 1
                    
                if travel[1] == 'Caldas - Medellin - Tablaza Variante' and (travel[5] > 40):
                    travels[date]["ida"]["vt"] += 1
                    travels[date]["ida"]["total"] += 1
                if travel[1] == 'Caldas - Medellin - Variante' and (travel[5] > 40):
                    travels[date]["ida"]["vm"] += 1
                    travels[date]["ida"]["total"] += 1
                if travel[1] == 'Caldas - Medellín - La 50' and (travel[5] > 40):
                    travels[date]["ida"]["c"] += 1
                    travels[date]["ida"]["total"] += 1
                if ((travel[1] == 'Minorista - La 50') or (travel[1] == 'Minorista - Variante') or (travel[1] == 'Minorista - Tablaza Variante')) and (travel[5] > 40):
                    travels[date]["ida"]["m"] += 1
                    travels[date]["vuelta"]["m"] += 1
                    travels[date]["ida"]["total"] += 1
                    travels[date]["vuelta"]["total"] += 1
                    
                

            if travel[1] in medellin:
                if travel[1] == 'Variante Miel Caldas' and (travel[5] > 40):
                    travels[date]["vuelta"]["vm"] += 1
                    travels[date]["vuelta"]["total"] += 1
                if travel[1] == 'Variante Tablaza Caldas' and (travel[5] > 40):
                    travels[date]["vuelta"]["vt"] += 1
                    travels[date]["vuelta"]["total"] += 1
                if travel[1] == 'Medellin - Caldas' and (travel[5] > 40):
                    travels[date]["vuelta"]["c"] += 1
                    travels[date]["vuelta"]["total"] += 1

            last_date = str(travel[3])[0:10]
        

        for key in travels.keys():
            if not travels[key]["metro"]:
                if travels[key]["ida"]["total"] == travels[key]["vuelta"]["total"]:
                    travels[key]["despachos"] = False

        
        return travels, travels_range_time