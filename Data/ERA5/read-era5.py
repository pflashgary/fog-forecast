import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np
import cartopy

path = "gribs/"  # Change this to where your data is stored
year = "2022"
variable = "10m_u_component_of_wind"
fname = f"{variable}-{year}-single.grib"
lonmin = 165
lonmax = 180
latmin = -48
latmax = -33

ds=xr.open_dataset(path+fname,engine='cfgrib',backend_kwargs={'indexpath': ''})

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(resolution="10m")
ax.set_extent([165, 180, -48, -33], crs=ccrs.PlateCarree())
plot = ds.u10[0].plot(
    cmap=plt.cm.coolwarm, cbar_kwargs={"shrink": 0.6}
)

xticks = np.linspace(lonmin, lonmax, 5)
yticks = np.linspace(latmin, latmax, 5)

ax.set_xticks(xticks, crs=cartopy.crs.PlateCarree())
ax.set_yticks(yticks, crs=cartopy.crs.PlateCarree())

lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()

ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

plt.title("ERA5 - 10m U component of wind, New Zealand")
plt.savefig(f"{variable}-{year}-single.png")