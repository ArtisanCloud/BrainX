from app.logger.log import LOGS_TASK_DIRECTORY, get_logger


logger = get_logger(__name__+'-task', log_dir=LOGS_TASK_DIRECTORY)
# print(logger)
# logger.info("Logger task info initiated")
# logger.error("Logger task error initiated")



logger_rag = get_logger(__name__+'-task-rag', log_dir=LOGS_TASK_DIRECTORY + "rag/")
# print(logger_rag)
# logger_rag.info("Logger task rag  info initiated")
# logger_rag.error("Logger task rag  error initiated")
