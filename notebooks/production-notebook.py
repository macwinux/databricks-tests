# Databricks notebook source
# get data path from the DLT Pipeline configuration so we can test the pipeline with smaller amount of data

default_json_path = "/databricks-datasets/wikipedia-datasets/data-001/clickstream/raw-uncompressed-json/"
json_path = spark.conf.get("my_etl.data_path", default_json_path)
print(f"Loading data from {json_path}")

# COMMAND ----------

import sys
import os
sys.path.append(os.path.abspath('/Workspace/Repos/Production/databricks-tests'))
# import helper functions from the current repository
import dlt_test.column_helpers as ch

# COMMAND ----------

df = spark.read.format("json").load(json_path)
new_cols = ch.columns_except(df, ['prev_id', 'prev_title'])

# COMMAND ----------

df.where("type is not null and type in ('link', 'redlink')").select(*new_cols).createOrReplaceGlobalTempView("clickstream_filtered")

# COMMAND ----------

#display(spark.sql("SELECT COUNT(*) FROM global_temp.clickstream_filtered"))
