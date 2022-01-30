# Create a TensorFlow dataset

```bash
alias create-tf-dataset='python3 create_tf_dataset.py'
conda activate fog
create-tf-dataset --startdate 20200601 --enddate 20200601 --basetime-hour 0 --progs 0 --outdir NAM/tfrecords/
```