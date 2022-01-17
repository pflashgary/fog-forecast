import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np
import cartopy

path = "gribs/"  # Change this to where your data is stored
fname = f"nam_218_20200601_0000_000_TMP_2_m_above_ground.grb2"

ds=xr.open_dataset(path+fname,engine='cfgrib',backend_kwargs={'indexpath': ''})

fig = plt.figure(figsize=(10, 10))
plot = ds.t2m.plot(
    cmap=plt.cm.coolwarm, cbar_kwargs={"shrink": 0.6}
)

plt.title("NAM t2m")
plt.savefig(f"{fname}-single.png")