from tkinter import filedialog as fd
import pandas as pd
import numpy as np

rutes = []

def select_file(rute_type:str):

    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes)
    
    rutes.append({"filename": filename, "rute_type": rute_type})
    
    return {"filename": filename, "rute_type": rute_type}


def get_data():

    data_dict = {
        "buses_list": None,
        "passengers": {"data": None, "status": False},
        "itineraries": {"data": None, "status": False}
    }

    for rute in rutes:
        if rute["rute_type"] == "passengers":
            data_dict["passengers"] = {
                "data": pd.read_csv(rute["filename"], encoding="utf_16", sep='\t', engine='python'),
                "status": True
            }
            data_dict["buses_list"] = np.unique(
                pd.DataFrame(data_dict["passengers"]["data"].loc[:, "mDescription"]).to_numpy().flatten()
            )
            continue
        if rute["rute_type"] == "itineraries":
            data_dict["itineraries"] = {
                "data": pd.read_csv(rute["filename"], encoding="utf_16", sep='\t', engine='python', index_col=False),
                "status": True
            }
            continue

    return data_dict