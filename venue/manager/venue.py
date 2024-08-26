from models import Venue
from utils.database import connect_to_database


class VenueManager:
    def __init__(self) -> None:
        self.session = connect_to_database()
        self.operationError = (None, "Some operation went wrong, please contact admin.")
    
    def get_all_venue(self) -> Venue:
        '''Get all venue from db'''

        try:
            venues = self.session.query(Venue)

            if venues is None:
                return (None, "There is no available venue now.")
        except Exception:
            return self.operationError

        return venues
    

    def get_venue_by_id(self, vid: int) -> Venue:
        '''Get venue by id'''

        try:
            venue = self.session.query(Venue).filter_by(vid=vid).first()

            if venue is None:
                return (None, "The vid does not match any venue.")
        except Exception:
            return self.operationError
        
        return venue
