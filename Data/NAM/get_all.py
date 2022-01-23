import json
import os
from NAM import VARIABLES

TO_REPLACE = {":": "_", " ": "_", "_.": "."}


def filename(str1):
    for key, value in TO_REPLACE.items():
        str1 = str1.replace(key, value)
    return str1


with open("inv.json", "r") as f:
    inv = json.load(f)

for key in list(inv.keys()):
    url = inv[key]["url"]
    dirs = inv[key]["dirs"]
    vars = inv[key]["vars"]
    for dir in dirs:
        for var in vars:
            for day in range(1, 32):
                for prog in range(0, 85):
                    subdir = f"{dir}{day:02d}"
                    source_inv = f"{url}/{dir}/{subdir}/nam_218_{subdir}_0000_{prog:03d}.grb2.inv"
                    source_grib = (
                        f"{url}/{dir}/{subdir}/nam_218_{subdir}_0000_{prog:03d}.grb2"
                    )
                    dest_grib = filename(
                        f"gribs/nam_218_{subdir}_0000_{prog:03d}{var}.grb2"
                    )
                    command = f'./get_inv.pl {source_inv} | grep "{var}" | ./get_grib.pl {source_grib} {dest_grib}'
                    os.system(command)
