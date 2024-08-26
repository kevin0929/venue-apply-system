from sqlalchemy.exc import SQLAlchemyError

from models import Venue
from utils.database import connect_to_database


class VenueManager:
    def __init__(self) -> None:
        self.session = connect_to_database()
        self.operationError = (None, "Some operation went wrong, please contact admin.")
    
    def get_all_venue(self) -> Venue:
        '''Get all venue from db'''

        try:
            venues = self.session.query(Venue).order_by(Venue.vid.asc()).all()

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
    

    def add_venue(self, create_name) -> None:
        '''Add new venue into db'''

        try:
            new_venue = Venue(name=create_name)
            self.session.add(new_venue)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")

    def delete_venue_by_id(self, vid) -> None:
        '''Delete venue by id from db'''

        try:
            venue = self.session.query(Venue).filter_by(vid=vid).first()
            self.session.delete(venue)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")

    
    def modify_venue_name(self, venue, new_name) -> None:
        '''Modify venue's name'''

        try:
            venue.name = new_name
            self.session.commit()
        except Exception:
            return self.operationError
