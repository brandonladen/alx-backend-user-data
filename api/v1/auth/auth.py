from flask import request
from typing import List, TypeVar

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
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
        if request is not None:
           return request.headers.get('Authorization', None)
        return None
        
    def current_user(self, request=None) -> TypeVar('User'):
        return None