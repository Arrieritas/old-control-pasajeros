def generate_excel_list (dict:dict):
    excel_list = [
        ['VEHICULO', 'P1', 'P2', 'DESCUENTO', 'FECHA', 'CONDUCTOR', 'TOTAL_IDA', 'TOTAL_VUELTA', 'CR', 'IDA_VM', 'IDA_VT', 'IDA_C', 'IDA_M', 'VUELTA_VM', 'VUELTA_VT', 'VUELTA_C', 'VUELTA_M']
    ]


    for key, value in dict.items():
        for k, v in value.items():
            excel_list.append([
                v["bus"],
                v["p1"], 
                v["p2"],
                v["descuento"], 
                k,
                v["conductor"], 
                v["viajes"]["ida"]["total"],
                v["viajes"]["vuelta"]["total"],
                v["viajes"]["ida"]["cr"],
                v["viajes"]["ida"]["vm"],
                v["viajes"]["ida"]["vt"],
                v["viajes"]["ida"]["c"],
                v["viajes"]["ida"]["m"],
                v["viajes"]["vuelta"]["vm"],
                v["viajes"]["vuelta"]["vt"],
                v["viajes"]["vuelta"]["c"],
                v["viajes"]["vuelta"]["m"]
                ])

    return excel_list

def generate_despachos_list(dict):
    excel_list = [["FECHA", "TERMINAL", "JORNADA", "DESPACHADOR", "EMPRESA", "DESPACHOS"]]

    for key, value in dict.items():
        excel_list.append([
            key,
            value["terminal"],
            value["jornada"],
            value["despachador"],
            value["empresa"],
            value["despachos"]
        ])
    
    return excel_list