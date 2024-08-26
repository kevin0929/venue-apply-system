from sqlalchemy.exc import SQLAlchemyError

from models import Application
from utils.database import connect_to_database



class ApplicationManager:
    def __init__(self) -> None:
        self.session = connect_to_database()
    
    def add_application(self, user, venue, datetime, order):
        '''Insert application into db'''

        try:
            application = Application(userid=user.userid, vid=venue.vid, datetime=datetime, order=order)
            self.session.add(application)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")
