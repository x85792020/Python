import eel
import sys
import pymysql
import json
import datetime
import dateutil.relativedelta

db = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="sandy8686956",db="pethotel",charset='utf8')
cursor = db.cursor()
eel.init('web')
#建立訂單Model


@eel.expose
def getOrderDataPy(petName="",mode=""):

    sql = '''
        SELECT ord.order_id,pets.pet_name,ord.DATE, rooms.room_name,emp.empoloyee_name,price
        FROM pethotel.orders as ord
        join pethotel.pets as pets on ord.pet_id = pets.pet_id 
        join pethotel.empoloyees as emp on ord.employee_id = emp.empoloyee_id
        join pethotel.rooms as rooms on ord.room_id = rooms.room_id

    '''
    if petName !="":
        petNameArray = petName.split(',')
        convertArray = []
        for pet in petNameArray:
            convertPet = "'"+pet+"'"
            convertArray.append(convertPet)
        print(convertArray)
        convertArrayStr = ','.join(convertArray)
        print(convertArrayStr)
        if mode == 'IN' or mode == 'NOT IN':
            sql = sql + "WHERE pets.pet_name {0} ({1})".format(mode,convertArrayStr)
        else:
            sql = sql + '''
                WHERE {0} (
                select * from pethotel.pets as pets  where pets.pet_name IN ({1}) and ord.pet_id=pets.pet_id
                );
            '''.format(mode,convertArrayStr)
    print(sql)
    cursor.execute(sql) 
    # 取得所有資料
    result = cursor.fetchall()
    output = ""
    rawData = []
    for row in result:
        #創造物件
        data =  {
            "order_id": row[0],
            "pet_name": row[1],
            "date":row[2].strftime("%Y/%m/%d"),
            "room_name":row[3],
            "empoloyee_name":row[4],
            "price":row[5]
        }

        rawData.append(data)
    
    #將資料轉JSON
    jsonStr  = json.dumps(rawData)
    return jsonStr
@eel.expose
def getPetOptionPy():
    sql = 'SELECT * FROM pethotel.pets;' 
    cursor.execute(sql)
    # 取得所有資料
    result = cursor.fetchall()
    rawData = []
    for row in result:
        data =  {
            "text": row[1],
            "value": row[0],
        }
        rawData.append(data)
    #將資料轉JSON
    jsonStr  = json.dumps(rawData)
    return jsonStr
@eel.expose
def getEmployeeOptionPy():
    sql = 'SELECT * FROM pethotel.empoloyees;' 
    cursor.execute(sql)
    # 取得所有資料
    result = cursor.fetchall()
    rawData = []
    for row in result:
        data =  {
            "text": row[1],
            "value": row[0],
        }
        rawData.append(data)
    #將資料轉JSON
    jsonStr  = json.dumps(rawData)
    return jsonStr
@eel.expose
def getRoomOptionPy():
    sql = 'SELECT * FROM pethotel.rooms;' 
    cursor.execute(sql)
    # 取得所有資料
    result = cursor.fetchall()
    rawData = []
    for row in result:
        data =  {
            "text": row[1],
            "value": row[0],
        }
        rawData.append(data)
    #將資料轉JSON
    jsonStr  = json.dumps(rawData)
    return jsonStr

@eel.expose
def delOrderPy(order_id):
    successCode ='success'
    try:
        sql = 'DELETE FROM pethotel.orders WHERE order_id = '  + order_id
        cursor.execute(sql) 
        db.commit()
    except :
        successCode ='fail'
    return successCode
@eel.expose
def submitOrderDataPy(addOrEdit,submitData):
    #進行新增或編輯

    successCode = ''
    try:
        print(submitData)
        sql = ""
        if addOrEdit == "Add":
            sql = '''
            INSERT INTO pethotel.orders (pet_id, room_id, employee_id,date,price )
            VALUES ('{0}', '{1}','{2}', '{3}','{4}');
            '''.format(submitData["pet_id"],submitData["room_id"],submitData["employee_id"],submitData["date"],submitData["price"])
            successCode = '新增成功'
            print(sql)
        elif addOrEdit == "Edit":
            print('編輯')
            
            sql = '''
            UPDATE pethotel.orders
            SET pet_id = '{0}',DATE= '{1}',room_id='{2}',employee_id='{3}',price={4}
            WHERE order_id= {5};
            '''.format(submitData["pet_id"],submitData["date"],submitData["room_id"],submitData["employee_id"],submitData["price"],submitData["order_id"])

            successCode = '編輯完成'
            print(sql)
        cursor.execute(sql) 
        db.commit()
    except :
        successCode = '操作失敗,請重新進行操作!'
    return successCode
@eel.expose
def getOrderFormDataPy(order_id):
    sql = '''
        SELECT * 
        FROM pethotel.orders
        WHERE order_id = {0}
        '''.format(order_id)
    successCode =''
    try:
        cursor.execute(sql) 
        result = cursor.fetchall()
        rawData = []
        for row in result:
            data =  {
                "order_id": row[0],
                "pet_id": row[1],
                "date":row[2].strftime("%Y-%m-%d"),
                "room_id":row[3],
                "employee_id":row[4],
                "price":row[5]
            }
            rawData.append(data)
            result = cursor.fetchall()

    except :
        successCode = '私服器異常'
    output = {
        "successCode":successCode,
        "data":rawData
    }
    #將資料轉JSON
    jsonStr  = json.dumps(output)
    return jsonStr

#執行SQL的Function
@eel.expose
def runSQLPy(sql): 
    successCode ='success!'
    output = {}
    #取得欄位名稱
    columns = []
    message = ''
    #取得資料
    data =[]
    try:
        cursor.execute(sql)
        upperSQL = sql.upper()
        isTable = True
        if ("INSERT" in upperSQL) or ("UPDATE" in upperSQL) or ("DELETE" in upperSQL):
            print('commit')
            isTable = False
            if "INSERT" in upperSQL:
                message = 'INSERT SUCCESS!'
            elif ("UPDATE" in upperSQL):
                message = 'UPDATE SUCCESS!'
            elif ("DELETE" in upperSQL):
                message = 'DELETE SUCCESS!'
            db.commit()
        else:
            col_result = cursor.description
            for i in range(len(col_result)):
                columns.append(col_result[i][0])
            result = cursor.fetchall()
            for row in result:
                #每一筆資料
                rawData = []
                for colValue in row:
                    rawData.append(str(colValue))
                data.append(rawData)
        output = {
            "successCode":successCode,
            "isTable" : isTable,
            "msg": message,
            "columns":columns,
            "data":data
        }

    except  Exception as e:
        print('----------------------')
        print('繼續!')
        successCode = 'fail'
        output = {
            "successCode":successCode,
            "msg":str(e),

        }
    #將資料轉JSON
    jsonStr  = json.dumps(output)
    #print(jsonStr)
    return jsonStr

@eel.expose
def getTableInfoPy(tableName,target): 
    sql = ""
    columns = []
    if tableName == 'pets':
        sql = '''
            SELECT p.pet_id,p.pet_name,p.variety,p.birthday,o.owner_name FROM pethotel.pets as p
            join pethotel.owner as o on o.owner_id = p.owner_id;
        '''
        columns = ['寵物編號','名稱','品種','生日','主人名稱']
    elif tableName == 'rooms':
        sql = '''
            SELECT room_id,room_name,room_discript
            FROM pethotel.rooms;
        '''
        columns = ['房間編號','房間名稱','房間描述']
    elif tableName == 'owner':
        sql = '''
            SELECT OWNER_ID,OWNER_NAME,OWNER_ADDRESS,OWNER_PHONE
            FROM pethotel.owner;
        '''
        columns = ['客戶編號','客戶名稱','客戶地址','連絡電話']
    elif tableName == 'hospital':
        sql = '''
            SELECT hospital_id,hospital_name,hospital_address,hospital_phone
            FROM pethotel.hospital;
        '''
        columns = ['醫院編號','醫院名稱','醫院地址','連絡電話']
    elif tableName == 'employees':
        sql = '''
            SELECT empoloyee_id,empoloyee_name,empoloyee_phone,department_id
            FROM pethotel.empoloyees;
        '''
        columns = ['員工編號','員工名稱','員工手機','部門代號'] 
    #取得資料
    data =[]
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        #每一筆資料
        rawData = []
        for colValue in row:
            rawData.append(str(colValue))
        data.append(rawData)
    output = {
        "columns":columns,
        "data":data,
        "target":target
    }
    #將資料轉JSON
    jsonStr  = json.dumps(output)
    return jsonStr

@eel.expose
def getOraderMonthRankPy(year,month,day):
    date = datetime.date(int(year),int(month),int(day))
    print(str(date))
    
    Nextdate = date +  dateutil.relativedelta.relativedelta(months=1)
    print(str(Nextdate))
    sql = '''
        SELECT employee_id,employee_name,count(employee_id) orderCount
        FROM (
            SELECT emp.empoloyee_id employee_id,emp.empoloyee_name employee_name,ord.order_id order_id,emp.empoloyee_id empoloyee_id,ord.DATE
            FROM pethotel.orders as ord
            join pethotel.empoloyees as emp on ord.employee_id = emp.empoloyee_id
            WHERE ord.DATE >= '{0}' and ord.DATE <'{1}'
        ) AS t
        group by empoloyee_id
        HAVING orderCount >= 3
        ORDER BY orderCount DESC;
    '''.format(date,Nextdate)
    #會得到12月 排名 前五名
    cursor.execute(sql)

    result = cursor.fetchall()
    dataList= []
    for row in result:
        data = {
            "employee_id" : str(row[0]),
            "emplyee_name":str(row[1]),
            "order_count": str(row[2])
        }
        dataList.append(data)
    jsonStr  = json.dumps(dataList)
    return jsonStr

@eel.expose
def getCalculatePy(selectOption):
    sql = ''
    if selectOption == 'COUNT':
        #訂單數量
        sql = 'SELECT count(*) COUNT FROM pethotel.orders;'
    elif selectOption == 'SUM':
        #目前訂單總入住金額
        sql = 'SELECT sum(price) SUM FROM pethotel.orders;'
    elif selectOption == 'AVG':
        #平均訂單入住金額
        sql = 'SELECT avg(price) AVG FROM pethotel.orders;'
    elif selectOption == 'MAX':
        #訂單最高入住金額
        sql = 'SELECT max(price) MAX FROM pethotel.orders;'
    elif selectOption == 'MIN':
        #訂單最低入住金額
        sql = 'SELECT min(price) MIN FROM pethotel.orders;'
    #取得資料
    data =[]
    columns = []
    cursor.execute(sql)
    col_result = cursor.description
    for i in range(len(col_result)):
        columns.append(col_result[i][0])
    result = cursor.fetchall()
    for row in result:
        #每一筆資料
        rawData = []
        for colValue in row:
            rawData.append(str(colValue))
        data.append(rawData)
    output = {
        "columns":columns,
        "data":data,
    }
    print(output)
    #將資料轉JSON
    jsonStr  = json.dumps(output)
    return jsonStr

eel.start('order.html')


