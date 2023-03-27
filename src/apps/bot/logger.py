import os


def create_log_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
