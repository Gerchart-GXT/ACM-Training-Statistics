from component.browser import Browser
from component.database import SqlLite
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import logging

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
    def __init__(self, urlPath, browser:Browser):
        self.browser=browser
        with open(file=urlPath, mode="r") as file:
            self.urls = json.load(file)
        self.urls = self.urls["codeforces"]

        self.db = SqlLite("codeforces.db")
        self.db.executeSQL(sql=
            '''            
                CREATE TABLE IF NOT EXISTS cf_user (
                    userName TEXT PRIMARY KEY,
                    isOnline TEXT,
                    lastLoginUpdateTMP TEXT,
                    lastSubUpdateTMP TEXT
                );
            '''
        )
        self.db.executeSQL(sql=
            '''            
                CREATE TABLE IF NOT EXISTS cf_sub (
                    userName TEXT,
                    subTMP TEXT,
                    subID TEXT PRIMARY KEY,
                    proPath TEXT,
                    status TEXT,
                    FOREIGN KEY (userName) REFERENCES cf_user(userName) ON DELETE CASCADE
                );
            '''
        )
        logging.info("Codeforces Init Finish")
    
    def _getUserInfo(self, userName):
        url="https://" + self.urls["sni"] + self.urls["user"]["home"] + "/" + userName
        self.browser.openPage(url)
        logging.info("_getUserInfo:" + url)

        try:
            if self.browser.driver.current_url != url:  
                raise Exception("User Not Found")
            if self.browser.getElement(css=".userbox .main-info > h1").text != userName:
                raise Exception("Name Not Match")
            
            infos = self.browser.getElement(css=".userbox > .info > ul").find_elements(By.CSS_SELECTOR, "li")
            rankLine=infos[0].text.split(' ')
            loginLine = infos[3].text.split(' ')
            logging.info("_getUserInfo Success")

            return {
                    "userName":userName,
                    "found": True,
                    "rank": {
                        "current": rankLine[2], 
                        "max": rankLine[len(rankLine) - 1][:-1]
                    },
                    "loginStatus": True if loginLine[2] == "online" else False
            }
        except Exception as e:
            logging.info("_getUserInfo Failed" + str(e))
            return {
                "userName":userName,
                "found": False
            }

    def _getUserSubmission(self, userName, verdict, minTMP):
        if self._getUserInfo(userName=userName)["found"] != True:
            return {
                "userName": userName,
                "found": False,
            }
        
        url="https://" + self.urls["sni"] + self.urls["user"]["submission"] + "/" + userName
        try:
            logging.info("_getUserSubmission:" + url)
            self.browser.openPage(url)

            verdictSelector=Select(self.browser.getElement(css="form.status-filter select[id='verdictName']"))
            verdictSelector.select_by_visible_text(text=verdict)
            self.browser.getElement(css="form.status-filter input[value='Apply']").click()

            pageCount = 1
            for i in self.browser.getElements(css=".page-index"):
                pageCount = max(pageCount, int(i.text))

            subs={}

            outDated = False
            for _ in range(pageCount):
                infos = (self.browser.getElement("div.datatable table.status-frame-datatable")).find_elements(By.CSS_SELECTOR, "tr")
                infos = infos[1:]
                for line in infos:
                    lineItems = line.find_elements(By.CSS_SELECTOR, "td")
                    subID = lineItems[0].text

                    subTMP = lineItems[1].text.split(' ')
                    subDate = subTMP[0].split('/')
                    subDate[0] = MONTH[subDate[0]]
                    subTime = (subTMP[1][0:2], subTMP[1][3:5])
                    subTMP = f"{subDate[2]}{subDate[0]}{subDate[1]}{subTime[0]}{subTime[1]}"

                    if subTMP < minTMP:
                        outDated = True
                        break
                    proPath = lineItems[3].find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                    subs[proPath] = (subID, subTMP)
                if outDated == True:
                    break
                if _ + 1 < pageCount:
                    self.browser.getElement(f"a[href='/submissions/{userName}/page/{_ + 2}']").click()

        except Exception as e:
            logging.info("_getUserSubmission Failed" + str(e))
            return {
                "userName": userName,
                "found": False,
            }
        logging.info("_getUserSubmission Success")
        return {
            "userName": userName,
            "found": True if len(subs) > 0 else False,
            "submission": [{
                "userName":userName, 
                "proPath": key, 
                "subID":value[0], 
                "subTMP":value[1],
                "status": verdict
            } for key, value in subs.items()]
        }
        
    def _updateUserInfo(self, userInfo, lastSubUpdateTMP):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y%m%d%H%M")
        self.db.executeSQL(sql=
            f'''
                INSERT OR REPLACE INTO cf_user (userName, isOnline, lastSubUpdateTMP, lastLoginUpdateTMP) 
                VALUES ("{userInfo["userName"]}", "{1 if userInfo["loginStatus"] == True else 0}", "{lastSubUpdateTMP}", "{formatted_time}");
            '''
        )

    
    def _updateSubmission(self, userName, submissions):
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
        

    def insertUser(self, userName):
        apiRes = self._getUserInfo(userName=userName)
        if apiRes["found"] == False:
            return False
        self._updateUserInfo(userInfo=apiRes, lastSubUpdateTMP=INITTMP)
        return True

    def updateUsersLogin(self):
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
        except Exception as e:
            print(e)
            return False
        return True

    def updateUsersSub(self, verdict, minTMP=None):
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
                apiRes = self._getUserSubmission(userName=userName, verdict=verdict, minTMP=lastSubUpdateTMP)
                if apiRes["found"] == True:
                    self._updateSubmission(userName=userName, submissions=apiRes["submission"])
        except Exception as e:
            print(e)
            return False
        return True
    
    def deleteUser(self, userName):
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
        except Exception as e:
            print(e)
            return False
        return True

