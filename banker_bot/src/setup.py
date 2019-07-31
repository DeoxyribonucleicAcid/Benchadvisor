import argparse
import json
import logging
import os
import pymongo

import setproctitle

from src.State import State

logger = logging.getLogger(__name__)


def prepare_environment():
    setproctitle.setproctitle("banker_bot")
    parser = argparse.ArgumentParser(description='Basic bench rating bot.')
    parser.set_defaults(which='no_arguments')
    parser.add_argument('-d', '--debug', action='store_true', required=False, help='Debug mode')

    if os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + '/conf.json'):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/conf.json') as f:
            config = json.load(f)
    else:
        raise EnvironmentError("Config file not existent or wrong format")
    args = parser.parse_args()
    if not args.debug:
        State.DEBUG = False
        State.token = config['token']
    else:
        State.DEBUG = True
        State.token = config['test_token']

    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/res/tmp'
    if not os.path.exists(directory):
        os.makedirs(directory)

    db_setup()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                        handlers=[logging.FileHandler('.log', 'w', 'utf-8')])


def db_setup():
    if os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + '/conf.json'):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/conf.json') as f:
            config = json.load(f)
    else:
        raise EnvironmentError("Config file not existent or wrong format")
    client = pymongo.MongoClient(config["mongo_db_srv"])

    if State.DEBUG:
        if "database_debug" in client.list_database_names():
            logging.info("The database exists.")
        else:
            raise EnvironmentError('Debug database does not exist!')

        db = client["database_debug"]
    else:
        if "database" in client.list_database_names():
            logging.info("The database exists.")
        else:
            raise EnvironmentError('Database does not exist!')

        db = client["database"]

    if "bench" in db.list_collection_names():
        logging.info("The collection exists.")
    else:
        raise EnvironmentError('Collection does not exist!')

    bench_collection = db["bench"]
    State.db = db
    State.bench_col = bench_collection
