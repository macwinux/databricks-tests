# Databricks notebook source
# Databricks notebook source
# MAGIC %pip install -U nutter chispa

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

# COMMAND ----------

from runtime.nutterfixture import NutterFixture, tag

class TestFixtureExceptNotebook(NutterFixture):
  def run_test_count(self):
      dbutils.notebook.run('../../notebooks/production-notebook', 600)

  def assertion_test_count(self):
      df = sqlContext.sql('SELECT COUNT(*) FROM global_temp.clickstream_filtered')
      first_row = df.first()
      assert (first_row[0] == 12480649)

# COMMAND ----------

result = TestFixtureExceptNotebook().execute_tests()
print(result.to_string())
is_job = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().isDefined()
if is_job:
  result.exit(dbutils)
