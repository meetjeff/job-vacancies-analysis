from flask_apispec import doc, MethodResource
import requests
import json

import pymysql

def db_init():
    db = pymysql.connect(
        host='azsqltop.mysql.database.azure.com',
        user='jeff',
        password='@a0987399832',
        port=3306,
        database='career'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


class trigger(MethodResource):

    @doc(description="選擇爬取網站，並輸入搜索關鍵字與爬取頁數", tags=['Crawler'])
    def get(self,website,search,page):
        try:
            url = requests.get(f"https://yourator.azurewebsites.net/api/orchestrators/crawlers?website={website}&search={search}&page={page}").json()["statusQueryGetUri"]

            db, cursor = db_init()
            cursor.execute(f"UPDATE career.statusurl SET url = '{url}' WHERE web = '{website}';")
            db.commit()
            cursor.close()
            db.close()
            
            res = f"已啟動{website}網站爬蟲(搜索關鍵字:{search},爬取頁數:{page}頁)"
        
        except:
            res = requests.get(f"https://yourator.azurewebsites.net/api/orchestrators/crawlers?website={website}&search={search}&page={page}").text
            
        return res


class status(MethodResource):
    
    @doc(description="追蹤爬蟲執行狀態", tags=['Crawler'])
    def get(self,website):
        try:
            db, cursor = db_init()
            cursor.execute(f"SELECT url FROM career.statusurl where web = '{website}';")
            url = cursor.fetchone()['url']
            db.commit()
            cursor.close()
            db.close()
        
            sta = requests.get(url).json()
            re={'爬取網站':website,'開始時間':sta['createdTime'],'執行狀態':sta['runtimeStatus'],'更新時間':sta['lastUpdatedTime'],'執行結果':sta['output'],'狀態網址':url}
            # s=f"爬取網站:{website}<br/>開始時間:{sta['createdTime']}\r\n執行狀態:{sta['runtimeStatus']}\\n更新時間:{sta['lastUpdatedTime']}\n執行結果:{sta['output']}\n狀態網址:{url}"
            return re
        except:
            return "請輸入爬蟲網站"

class skill(MethodResource):
    
    @doc(description="以技能查詢職缺資料", tags=['Skill'])
    def get(self,skill,records):

        db, cursor = db_init()
        cursor.execute(f"SELECT job,location,salary,company,education,skill FROM career.newjob where skill like '%{skill}%' collate utf8mb4_general_ci limit {records};")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        return data

class location(MethodResource):
    
    @doc(description="以城市查詢職缺資料", tags=['Location'])
    def get(self,location,records):

        db, cursor = db_init()
        cursor.execute(f"SELECT job,location,salary,company,education,skill FROM career.newjob where location like '%{location}%' collate utf8mb4_general_ci limit {records};")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        return data

class jobtitle(MethodResource):
    
    @doc(description="以關鍵字查詢職缺資料", tags=['Jobtitle'])
    def get(self,jobtitle,records):

        db, cursor = db_init()
        cursor.execute(f"SELECT job,location,salary,company,education,skill FROM career.newjob where job like '%{jobtitle}%' collate utf8mb4_general_ci limit {records};")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        return data

class enterprise(MethodResource):
    
    @doc(description="以企業查詢職缺資料", tags=['Enterprise'])
    def get(self,enterprise,records):

        db, cursor = db_init()
        cursor.execute(f"SELECT job,location,salary,company,education,skill FROM career.newjob where company like '%{enterprise}%' collate utf8mb4_general_ci limit {records};")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        return data

class salary(MethodResource):
    
    @doc(description="以薪資查詢職缺資料", tags=['Salary'])
    def get(self,salary,records):

        db, cursor = db_init()
        cursor.execute(f"SELECT job,location,salary,annualsalary,company,education,skill FROM career.newjob where annualsalary > {salary} ORDER BY annualsalary limit {records};")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        return data

class website(MethodResource):
    
    @doc(description="以平台查詢職缺資料", tags=['Website'])
    def get(self,website,records):

        db, cursor = db_init()
        cursor.execute(f"SELECT job,location,salary,annualsalary,company,education,skill FROM career.newjob where website = '{website}' limit {records};")
        data = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        return data

        
