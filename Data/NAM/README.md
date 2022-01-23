# Fast Download via inventory files

1. Specify variables and directories in `inv.json`. `url` defines if we download from `historical` or `forecast`.

2. To fast download each variable from each file run the example below:

We can run this in bash:

```bash
./get_inv.pl https://www.ncei.noaa.gov/data/north-american-mesoscale-model/access/forecast/202006/20200601/nam_218_20200601_0000_000.grb2.inv | grep ":TMP:2 m above ground:" | ./get_grib.pl https://www.ncei.noaa.gov/data/north-american-mesoscale-model/access/forecast/202006/20200601/nam_218_20200601_0000_000.grb2 gribs/nam_218_20200601_0000_000_TMP_2_m_above_ground.grb2

```

3. To download all the variables and dates of interest run `get_all.py`.