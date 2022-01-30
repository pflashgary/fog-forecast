# Create a TensorFlow dataset

```bash
alias create-tf-dataset='python3 create_tf_dataset.py'
conda create -n fog -c conda-forge python=3.8 cartopy eccodes cfgrib xarray[complete]
conda activate fog
create-tf-dataset --startdate 20200601 --enddate 20200601 --basetime-hour 0 --progs 0 --outdir NAM/tfrecords/
```