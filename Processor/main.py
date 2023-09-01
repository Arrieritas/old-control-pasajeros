from Processor.bus import Bus

def generate_passengers_control(data):
    buses_dic = {}
    despachos = {}
    new_bus = Bus()

    if not(data["passengers"]["status"]) or not(data["itineraries"]["status"]):
        print("Missing files :(")
        return

    for i in data["buses_list"]:
        bus_data = new_bus.get_buses_data(data["passengers"]["data"], i)
        travels_data = new_bus.get_travels_data(data["itineraries"]["data"], i)
        drivers_data = new_bus.get_driver_data(data["itineraries"]["data"], i)
        bus_dict = {}

        travels, travels_range_time = new_bus.get_number_of_travels(travels_data)
        passengers = new_bus.get_passengers(bus_data, travels_range_time)
        drivers = new_bus.get_driver_name(drivers_data)

        for key, value in drivers.items():
            template = {
                "bus": str(i),
                "p1": False if key not in passengers else passengers[key]["p1"], 
                "p2": False if key not in passengers else passengers[key]["p2"],
                "debe": False if key not in passengers else passengers[key]["debe"], 
                "novedades": False if key not in passengers else passengers[key]["novedades"], 
                "descuento": False if key not in passengers else passengers[key]["descuento"],
                "viajes": False if key not in travels else travels[key],
                "conductor": value["conductor"]
            }
            bus_dict[key] = template
        
        for key, v in travels.items():
            if not v["despachos"]:
                continue

            for value in v["despachos"]:
                if not value:
                    continue

                if despachos.get(f'{key}-{value["terminal"]}-{value["jornada"]}'):
                    jornada = despachos[f'{key}-{value["terminal"]}-{value["jornada"]}']["jornada"]
                    terminal = despachos[f'{key}-{value["terminal"]}-{value["jornada"]}']["terminal"]

                    if ((jornada != value["jornada"]) and (terminal != value["terminal"])):
                        despachos[f'{key}-{value["terminal"]}-{value["jornada"]}'] = {
                        "terminal": value["terminal"],
                        "jornada": value["jornada"],
                        "despachador": value["despachador"],
                        "empresa": value["empresa"],
                        "despachos": value["despachos"]
                        }
                    else:
                        despachos[f'{key}-{value["terminal"]}-{value["jornada"]}']["despachos"] += value["despachos"]
                else:
                    despachos[f'{key}-{value["terminal"]}-{value["jornada"]}'] = {
                        "terminal": value["terminal"],
                        "jornada": value["jornada"],
                        "despachador": value["despachador"],
                        "empresa": value["empresa"],
                        "despachos": value["despachos"]
                    }



        buses_dic[str(i)] = bus_dict

    return buses_dic, despachos





def generate_despachos(terminal, jornada, despachador, empresa, despachos):
    if (despachador == 'Carlos Correa '):
        return {
            "terminal": terminal,
            "jornada": jornada,
            "despachador": despachador,
            "empresa": empresa,
            "despachos": despachador
        }