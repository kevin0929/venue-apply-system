from sqlalchemy.exc import SQLAlchemyError

from models import Application
from utils.database import connect_to_database



class ApplicationManager:
    def __init__(self) -> None:
        self.session = connect_to_database()
        self.operationError = (None, "Some operation went wrong, please contact admin.")
    
    
    def get_all_application(self) -> Application:
        '''Get all applications in db'''

        try:
            applications = self.session.query(Application)

            if applications is None:
                return (None, 'The application is empty now.')
        except Exception:
            self.operationError
        
        return applications


    def check_application_conflict(self, venue, datetime, order=1) -> bool:
        '''Check whether the venue has reverse in same datetime'''

        try:
            application = self.session.query(Application).filter_by(vid=venue.vid, datetime=datetime, order=order).all()

            if application:
                return True
        except Exception:
            self.operationError

        return False

    
    def add_application(self, user, venue, datetime, order) -> None:
        '''Insert application into db'''

        try:
            application = Application(userid=user.userid, vid=venue.vid, datetime=datetime, order=order)
            self.session.add(application)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")


    def delete_application(self, user, venue, datetime) -> None:
        '''Delete application from db'''

        try:
            application = self.session.query(Application).filter_by(vid=venue.vid, userid=user.userid, datetime=datetime).first()

            if application:
                self.session.delete(application)
                self.session.commit()
            else:
                return (None, 'You have not reserved this datetime in venue.')
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")
        