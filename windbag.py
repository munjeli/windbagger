import cfg
import logging

fmt = "%(levelname)s\t%(funcName)s():%(lineno)i\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)


class Windbag:
    def __init__(self):
        self.name = ''
        self.channels = []
        self.title = ''
        self.email = ''
        self.phone = ''
        self.website = ''
        self.twitter_id = ''
        self.you_tube_id = ''
        self.facebook_id = ''
        self.google_id = ''
        self.level = ''
        self.image_link = ''
        self.party = ''

    def build_data(self, office_data, official_data):
        level = office_data['divisionId'].split("/")[-1]
        if level.split(':')[0] in ['county', 'council_district']:
            self.level = 'local'
        elif 'state' in level:
            self.level = 'state'
        elif 'country' in level:
            self.level = 'federal'

        try:
            self.title = office_data['name']
            self.name = official_data['name']
            self.party = official_data['party']
            self.phone = official_data['phones']
            self.email = official_data['emails']
            self.website = official_data['urls']
            self.image_link = official_data['photoUrl']

            for c in official_data['channels']:
                if 'Facebook' in c['type']:
                    self.facebook_id = c['id']
                elif 'Twitter' in c['type']:
                    self.twitter_id = c['id']
                elif 'GooglePlus' in c['type']:
                    self.google_id = c['id']
                elif 'YouTube' in c['type']:
                    self.you_tube_id = c['id']

        except KeyError:
            pass

        cfg.rep_arr.append(self)
