#!/usr/bin/python3
"""
module creates status route
"""
from api.v1.views import app_views

@app_views.route('/status')
def show_status():
    return {"status": "OK"}
