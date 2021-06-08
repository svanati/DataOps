# -*- coding: utf-8 -*-
"""Pipeline import process

This module will ingest the data from the supplied table(s) in the
configuration file(s)

Author:
    Elvin Ellis Smith Jr

Example:
    $ python PipelineImport.py

To-do:
    * NA

Changelog:
    * 2021-05-01: Initial release

License:
    MIT <https://mit-license.org/>
"""
import json
from datetime import date

from faker import Factory
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from PipelineLogger.PipelineLogger import PipelineLogger


class PipelineImport:
    """This class will parse various configuration file(s)."""

    def __init__(self, pipeline_env):
        """
        Class initialization

        Args:
        :type pipeline_env: object
        """
        self.env_config = "configs/pipeline-env-{}.json".format(
            pipeline_env)
        self.tbl_config = "configs/pipeline-tbl-{}.json".format(
            pipeline_env)
        self.pipeline_env = pipeline_env

    def pipeline_import(self):
        """Database pipeline connection - IMPORT."""

        # Initialize data masking (faker) object
        fake = Factory.create()

        # Create logging instance
        pipeline_log_file = './logs/pipeline.log'
        pl_log = PipelineLogger()

        try:
            # Load JSON configuration file(s)
            with open(self.env_config.lower(), 'r') as json_env_file:
                json_env_config = json.load(json_env_file)

            with open(self.tbl_config.lower(), 'r') as json_tbl_file:
                json_tbl_config = json.load(json_tbl_file)

            # Database JSON configuration information
            database = str(json_env_config['db-source'][0]['database'])
            hostname = str(json_env_config['db-source'][0]['hostname'])
            port = str(json_env_config['db-source'][0]['port'])
            url = str(json_env_config['db-source'][0]['url'])
            driver = str(json_env_config['db-source'][0]['driver'])
            username = str(json_env_config['db-source'][0]['username'])
            password = str(json_env_config['db-source'][0]['password'])

            jdbc_url = "{0}://{1}:{2}/{3}".format(url, hostname, port,
                                                  database)

            # Spark ini information
            spark_master = str(json_env_config['spark'][0]['master'])

            if len(json_tbl_config['table']) > 0:
                for tbl in json_tbl_config['table']:

                    # Build the final query
                    query = 'SELECT * FROM {0}.{1}'.format(database, tbl)

                    # Determine if the table is incremental based
                    incremental_sql = str(
                        json_tbl_config['table'][tbl][2]['incremental_sql'])

                    if len(incremental_sql) > 0:
                        query = "{0} {1}".format(query, incremental_sql)

                    # Create a Spark Session Object
                    spark = SparkSession \
                        .builder \
                        .appName("Pipeline - SQL") \
                        .master(spark_master) \
                        .config("spark.driver.extraClassPath", "./jars/*") \
                        .config("spark.executor.extraClassPath", "./jars/*") \
                        .config("spark.logConf", "true") \
                        .getOrCreate()

                    spark.conf.set("spark.default.parallelism", 10)
                    spark.conf.set("spark.sql.shuffle.partitions", 10)

                    # Read data from table
                    src_df = (
                        spark.read.format("jdbc").option("url", jdbc_url)
                            .option("driver", driver)
                            .option("dbtable", "(" + query + ") AS tbl")
                            .option("user", username)
                            .option("password", password).load())

                    # src_df.persist()

                    # Uncomment to return all row(s)
                    # src_df.show(src_df.count(), False)

                    # Uncomment for testing purpose(s)
                    # src_df.show()

                    # Anonymize sensitive data
                    if len(json_tbl_config['table'][tbl][0]['anonymize']) > 0:
                        for anon in json_tbl_config['table'][tbl][0][
                            'anonymize'
                        ]:
                            anon_col = anon['column']

                            fake_udf = udf(fake.pystr, StringType())

                            anon_df = src_df.withColumn(anon_col,
                                                        fake_udf())

                            # Uncomment for testing purpose(s)
                            # anon_df.show()

                            # Process data to S3
                            aws_access_key = str(json_env_config['s3'][0][
                                                     'access_key'])

                            aws_secret_key = str(json_env_config['s3'][0][
                                                     'secret_Key'])

                            bucket_name = str(json_env_config['s3'][0][
                                                  'bucket_name'])

                            spark.sparkContext._jsc.hadoopConfiguration().set(
                                "fs.s3a.access.key",
                                aws_access_key)
                            spark.sparkContext._jsc.hadoopConfiguration().set(
                                "fs.s3a.secret.key",
                                aws_secret_key)
                            spark.sparkContext._jsc.hadoopConfiguration().set(
                                "fs.s3a.endpoint",
                                "s3.amazonaws.com")
                            spark.sparkContext._jsc.hadoopConfiguration().set(
                                "fs.s3a.impl",
                                "org.apache.hadoop.fs.s3a.S3AFileSystem")
                            spark.sparkContext._jsc.hadoopConfiguration().set(
                                "com.amazonaws.services.s3.enableV4",
                                "true")
                            spark.sparkContext._jsc.hadoopConfiguration().set(
                                "fs.s3a.endpoint",
                                "s3.us-east-1.amazonaws.com")

                            partition_year = date.today().year
                            partition_month = date.today().month
                            partition_day = date.today().day

                            s3 = "s3a://{0}/year={1}/month={2}/" \
                                 "day={3}/{4}.parquet".format(bucket_name,
                                                              partition_year,
                                                              partition_month,
                                                              partition_day,
                                                              tbl)

                            anon_df.repartition(1).write.mode(
                                'overwrite').parquet(s3)

        except Exception as e:
            print("Exception: {0}".format(e))
            pl_log.logger_general(pipeline_log_file, "INFO",
                                  "Exception: {0}".format(e))
