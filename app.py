#!/usr/bin/env python3

import os
import sys
from absl import app as absl_app 
from absl import flags
import flask
from flask import request, jsonify

from daemon import *



FLAGS = flags.FLAGS
flags.DEFINE_string("iroha_addr", "127.0.0.1", "iroha host address.")
flags.DEFINE_integer("iroha_port", 50051, "iroha host port.")
flags.DEFINE_string("account_id", "admin@test", "Your account ID.")


app = flask.Flask(__name__)
app.config["DEBUG"] = True
keys = Keypair('f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70', '313a07e6384776ed95447710d15e59148473ccfc052a681317a72a69f2a49910')
daemon = None

@app.route("/api/v1/get_all_table", methods=['GET'])
def select():
    global daemon
    return jsonify(daemon.show_all_tables())


@app.route("/api/v1/create_table", methods=['POST'])
def create_table():
    global daemon
    data = request.get_json()
    daemon.create_table(data['table_name'])
    return "Created", 201


@app.route("/api/v1/insert", methods=['POST'])
def insert():
    global daemon
    data = request.get_json()
    j = data['data']

    if daemon.insert_data(Entry(**j)) == True:
        return "OK", 201
    else:
        return "", 500


@app.route("/api/v1/get_data", methods=['POST'])
def select_data():
    global daemon
    data = request.get_json()
    table = data['table_name']
    return json.dumps(daemon.get_data(table))


@app.route("/api/v1/select_columns", methods=['POST'])
def select_columns():
    global daemon
    data = request.get_json()
    table = data['table_name']
    columns = data['columns']
    return json.dumps(daemon.select_columns(table, columns)) # need to format the data to be sent


def main(argv):
    """
    Main function.
    """
    logging.set_verbosity(logging.DEBUG)
    if sys.version_info[0] < 3:
        raise Exception('Python 3 or a more recent version is required.')
    global daemon
    daemon = Daemon(FLAGS, keys)
    app.run(host = '0.0.0.0')
    
    

if __name__ == '__main__':
    absl_app.run(main)