#coding=utf-8
import requests
import time
import pandas as pd
import os
import sys
import random
from xlrd import open_workbook
import xlsxwriter
from xlutils.copy import copy
import pymysql
import time
sys.path.append(r"skclas.py")
import skclas

def writeExcelPandas(lista, filename):
    '''
    使用pandas，将全部公司基本信息写入excel 自动生成excel文件
    :param lista:
    :param filename:
    :return:
    '''
    df = pd.DataFrame(lista)
    if os.path.exists(filename):
        path = os.path.join(os.path.abspath('.'), filename)
        os.remove(path)
        df.to_excel(filename)
    else:
        df.to_excel(filename)
    print (u'写入%s文件成功' % filename)

# def selectSql(dateString):
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM `nx_reptile_management_system` where certiEDate<%s',dateString)
#     rows = cursor.fetchall()
#     print (rows[0])
#     return rows
#     # for row in rows:
#     #     print(row)
#
# def updateSql(info):
#     try:
#         cursor = db.cursor()
#         sql = 'UPDATE nx_reptile_management_system SET authProjCode = "%s",certNumber = "%s",certiEDate = "%s",rzjgId = "%s",rzjgIdName = "%s",zersda="%s"  WHERE authProjCodeName = "%s"  and  orgName = "%s"' % (info['authProjCode'],info['certNumber'],info['certiEDate'],info['rzjgId'],info['rzjgIdName'],info['zersda']);  # 插入数据库的SQL语句
#         cursor.execute(sql)
#         db.commit()
#     except BaseException as e:
#         print(e)
#         db.rollback()

def getInfoByName(GCName,yzmCount):
    '''
    :param GCName: 公司名称获取公司
    :param yzmCount: 验证码错误重试次数
    :return: 公司信息 type：dict，是否成功获取信息
    '''
    url = 'http://cx.cnca.cn/rjwcx/checkCode/rand.do?d='
    sleeptime = random.uniform(3, 7)
    headerd = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        'Connection': 'keep-alive',
        'Cookies': r'''JSESSIONID=0000gOXBaRd_LpTc6rYB0N184ng:-1; Hm_lvt_1ab04bcaf4dd6e15edf78188f2d6a32c=1530666281,1530691786,1530693043,1530694236; Hm_lpvt_1ab04bcaf4dd6e15edf78188f2d6a32c=1530694628'''
    }
    one_session = requests.Session()
    # one_session.headers=headerd
    # html_data = one_session.get(url, headers=header).content
    checkFile = one_session.get(url, headers=headerd).content
    name = int(time.time() * 10)
    with open(r'temp/%s.gif' % name, 'ab') as f:
        f.write(checkFile)
    sum = skclas.countSum('%s.gif' % name)
    print(sum)
    datap = {
            "orgName":GCName,
             "queryType": "public",
             "certItemOne": "A",
             "checkCode": sum}
    time.sleep(sleeptime)
    r = one_session.post('http://cx.cnca.cn/rjwcx/cxAuthenticationResult/queryOrg.do?progId=10',headers=headerd, data=datap)
    jsonCheck = r.json()
    if jsonCheck['success']==False:
        yzmCount = yzmCount -1
        print("----错误信息----：", jsonCheck['msg'])
        print ('验证码 error! remain: %s'%yzmCount)
        if yzmCount <= 0:
            return ['abc'], '0'
        else:
            return getInfoByName(GCName,yzmCount)
    else:
        print('验证码正确!')
        if len(jsonCheck['data'])<=0 :
            print('没找到该公司信息')
            return [],'-1'
        else:
            orgName = jsonCheck['data'][0]['orgName']
            orgCode = jsonCheck['data'][0]['orgCode']
            checkC = jsonCheck['data'][0]['checkC']
            randomCheckCode = jsonCheck['data'][0]['randomCheckCode']
            dataCheck = {'orgName': orgName,
                         'orgCode': orgCode,
                         'method': "queryCertByOrg",
                         'needCheck': "false",
                         'checkC': checkC,
                         'randomCheckCode': randomCheckCode,
                         'queryType': "public",
                         'page': "1",
                         'rows': "10",
                         'Cache-Control': "no-cache",
                         }
            time.sleep(random.uniform(1, 3))
            textdata = one_session.post('http://cx.cnca.cn/rjwcx/web/cert/list.do?progId=10', headers=headerd, data=dataCheck)
            detalis= textdata.json()['rows']
            return detalis,'1'


def selectSql(dateString):
    db = pymysql.connect('localhost', 'root', '123456', 'credit', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    with db.cursor()as cursor:
        cursor.execute('SELECT * FROM `nx_reptile_management_system` where certiEDate<%s and certiStatus=%s',(dateString,'2'))
        rows = cursor.fetchall()
    db.close()
    return rows

    # for row in rows:
    #     print(row)

def updateSql(info):
    db = pymysql.connect('localhost', 'root', '123456', 'credit', charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with db.cursor()as cursor:
            sql = 'UPDATE nx_reptile_management_system SET authProjCode = "%s",certNumber = "%s",certiEDate = "%s",rzjgId = "%s",rzjgIdName = "%s",zersda="%s",certiStatus="%s",certiStatusName="%s"  WHERE authProjCodeName = "%s"  and  orgName = "%s"' % (info['authProjCode'],info['certNumber'],info['certiEDate'].replace('-',''),info['rzjgId'],info['rzjgIdName'],info['zersda'].replace('-',''),info['certiStatus'],info['certiStatusName'],info['authProjCodeName'],info['orgName']);  # 插入数据库的SQL语句
            cursor.execute(sql)
        db.commit()
    except BaseException as e:
        print(e)
        db.rollback()
    finally:
        db.close()


def main():
    dateString = str(time.strftime("%Y%m%d", time.localtime()))
    print("当前时间格式化后：", dateString)
    datasInvalid=selectSql(dateString)
    nofind=[]
    findl=[]
    errorl=[]
    print(len(datasInvalid))
    for dataInvalid in datasInvalid:
        try:
            dataInvalidT = dataInvalid
            dataInvalidT['certiStatus'] = '3'
            updateSql(dataInvalidT)
            print(dataInvalid['orgName'], dataInvalid['authProjCodeName'], '修改状态certiStatus为3')
            details,tar=getInfoByName(dataInvalid['orgName'].replace('（','(').replace('）',')'), 3)
            if tar == '-1':
                nofind.append(dataInvalid['orgName'])
            else:
                findl.append(dataInvalid['orgName'])
                # print(details)
                for detail in details:
                    if detail['orgName']==dataInvalid['orgName'] and detail['authProjCodeName']==dataInvalid['authProjCodeName'] and detail['certiStatus']=='01':
                        updateSql(detail)
                        print(dataInvalid['orgName'],dataInvalid['authProjCodeName'],'更新成功！')
                    else:
                        pass

            print()
        except Exception as  e:
            print(e)
            errorl.append(dataInvalid['orgName'])

    writeExcelPandas(findl, 'excelData/find.xls')
    writeExcelPandas(nofind, 'excelData/nofind.xls')
    writeExcelPandas(errorl, 'excelData/errorl.xls')


main()
# getInfoByName('上海奈那卡斯电子配件有限公司', 3)
