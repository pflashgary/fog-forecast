# Pull ERA5 via public CDS API

- To get your API key go to https://cds.climate.copernicus.eu/api-how-to
- Browse into the product you want, you can either use the UI and select `Show API request`. There is a trick as it doesn't let you copy the script and you don't want to type it. Ctrl+U and search for "copy not ok" and remove it from the source. This step is only required if we need to download more variables.

# Install eccodes and other python packages; More details [here](https://confluence.ecmwf.int/display/ECC/ecCodes+installation):
1. Get the latest version from https://confluence.ecmwf.int/display/ECC
2. Run this on your terminal

```bash
tar -xzf  eccodes-2.24.1-Source.tar.gz  # Change the version accordingly
mkdir build ; cd build

cmake  ../eccodes-2.24.1-Source

make
ctest
sudo make install
```

3. Install some dependencies for Cartopy

```bash
sudo apt-get install libproj-dev proj-data proj-bin
sudo apt-get install libgeos-dev
```

4. Install the python packages

```bash
conda create -n fog -c conda-forge python=3.8 cartopy eccodes cfgrib xarray[complete]
conda activate fog
```
