import argparse
import json
import logging
import os

import setproctitle

from src.State import State

logger = logging.getLogger(__name__)


def prepare_environment():
    setproctitle.setproctitle("banker_bot")
    parser = argparse.ArgumentParser(description='Basic pokemon bot.')
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

    # db_setup()

    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
    #                     handlers=[logging.FileHandler('.log', 'w', 'utf-8')])


def db_setup():
    pass
