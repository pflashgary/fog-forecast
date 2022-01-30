# Install eccodes and other python dependencies; More details [here](https://confluence.ecmwf.int/display/ECC/ecCodes+installation):
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

4. Install python dependencies
```bash
conda create -n fog -c conda-forge python=3.9 cartopy eccodes cfgrib xarray[complete] apache_beam
conda activate fog
```
