'''
mc mb minio/customer-data-parq
mc ls minio/customer-data-parq
'''

import dask.dataframe as dd

store_opt = {
    "client_kwargs": {
        "endpoint_url": "http://127.0.0.1:9000"
    }
}

file_csv = 's3://customer-data-text/customer.csv'
file_parq = 's3://customer-data-parq/customer.parq'
file_parq2 = 's3://customer-data-parq2/'

df = dd.read_csv(file_csv, storage_options=store_opt)
print(df.compute())

# df.to_parquet(file_parq, engine='pyarrow',
#               storage_options=store_opt)

df2 = dd.read_parquet(file_parq, storage_options=store_opt)
print(df2.compute())

df3 = dd.read_parquet(file_parq2, storage_options=store_opt)
print(df3.compute())
