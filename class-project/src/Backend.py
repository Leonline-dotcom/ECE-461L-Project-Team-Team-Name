import os
from flask import Flask, jsonify
from flask_cors import cross_origin,CORS

app=Flask(__name__,static_folder='.build',static_url_path='/')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#Sign Up Backend
@app.route('/Sign-Up/<User>/<Pass>')