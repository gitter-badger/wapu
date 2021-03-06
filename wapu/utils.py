# -*- coding: utf-8 -*-

from functools import wraps
import requests
from .errors import AuthException
import re


def auth_required_decorator(url, msg):
    def wrapper(f):
        @wraps(f)
        def returned_wrapper(*args, **kwargs):
            obj = args[0]  # Instancia de algun wrapper, deberia tener un campo __cookies__ con ... la cookie
            req = requests.get(url, headers=obj.__headers__, cookies=obj.__cookies__, **kwargs)
            if msg in req.text:
                raise AuthException('Oh-Oh problema de autenticación! prueba realizando nuevamente el login')
            return f(*args, **kwargs)

        return returned_wrapper

    return wrapper


def read_nota(s):
    try:
        nota = float(re.findall('\d+,\d+', s)[0].replace(',', '.'))
    except IndexError:
        nota = None
    return nota

def read_ponderacion(s):
    try:
        ponderacion = float(re.findall('\d+', s)[0])
        ponderacion /= 100
    except IndexError:
        ponderacion = None
    return ponderacion