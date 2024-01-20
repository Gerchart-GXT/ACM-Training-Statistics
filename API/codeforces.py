from flask import jsonify, request
from flask.views import MethodView
from OJs.codeforces import Codeforces

class API_Codeforces_Insertuser(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        userName = request.args.get("userName") 
        data = {"success": self.codeforces.insertUser(userName=userName)}
        return jsonify(data)
    
class API_Codeforces_updateUserLogin(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        data = {"success": self.codeforces.updateUsersLogin()}
        return jsonify(data)

class API_Codeforces_updateUserSub(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        verdict = request.args.get("verdict") 
        print(verdict)
        minTMP = request.args.get("minTMP")
        data = {"success": self.codeforces.updateUsersSub(verdict=verdict, minTMP=minTMP)}
        return jsonify(data)
    
class API_Codeforces_DeleteUser(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        userName = request.args.get("userName") 
        data = {"success": self.codeforces.deleteUser(userName=userName)}
        return jsonify(data)
    
class API_Codeforces_GetUsers(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        users = [i[0] for i in self.codeforces.db.executeSQL(sql=
            f'''
                SELECT userName FROM cf_user
            '''
        )]
        data = {
            "success": True, 
            "users":users
        }
        return jsonify(data)
    
class API_Codeforces_GetUserInfo(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        userName = request.args.get("userName") 
        userInfo = self.codeforces._getUserInfo(userName=userName)
        data = {
            "success": userInfo["found"], 
            "userInfo": userInfo
        }
        return jsonify(data)

class API_Codeforces_GetUserSub(MethodView):
    def __init__(self, codeforces:Codeforces):
        super().__init__()
        self.codeforces = codeforces

    def get(self):
        userName = request.args.get("userName") 
        verdict = request.args.get("verdict") 
        subs = self.codeforces.db.executeSQL(sql=
            f'''
                SELECT * FROM cf_sub
                WHERE userName = "{userName}"
            '''
        )
        data = {
            "success": True if len(subs) > 0 else False, 
            "userInfo": subs
        }
        return jsonify(data)