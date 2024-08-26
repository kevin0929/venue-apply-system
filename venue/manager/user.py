from flask import session

from models import User
from utils.database import connect_to_database


class UserManager:
    def __init__(self) -> None:
        self.session = connect_to_database()
        self.operationError = (None, "Some operation went wrong, please contact admin.")
    
    
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
