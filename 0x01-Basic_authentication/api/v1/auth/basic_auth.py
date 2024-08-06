#!/usr/bin/env python3
"""
Module for Basic authentication in a Flask application.

This module defines the BasicAuth class that provides methods for Basic
Authentication, including extracting and decoding Base64 authorization headers,
and retrieving user credentials from them.
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User

class BasicAuth(Auth):
    """
    BasicAuth class for handling Basic Authentication.

    This class inherits from Auth and provides methods specific to Basic Authentication.
    It includes methods to extract, decode, and validate user credentials from
    Base64 encoded authorization headers.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 part from the Authorization header.

        Args:
            authorization_header (str): The Authorization header containing the Base64 string.

        Returns:
            str: The Base64 part of the Authorization header, or None if conditions are not met.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded authorization header.

        Returns:
            str: The decoded value as a UTF-8 string, or None if decoding fails.
        """
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
        """
        Extract user credentials from the decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string containing user credentials.

        Returns:
            tuple: A tuple containing the user email and password, or (None, None) if conditions are not met.
        """
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
        """
        Retrieve a User instance based on the provided email and password.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            TypeVar('User'): The User instance if credentials are valid, or None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
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
        """
        Retrieve the current user based on the request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user if authentication is successful, or None otherwise.
        """
        if request is None:
            return None
        header = self.authorization_header(request)
        base_64 = self.extract_base64_authorization_header(header)
        decoded_str = self.decode_base64_authorization_header(base_64)
        user_email, user_pwd = self.extract_user_credentials(decoded_str)
        return self.user_object_from_credentials(user_email, user_pwd)
