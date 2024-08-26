from sqlalchemy.exc import SQLAlchemyError

from models import User
from utils.database import connect_to_database


class UserManager:
    def __init__(self) -> None:
        self.session = connect_to_database()
        self.operationError = (None, "Some operation went wrong, please contact admin.")
    
    
    def get_all_user(self) -> User:
        '''Get all user from db'''

        try:
            users = self.session.query(User).all()

            if users is None:
                return (None, "There is no available user now.")
        except Exception:
            return self.operationError

        return users


    def get_user_by_username(self, username: str) -> str:
        '''Get password base on username'''

        if not username:
            return (None, "User name is required")
        
        try:
            user = self.session.query(User).filter_by(username=username).first()

            if user is None:
                return (None, f"No match user with username : {username}")
        except Exception:
            return self.operationError

        return user

    
    def get_user_by_id(self, userid) -> User:
        '''Get current user by session'''

        try:
            user = self.session.query(User).filter_by(userid=userid).first()

            if user is None:
                return (None, f"Session has no information about loginer.")
        except Exception:
            return self.operationError
        
        return user

    
    def add_user(self, userinfo) -> None:
        '''Add user into db'''

        username = userinfo['username']
        password = userinfo['password']
        email = userinfo['email']
        role = userinfo['role']

        try:
            user = User(username=username, password=password, email=email, role=role)
            self.session.add(user)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")

    
    def edit_user(self, user, userinfo) -> None:
        '''Edit user info from db'''

        new_username = userinfo['username']
        new_email = userinfo['email']
        new_role = userinfo['role']

        try:
            user.username = new_username
            user.email = new_email
            user.role = new_role
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")

    
    def delete_user(self, userid) -> None:
        '''Delete user from db'''

        try:
            user = self.session.query(User).filter_by(userid=userid).first()
            self.session.delete(user)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred: {e}")

