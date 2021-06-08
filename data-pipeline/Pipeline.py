# -*- coding: utf-8 -*-
"""Pipeline main process

This module will execute the pipeline process

Author:
    Elvin Ellis Smith Jr

Example:
    $ python Pipeline.py

To-do:
    * NA

Changelog:
    * 2021-05-01: Initial release

License:
    MIT <https://mit-license.org/>
"""

from PipelineImport.PipelineImport import PipelineImport
from PipelineLogger.PipelineLogger import PipelineLogger


class Pipeline:
    """This class will execute the pipeline process"""

    def __init__(self, pipeline_env, pipeline_process_id):
        """
        Class initialization

        Args:
        :type pipeline_env: object
        :type pipeline_process_id: object
        """
        self.pipeline_env = pipeline_env
        self.pipeline_process_id = pipeline_process_id

    def pipeline(self):
        """Pipeline process manager."""
        try:
            pl_log.logger_general(pipeline_log_file, "INFO", "Pipeline "
                                                             "Import "
                                                             "Process "
                                                             "- Start")

            if self.pipeline_process_id == "IMPORT":
                pl_import = PipelineImport(self.pipeline_env)
                pl_import.pipeline_import()

            # elif self.pipeline_process_id == "export":
            #     pl_export = PipelineExport
            # else:
            #     pl_full = PipelineFull

        except Exception as e:
            print("Exception: {0}".format(e))
            pl_log.logger_general(pipeline_log_file, "INFO",
                                  "Exception: {0}".format(e))


if __name__ == "__main__":
    # Create logging instance
    pipeline_log_file = './logs/pipeline.log'
    pl_log = PipelineLogger()

    # Execute pipeline process
    pli = Pipeline("DEVELOPMENT", "IMPORT")
    pli.pipeline()
