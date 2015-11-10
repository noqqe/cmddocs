import re
import os

def add_fileextension(article, extension):
    "add file extension to article"

    if os.path.isfile(article + '.' + extension):
        article = article + '.' + extension

    return article

def remove_fileextension(article, extension):
    "remove file extension"

    extension = '\.' + extension + '$'

    # python3 compatibility
    try:
        extension = bytes(extension,"UTF-8")
    except TypeError:
        pass

    # in python3, re is expecting byte arrays
    article = re.sub(extension, b"", article, flags=re.M)
    article = article.decode("UTF-8")

    return article
