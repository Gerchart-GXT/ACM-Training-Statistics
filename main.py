from component.browser import Browser
from OJs.codeforces import Codeforces
from API.codeforces import API_Codeforces_Insertuser, API_Codeforces_updateUserLogin, API_Codeforces_updateUserSub, API_Codeforces_DeleteUser, API_Codeforces_GetUsers, API_Codeforces_GetUserInfo, API_Codeforces_GetUserSub
from flask import Flask
import logging

def logInit():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='app.log',
        filemode='w'
    )

def main():
    app = Flask(__name__)

    browser = Browser()
    codeforces = Codeforces(urlPath="./url.json", browser=browser)

    app.add_url_rule('/api/codeforces/insert-user', view_func=API_Codeforces_Insertuser.as_view("/api/codeforces/insert-user", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/update-user-login', view_func=API_Codeforces_updateUserLogin.as_view(name="/api/codeforces/update-user-login", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/update-user-sub', view_func=API_Codeforces_updateUserSub.as_view(name="/api/codeforces/update-user-sub", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/delete-user', view_func=API_Codeforces_DeleteUser.as_view(name="/api/codeforces/delete-user", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-users', view_func=API_Codeforces_GetUsers.as_view(name="/api/codeforces/get-users", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-user-info', view_func=API_Codeforces_GetUserInfo.as_view(name="/api/codeforces/get-user-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-user-sub', view_func=API_Codeforces_GetUserSub.as_view(name="/api/codeforces/get-user-sub", codeforces=codeforces), methods=['GET'])
    
    app.run(debug=True)

if __name__ == "__main__":
    logInit()
    main()