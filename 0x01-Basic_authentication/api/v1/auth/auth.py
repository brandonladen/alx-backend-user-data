#!/usr/bin/env python3
"""
Module for authentication in a Flask application.

This module contains the Auth class that handles the authentication logic for the API.
"""

from flask import request
from typing import List, TypeVar

class Auth:
    """
    Auth class for handling authentication.

    This class provides methods to check required authentication, retrieve the
    authorization header from a request, and obtain the current user.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        
        # Normalize the path by removing trailing slashes
        normalized_path = path.rstrip('/')

        # Check if the path matches any of the excluded paths
        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            if normalized_path == normalized_excluded_path:
                return False

        # If no match is found, return True
        return True
    
    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from a request.

        Args:
            request: The Flask request object (optional).

        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is not None:
           return request.headers.get('Authorization', None)
        return None
        
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user based on the request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user, or None if not authenticated.
        """
        return None
