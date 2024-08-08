#!/usr/bin/env python3
"""Session authentication module for the API.
"""
from .auth import Auth
import uuid
from models.user import User

class SessionAuth (Auth):
    """
    class SessionAuth that inherits from Auth
    """
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """Creates a session id
        """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        
        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        
        return self.__class__.user_id_by_session_id.get(session_id)#user id

    def current_user(self, request=None):
        """returns a User instance based on a cookie value:
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user = User.get(user_id)
        
        return user