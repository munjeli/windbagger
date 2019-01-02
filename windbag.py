import cfg
import logging
import twitter_util

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
        self.communications = []

    def build_data(self, office_data, official_data):
        logger.debug(office_data)
        level = office_data['divisionId'].split("/")[-1]
        if level.split(':')[0] in ['county', 'council_district']:
            self.level = 'local'
        elif 'state' in level:
            self.level = 'state'
        elif 'country' in level:
            self.level = 'federal'

        try:
            if 'country' in office_data['levels']:
                self.level = 'federal'
        except KeyError:
            pass

        if 'name' in office_data: self.title = office_data['name']
        if 'name' in official_data: self.name = official_data['name']
        if 'party' in official_data: self.party = official_data['party']
        if 'phones' in official_data: self.phone = official_data['phones']
        if 'emails' in official_data: self.email = official_data['emails']
        if 'urls' in official_data: self.website = official_data['urls']
        if 'photoUrl' in official_data:
            self.image_link = official_data['photoUrl']
        else:
            self.image_link = "https://upload.wikimedia.org/wikipedia/commons/f/f3/Uncle_Sam_%28pointing_finger%29.jpg"
        logger.debug(self.website)

        try:
            for c in official_data['channels']:
                if 'Facebook' in c['type']:
                    self.facebook_id = c['id']
                elif 'Twitter' in c['type']:
                    self.twitter_id = c['id']
                elif 'GooglePlus' in c['type']:
                    self.google_id = c['id']
                elif 'YouTube' in c['type']:
                    self.you_tube_id = c['id']
        except Exception as e:
            logger.warning(e)

        cfg.rep_arr.append(self)

    def stuff_communications(self):
        if self.twitter_id:
            tweets = twitter_util.fetch_latest(self.twitter_id)
            if tweets:
                self.communications.append(tweets)

