from flask import Blueprint, request
from requests import get
from function_jwt import validate_token
import time
import json
from pyModbusTCP.client import ModbusClient
users_github = Blueprint("users_github", __name__)


@users_github.before_request
def verify_token_middleware():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token,output=False)

@users_github.route("/github/users", methods=["POST"])
def github():
    data = request.get_json()
    #print(data)
    payload = data['payload']
    c = ModbusClient(host='localhost', port=502, auto_open=True, debug=False)
    if data['payload'] == 'holdingRegister':
        regs = c.read_holding_registers(0, 100)
    if data['payload'] == 'InputRegister':
        regs = c.read_input_registers(0,100)
    if data['payload'] == 'Coil':
        regs = c.read_coils(0,100)
    if data['payload'] == 'discreteInput':
        regs = c.read_discrete_inputs(0,100)
    return {"Read Function": data['payload'],
            "payload": regs}
