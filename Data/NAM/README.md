# Fast Download via inventory files

1. Specify variables and directories in `inv.json`. `url` defines if we download from `historical` or `forecast`.

2. To fast download each variable from each file run the example below:

We can run this in bash:

```bash
./get_inv.pl https://www.ncei.noaa.gov/data/north-american-mesoscale-model/access/forecast/202005/20200529/nam_218_20200529_0000_068.grb2.inv | grep ":TMP:750 mb:" | ./get_grib.pl https://www.ncei.noaa.gov/data/north-american-mesoscale-model/access/forecast/202005/20200529/nam_218_20200529_0000_068.grb2 nam_218_20200529_0000_068__TMP_750_mb_.grb2

```

3. To download all the variables and dates of interest run `get_all.py`.