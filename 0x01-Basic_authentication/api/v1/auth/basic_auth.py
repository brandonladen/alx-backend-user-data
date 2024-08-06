from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User

class BasicAuth (Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to UTF-8 string
            decoded_str = decoded_bytes.decode('utf-8')
            
            return decoded_str
        except(base64.binascii.Error, UnicodeDecodeError):
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
         # Split the string at the first ':'
        parts = decoded_base64_authorization_header.split(':', 1)
        
        # Return the user email and password
        return (parts[0], parts[1])
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd  is None or not isinstance(user_pwd , str):
            return None
         # Search for user by email
        user_list = User.search({"email": user_email})
        
        if not user_list:
            return None
        
        user = user_list[0]
        
        # Validate password
        if not user.is_valid_password(user_pwd):
            return None
        
        return user
    
    def current_user(self, request=None) -> TypeVar('User'):
        if request is None:
            return None
        header = self.authorization_header(request)
        base_64 = self.extract_base64_authorization_header(header)
        decoded_str = self.decode_base64_authorization_header(base_64)
        user_email, user_pwd = self.extract_user_credentials(decoded_str)
        return self.user_object_from_credentials(user_email, user_pwd)