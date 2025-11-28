import os
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"
worker_class = "gthread"
