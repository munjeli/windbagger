import requests
import logging
from windbag import Windbag
import cfg
import json

fmt = "%(levelname)s\t%(funcName)s():%(lineno)i\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)


def fetch_gca_creds():
    key_path = 'C:/Users/munjeli/.ssh/windbagger-key'
    with open(key_path, 'r') as key_file:
        return key_file.readline().rstrip("\n\a")


def fetch_reps_data():
    dev_key = fetch_gca_creds()
    gcivic_url = "https://www.googleapis.com/civicinfo/v2/representatives?key={}&".format(dev_key)
    address = "address=3131%20Homestead%20Road%20Santa%20Clara%20CA"
    reps_data = requests.get(gcivic_url + address).json()
    logger.debug(reps_data)

    windbags = []
    for office in reps_data['offices']:
        for i in office['officialIndices']:
            windbag = Windbag()
            windbag.build_data(office, reps_data['officials'][i])
            windbags.append(windbag)
    return windbags

if __name__ == "__main__":
    fetch_reps_data()
    for rep in cfg.rep_arr:
        logger.debug(rep.name)

