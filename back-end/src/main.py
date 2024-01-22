from component.browser import Browser
from OJs.codeforces import Codeforces
from API.codeforces import API_Codeforces_Insertuser, API_Codeforces_updateUserInfo, API_Codeforces_updateUserSub, API_Codeforces_DeleteUser, API_Codeforces_GetUsersInfo, API_Codeforces_SearchUserInfo, API_Codeforces_GetUsersSub
from flask import Flask
from flask_cors import CORS
from component.logger import Logger
from component.circleTask import CircleTask

import threading
import requests

from waitress import serve

def UpdateUserInfoWithAPI():
    Logger.callFunction()
    url = 'http://localhost:5000/api/codeforces/update-user-info'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == True:
            Logger.retFunction("success")
    else:
        Logger.retFunction("failed " + response.status_code )

def UpdateUserSubWithAPI():
    Logger.callFunction()
    url = 'http://localhost:5000/api/codeforces/update-user-sub' 
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == True:
            Logger.retFunction("success")
    else:
        Logger.retFunction("failed " + response.status_code )

def create_app():
    app = Flask(__name__)
    CORS(app)
    browser = Browser()
    codeforces = Codeforces(urlPath="./url.json", browser=browser)

    app.add_url_rule('/api/codeforces/insert-user', view_func=API_Codeforces_Insertuser.as_view("/api/codeforces/insert-user", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/update-user-info', view_func=API_Codeforces_updateUserInfo.as_view(name="/api/codeforces/update-user-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/update-user-sub', view_func=API_Codeforces_updateUserSub.as_view(name="/api/codeforces/update-user-sub", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/delete-user', view_func=API_Codeforces_DeleteUser.as_view(name="/api/codeforces/delete-user", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-users-info', view_func=API_Codeforces_GetUsersInfo.as_view(name="/api/codeforces/get-users-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/search-users-info', view_func=API_Codeforces_SearchUserInfo.as_view(name="/api/codeforces/search-users-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-users-sub', view_func=API_Codeforces_GetUsersSub.as_view(name="/api/codeforces/get-users-sub", codeforces=codeforces), methods=['GET'])
    
    return app

def main():
    app = create_app()

    server = threading.Thread(target=lambda: serve(app, host="localhost", port=5000))
    server.start()
    UpdateUserInfoWithAPI()
    UpdateUserSubWithAPI()

    updateUserInfo = CircleTask(task=UpdateUserInfoWithAPI, TSecond=30)
    updateUserInfo.run()
    updateUserSub = CircleTask(task=UpdateUserSubWithAPI, TSecond=300)
    updateUserSub.run()
    
    
if __name__ == "__main__":
    Logger.__init__()
    main()
