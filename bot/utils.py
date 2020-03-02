import logging
from decos import log
#  Utils for Bot


@log
def get_key(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
