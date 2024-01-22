from flask import jsonify, request
from flask.views import MethodView
from OJs.codeforces import Codeforces
import logging

class API_Codeforces_Insertuser(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            userName = request.args.get("userName") 
            logging.info("API_Codeforces_Insertuser " + userName)
            data = {
                "success": self.codeforces.insertUser(userName=userName)
            }
        except Exception as e:
            logging.info("API_Codeforces_Insertuser Failed" + str(e))
        return jsonify(data)

class API_Codeforces_updateUserInfo(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            logging.info("API_Codeforces_updateUserInfo ")
            data = {
                "success": self.codeforces.updateUsersInfo(),
            }
        except Exception as e:
            logging.info("API_Codeforces_updateUserInfo Failed" + str(e))
        return jsonify(data)



class API_Codeforces_updateUserSub(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            verdict = request.args.get("verdict") 
            try:
                minTMP = request.args.get("minTMP")
                logging.info("API_Codeforces_updateUserSub " + verdict + " " + minTMP)
                data = {"success": self.codeforces.updateUsersSub(verdict=verdict, minTMP=minTMP)}
            except Exception as e:
                logging.info("verdict is None")
                logging.info("API_Codeforces_updateUserSub " + verdict)
                data = {"success": self.codeforces.updateUsersSub(verdict=verdict)}

        except Exception as e:
            logging.info("API_Codeforces_updateUserSub Failed" + str(e))
        return jsonify(data)
    
class API_Codeforces_DeleteUser(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            userName = request.args.get("userName") 
            logging.info("API_Codeforces_DeleteUser " + userName)
            data = {"success": self.codeforces.deleteUser(userName=userName)}
        except Exception as e:
            logging.info("API_Codeforces_DeleteUser Failed" + str(e))
        return jsonify(data)
    
class API_Codeforces_GetUsersInfo(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            logging.info("API_Codeforces_GetUsersInfo ")

            users = [list(i) for i in self.codeforces.db.executeSQL(sql=
                f'''
                    SELECT userName, isOnline, rankCurrent, rankMax FROM cf_user
                '''
            )]
            data = {
                "success": True, 
                "users":[
                    {
                        "userName": user[0],
                        "isOnline": user[1],
                        "rankCurrent": user[2],
                        "rankMax": user[3]
                    } for user in users
                ]
            }
        except Exception as e:
            logging.info("API_Codeforces_GetUsersInfo Failed" + str(e))
        return jsonify(data)
    
class API_Codeforces_SearchUserInfo(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            userName = request.args.get("userName") 
            logging.info("API_Codeforces_SearchUserInfo " + userName)
            userInfo = self.codeforces._getUserInfo(userName=userName)
            data = {
                "success": userInfo["found"], 
                "userInfo": {
                    "userName":userInfo["userName"],
                    "rankCurrent":userInfo["rank"]["current"],
                    "rankMax":userInfo["rank"]["max"],
                    "loginStatus":userInfo["loginStatus"]
                }
            }
        except Exception as e:
            logging.info("API_Codeforces_SearchUserInfo Failed" + str(e))
        return jsonify(data)

class API_Codeforces_GetUsersSub(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        try:
            userName = request.args.get("userName") 
            verdict = request.args.get("verdict") 
            logging.info("API_Codeforces_GetUsersSub " + userName + " " + verdict)
            subs = [list(i) for i in self.codeforces.db.executeSQL(sql=
                f'''
                    SELECT * FROM cf_sub
                    WHERE userName = "{userName}" AND status = "{verdict}"
                '''
            )]
            data = {
                "success": True if len(subs) > 0 else False, 
                "subInfo": [
                    {
                        "userName": sub[0],
                        "subTMP": sub[1],
                        "subID": sub[2],
                        "proPath": sub[3],
                        "status": sub[4]
                    } for sub in subs
                ]
            }
        except Exception as e:
            logging.info("API_Codeforces_GetUsersSub Failed" + str(e))
        return jsonify(data)