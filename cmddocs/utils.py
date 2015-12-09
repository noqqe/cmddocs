""" File Extension Add/Remove Util"""

import re

def add_fileextension(article, extension):
    "add file extension to article"

    article = article + '.' + extension

    return article

def remove_fileextension(article, extension):
    "remove file extension"

    extension = r'\.' + extension + '$'
    article = re.sub(extension, "", article, flags=re.M)

    return article
