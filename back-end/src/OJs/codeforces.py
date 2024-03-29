from component.browser import Browser
from component.database import SqlLite
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime
import json
from component.logger import Logger

INITTMP = "202401010000"
MONTH = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}

class Codeforces:
    def __init__(self, urlPath):
        Logger.callFunction()
        with open(file=urlPath, mode="r") as file:
            self.urls = json.load(file)
        self.urls = self.urls["codeforces"]

        self.db = SqlLite("codeforces.db")
        self.db.executeSQL(sql=
            '''            
                CREATE TABLE IF NOT EXISTS cf_user (
                    userName TEXT PRIMARY KEY,
                    isOnline INTEGER,
                    rankCurrent INTEGER,
                    rankMax INTEGER,
                    lastLoginUpdateTMP INTEGER,
                    lastSubUpdateTMP INTEGER
                );
            '''
        )
        self.db.executeSQL(sql=
            '''            
                CREATE TABLE IF NOT EXISTS cf_sub (
                    userName TEXT,
                    subTMP INTEGER,
                    subID INTEGER PRIMARY KEY,
                    proPath TEXT,
                    status TEXT,
                    FOREIGN KEY (userName) REFERENCES cf_user(userName) ON DELETE CASCADE
                );
            '''
        )
        Logger.retFunction("success")
    
    def _getUserInfo(self, userName):
        Logger.callFunction()

        url="https://" + self.urls["sni"] + self.urls["user"]["home"] + "/" + userName
        browser = Browser()
        browser.openPage(url)
        try:
            if browser.driver.current_url != url:  
                raise Exception("User Not Found")

            if browser.getElement(css=".userbox .main-info  h1").text != userName:
                raise Exception("Name Not Match")
            infos = browser.getElement(css=".userbox  .info  ul").find_elements(By.CSS_SELECTOR, "li")
            rankLine = None
            loginLine = None
            for i in infos:
                line = i.text.split(' ')
                if (line[0] == "Contest" and rankLine == None):
                    rankLine = line
                if (line[0] == "Last" and loginLine == None):
                    loginLine = line
            Logger.retFunction("success")
            browser.closePage()
            return {
                    "userName":userName,
                    "found": True,
                    "rank": {
                        "current": rankLine[2], 
                        "max": rankLine[len(rankLine) - 1][:-1]
                    },
                    "loginStatus": 1 if loginLine[2] == "online" else 0
            }
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            browser.closePage()
            return {
                "userName":userName,
                "found": False
            }

    def _getUserSubmission(self, userName, verdict, minTMP):
        Logger.callFunction()
        browser = Browser()
        url="https://" + self.urls["sni"] + self.urls["user"]["submission"] + "/" + userName
        try:
            
            browser.openPage(url)

            verdictSelector=Select(browser.getElement(css="form.status-filter select[id='verdictName']"))
            verdictSelector.select_by_visible_text(text=verdict)
            browser.getElement(css="form.status-filter input[value='Apply']").click()

            pageCount = 1
            for i in browser.getElements(css=".page-index"):
                pageCount = max(pageCount, int(i.text))

            subs={}

            outDated = False
            for _ in range(pageCount):
                infos = (browser.getElement("div.datatable table.status-frame-datatable")).find_elements(By.CSS_SELECTOR, "tr")
                infos = infos[1:]
                for line in infos:
                    lineItems = line.find_elements(By.CSS_SELECTOR, "td")
                    subID = lineItems[0].text

                    subTMP = lineItems[1].text.split(' ')
                    subDate = subTMP[0].split('/')
                    subDate[0] = MONTH[subDate[0]]
                    subTime = (subTMP[1][0:2], subTMP[1][3:5])
                    subTMP = f"{subDate[2]}{subDate[0]}{subDate[1]}{subTime[0]}{subTime[1]}"

                    if str(subTMP) < str(minTMP):
                        outDated = True
                        break
                    proPath = lineItems[3].find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    subs[subID] = (proPath, subTMP)
                if outDated == True:
                    break
                if _ + 1 < pageCount:
                    browser.getElement(f"a[href='/submissions/{userName}/page/{_ + 2}']").click()
            Logger.retFunction("success")
            browser.closePage()
            return {
                "userName": userName,
                "found": True if len(subs) > 0 else False,
                "submission": [{
                    "userName":userName, 
                    "proPath": value[0], 
                    "subID": key,
                    "subTMP":value[1],
                    "status": verdict
                } for key, value in subs.items()]
            }
        except Exception as e:
            Logger.retFunction("failed" + str(e))        
            browser.closePage()
            return {
                "userName": userName,
                "found": False,
            }

        
    def _updateUserInfo(self, userInfo, lastSubUpdateTMP):
        Logger.callFunction()

        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M")
            self.db.executeSQL(sql=
                f'''
                    INSERT OR REPLACE INTO cf_user (userName, isOnline, rankCurrent, rankMax, lastSubUpdateTMP, lastLoginUpdateTMP) 
                    VALUES ("{userInfo["userName"]}", "{userInfo["loginStatus"]}", "{userInfo["rank"]["current"]}", "{userInfo["rank"]["max"]}", "{lastSubUpdateTMP}", "{formatted_time}");
                '''
            )
            Logger.retFunction("success")
            return True
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            return False
    
    def _updateSubmission(self, userName, submissions):
        Logger.callFunction()

        try:
            for sub in submissions:
                self.db.executeSQL(sql=
                    f'''
                        INSERT OR REPLACE INTO cf_sub (userName, subTMP, subID, proPath, status) 
                        VALUES ("{sub["userName"]}", "{sub["subTMP"]}", "{sub["subID"]}", "{sub["proPath"]}", "{sub["status"]}")
                    '''
                )
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M")
            self._updateUserInfo(userInfo=self._getUserInfo(userName), lastSubUpdateTMP=formatted_time)
            Logger.retFunction("success")
            return True
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            return False
        
    def insertUser(self, userName):
        Logger.callFunction()

        try:
            apiRes = self._getUserInfo(userName=userName)
            if apiRes["found"] == False:
                raise Exception("User NotFound!")
            self._updateUserInfo(userInfo=apiRes, lastSubUpdateTMP=INITTMP)
            Logger.retFunction("success")
            return True
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            return False

    def updateUsersInfo(self):
        Logger.callFunction()

        try:
            users = self.db.executeSQL(sql=
                f'''
                    SELECT userName FROM cf_user
                '''
            )
            for user in users:
                userName = user[0]
                lastSubUpdateTMP = self.db.executeSQL(sql=
                    f'''
                        SELECT lastSubUpdateTMP FROM cf_user
                        WHERE userName="{userName}"
                    '''
                )[0][0]
                self._updateUserInfo(userInfo=self._getUserInfo(userName=userName), lastSubUpdateTMP=lastSubUpdateTMP)
            Logger.retFunction("success")
            return True
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            return False

    def updateUsersSub(self, minTMP=None):
        Logger.callFunction()

        try:
            users = self.db.executeSQL(sql=
                f'''
                    SELECT userName FROM cf_user
                '''
            )
            for user in users:
                userName = user[0]
                lastSubUpdateTMP = self.db.executeSQL(sql=
                    f'''
                        SELECT lastSubUpdateTMP from cf_user
                        WHERE userName  = "{userName}"
                    '''
                )[0][0] if minTMP == None else minTMP
                subs = []
                apiRes = self._getUserSubmission(userName=userName, verdict="Accepted", minTMP=lastSubUpdateTMP)
                if apiRes["found"] == True:
                    for i in apiRes["submission"]:
                        subs.append(i)
                apiRes = self._getUserSubmission(userName=userName, verdict="Rejected", minTMP=lastSubUpdateTMP)
                if apiRes["found"] == True:
                    for i in apiRes["submission"]:
                        subs.append(i)
                if len(subs) > 0:
                    self._updateSubmission(userName=userName, submissions=subs)
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%Y%m%d%H%M")
                    self._updateUserInfo(userInfo=self._getUserInfo(userName), lastSubUpdateTMP=formatted_time)
            Logger.retFunction("success")
            return True
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            return False
    
    def deleteUser(self, userName):
        Logger.callFunction()

        try: 
            item = self.db.executeSQL(sql=
                f'''
                    SELECT userName from cf_user
                    WHERE userName  = "{userName}"
                '''
            )
            if len(item) == 0:
                return False
            isRecord = True if item[0][0] == userName else False
            if isRecord == False:
                return False
            self.db.executeSQL(sql=
                f'''
                    DELETE FROM cf_user
                    WHERE userName = "{userName}"
                '''
            )
            self.db.executeSQL(sql=
                f'''
                    DELETE FROM cf_sub
                    WHERE userName = "{userName}"
                '''
            )
            Logger.retFunction("success")
            return True
        except Exception as e:
            Logger.retFunction("failed" + str(e))
            return False

