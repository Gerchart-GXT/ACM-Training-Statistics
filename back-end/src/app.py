from component.browser import Browser
from OJs.codeforces import Codeforces
from API.codeforces import API_Codeforces_Insertuser, API_Codeforces_updateUserInfo, API_Codeforces_updateUserSub, API_Codeforces_DeleteUser, API_Codeforces_GetUsersInfo, API_Codeforces_SearchUserInfo, API_Codeforces_GetUsersSub
from flask import Flask
from component.logger import Logger

def main():
    app = Flask(__name__)

    browser = Browser()
    codeforces = Codeforces(urlPath="./url.json", browser=browser)

    app.add_url_rule('/api/codeforces/insert-user', view_func=API_Codeforces_Insertuser.as_view("/api/codeforces/insert-user", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/update-user-info', view_func=API_Codeforces_updateUserInfo.as_view(name="/api/codeforces/update-user-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/update-user-sub', view_func=API_Codeforces_updateUserSub.as_view(name="/api/codeforces/update-user-sub", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/delete-user', view_func=API_Codeforces_DeleteUser.as_view(name="/api/codeforces/delete-user", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-users-info', view_func=API_Codeforces_GetUsersInfo.as_view(name="/api/codeforces/get-users-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/search-users-info', view_func=API_Codeforces_SearchUserInfo.as_view(name="/api/codeforces/search-users-info", codeforces=codeforces), methods=['GET'])
    app.add_url_rule('/api/codeforces/get-users-sub', view_func=API_Codeforces_GetUsersSub.as_view(name="/api/codeforces/get-users-sub", codeforces=codeforces), methods=['GET'])
    
    app.run(debug=True)

if __name__ == "__main__":
    Logger.__init__()
    main()