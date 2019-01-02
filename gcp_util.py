import requests
import logging
from urllib.parse import quote
from windbag import Windbag
import cfg
import json

fmt = "%(levelname)s\t%(funcName)s():%(lineno)i\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)


def fetch_gca_creds():
    """
    read the credentials file for the app and return the key
    :return: api key for google civic api
    """
    key_path = 'C:/Users/munjeli/.ssh/windbagger-key'
    with open(key_path, 'r') as key_file:
        return key_file.readline().rstrip("\n\a")


def fetch_reps_data(address):
    """
    lookup the representatives for a given address with google civic api
    :param address:
    :return: array of windbags
    """
    logger.debug(address)
    dev_key = fetch_gca_creds()
    gcivic_url = "https://www.googleapis.com/civicinfo/v2/representatives?key={}&address=".format(dev_key)
    user_address = quote(address, safe='')
    try:
        reps_data = requests.get(gcivic_url + user_address)
        if reps_data.status_code != 200:
            return 'address not found'
    except Exception as e:
        logger.debug(e)

    windbags = []
    for office in reps_data.json()['offices']:
        for i in office['officialIndices']:
            windbag = Windbag()
            windbag.build_data(office, reps_data.json()['officials'][i])
            windbag.stuff_communications()
            windbags.append(windbag)
    return windbags


if __name__ == "__main__":
    print('heyo')

