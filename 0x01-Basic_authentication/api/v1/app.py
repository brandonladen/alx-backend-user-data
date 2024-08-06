#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv('AUTH_TYPE')

if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
else:
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()



@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    Before request handler to enforce Basic Authentication.

    This function is executed before processing any request. It checks the
    request path and enforces authentication for routes not excluded. If
    authentication is required and either the authorization header is missing
    or the user could not be authenticated, the function will return an error
    response:
        - 401 Unauthorized if the authorization header is missing.
        - 403 Forbidden if the user could not be authenticated.

    Excluded paths are:
        - /api/v1/status/
        - /api/v1/unauthorized/
        - /api/v1/forbidden/
    """
    # Skip authentication for certain paths
    if request.path in ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']:
        return

    # Check if authentication is required for the path
    if not auth.require_auth(request.path, ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']):
        return
    
    # Check if the authorization header is present
    if auth.authorization_header(request) is None:
        abort(401)

    # Check if the current user is authenticated
    if auth.current_user(request) is None:
        abort(403)
    
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
