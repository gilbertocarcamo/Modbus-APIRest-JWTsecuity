from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
import datetime
from flask import jsonify
import jwt
from Crypto.PublicKey import RSA
import pytz
import time
import json
from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa 

# funcion que permite guardar los archivos PEM de las llaves publicas y privadas
def save_file(filename, content):  
   f = open(filename, "wb")  
   f.write(content) 
   f.close()  


def expire_date(EXPseconds: int):
    #modificaremos agunos prarmetros de la funcion agregamos la Zona Horaria y la duracion del token es en segundos
    tz = pytz.timezone('America/Panama')
    ct = datetime.datetime.now(tz=tz)
    new_date = ct + datetime.timedelta(seconds = EXPseconds)
    return ct, new_date


def write_token(data: dict):
    #calcularemos la llave privada y publica usando RSA256 y crearemos dos archivos PEM, uno para la llave publica y otro para la llave privada
    
    # generate private key & write to disk  
    private_key = rsa.generate_private_key(  
        public_exponent=65537,  
        key_size=4096,  
        backend=default_backend()  
    )  
    pem = private_key.private_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PrivateFormat.PKCS8,  
        encryption_algorithm=serialization.NoEncryption()  
    )  
    save_file("private.pem", pem)  
    
    # generate public key  
    public_key = private_key.public_key()  
    pem = public_key.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo  
    )  
    save_file("public.pem", pem) 
    tiempo = expire_date(120)
    token = jwt.encode(payload = {"some": "payload", "iat": tiempo[0], "exp": tiempo[1]}, key = private_key, algorithm="RS256")
    return token.encode("UTF-8")


def validate_token(token, output=False):
    with open('public.pem') as f:
        public_key = f.read()
    try:
        if output:
            return decode(token, key=public_key, algorithms=["RS256"])
        decode(token, key=public_key, algorithms=["RS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response
