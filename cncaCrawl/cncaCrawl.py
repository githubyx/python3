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
sys.path.append(r"skclas.py")
import skclas


#爬虫操作
def getInfoByName(GCName,yzmCount):
    '''
    :param GCName: 公司名称获取公司
    :param yzmCount: 验证码错误重试次数
    :return: 公司信息 type：dict，是否成功获取信息
    '''
    url = 'http://cx.cnca.cn/rjwcx/checkCode/rand.do?d='
    sleeptime = random.uniform(5, 8)
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
    with open(r'temp\%s.gif' % name, 'ab') as f:
        f.write(checkFile)
    sum = skclas.countSum('%s.gif' % name)
    print(sum)
    datap = {
            "orgName":GCName,
             "queryType": "public",
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
            time.sleep(sleeptime)
            textdata = one_session.post('http://cx.cnca.cn/rjwcx/web/cert/list.do?progId=10', headers=headerd, data=dataCheck)
            detalis= textdata.json()['rows']
            return detalis,'1'

def getInfoByPage(i,yzmCount):
    '''

    :param i: 页编号
    :param yzmCount: 验证码错误重试次数
    :return:
    '''
    sleeptime=random.uniform(8, 12)
    url = 'http://cx.cnca.cn/rjwcx/checkCode/rand.do?d='
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Connection': 'keep-alive',
        'Cookies': r'''JSESSIONID=0000xSmM5HoK0jebjQAs2 - kuLCQ:-1;Hm_lvt_1ab04bcaf4dd6e15edf78188f2d6a32c=1523682215,1523682280,1523839936,1523841340;Hm_lpvt_1ab04bcaf4dd6e15edf78188f2d6a32c=1523841370'''
    }
    one_session = requests.Session()
    # html_data = one_session.get(url, headers=header).content
    checkFile = one_session.get(url, headers=header).content
    name = int(time.time() * 10)
    with open(r'temp\%s.gif' % name, 'ab') as f:
        f.write(checkFile)
    sum = skclas.countSum('%s.gif' % name)
    print (sum)
    #423792
    iso={'certItemOne': "A",
        'certItemTwo': "A01",
        'certItemThree': "A0101",
        'country': "156",
        'certStatus': "01",
        'queryType': "public",
        'checkCode': sum,
        'page': i,
        'rows': "100",
        }
    #189439
    hjgl = {
        'certItemOne': "A",
        'certItemTwo': "A02",
        'certItemThree': "A0201",
        'country': "156",
        'certStatus': "01",
        'queryType': "public",
        'checkCode': sum,
        'page': i,
        'rows': "100",

    }
    #147488
    zyjk = {'certItemOne': "A",
            'certItemTwo': "A03",
            'certItemThree': "A0301",
            'country': "156",
            'certStatus': "01",
            'queryType': "public",
            'checkCode': sum,
            'page': i,
            'rows': "100",
            }
    #6960
    xxaq = {'certItemOne': "A",
           'certItemTwo': "A05",
           'certItemThree': "A0501",
           'country': "156",
           'certStatus': "01",
           'queryType': "public",
           'checkCode': sum,
           'page': i,
           'rows': "100",
           }
    #3332
    xxjs = {'certItemOne': "A",
           'certItemTwo': "A06",
           'certItemThree': "A0601",
           'country': "156",
           'certStatus': "01",
           'queryType': "public",
           'checkCode': sum,
           'page': i,
           'rows': "100",
           }


    time.sleep(sleeptime)
    textdata = one_session.post('http://cx.cnca.cn/rjwcx/web/cert/list.do?progId=10', headers=header, data=iso)
    textjson=textdata.json()
    print (textjson)
    if textjson['success']==False:
        yzmCount = yzmCount -1
        print ('yzm error! remain: %s'%yzmCount)
        if yzmCount <= 0:
            return ['abc'], '-1'
        else:
            return getInfoByPage(i,yzmCount)
    else:
        data=textjson['rows']
        pageNo=textjson['pageNo']
        return data,pageNo

#excel操作
def write2Excel(values,excelName):
    '''
    读取excel 添加数据 没有该文件自动创建
    :param values:
    :param excelName:
    :return:
    '''
    if os.path.exists(excelName)==False:
        workbook = xlsxwriter.Workbook(excelName)
        workbook.add_worksheet('sheet1')
        workbook.close()
    time.sleep(1)
    rexcel = open_workbook(excelName)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    row = rows
    for value in values:
        table.write(row, 0, row)  # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 1, value['authProjCode'])
        table.write(row, 2, value['authProjCodeName'])
        table.write(row, 3, value['certAppshowFlag'])
        table.write(row, 4, value['certNumber'])
        table.write(row, 5, value['certOrderFlag'])
        table.write(row, 6, value['certiEDate'])
        table.write(row, 7, value['certiStatus'])
        table.write(row, 8, value['certiStatusName'])
        table.write(row, 9, value['checkC'])
        table.write(row, 10, value['orgName'])
        table.write(row, 11, value['rzjgId'])
        table.write(row, 12, value['rzjgIdName'])
        table.write(row, 13, value['zersda'])
        row += 1
    excel.save(excelName)
    print ("saved!:",len(values),'条记录')

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

#mysql操作
db = pymysql.connect('localhost', 'root', '123456', 'cnna', charset='utf8')
'''
CREATE TABLE `cnna` (
  `row` int(11) NOT NULL,
  `authProjCode` varchar(255) default NULL,
  `authProjCodeName` varchar(255) default NULL,
  `certNumber` varchar(255) default NULL,
  `certiEDate` varchar(255) default NULL,
  `certiStatus` varchar(255) default NULL,
  `certiStatusName` varchar(255) default NULL,
  `orgName` varchar(255) default NULL,
  `rzjgId` varchar(255) default NULL,
  `rzjgIdName` varchar(255) default NULL,
  `zersda` varchar(255) default NULL,
  PRIMARY KEY  (`row`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
def addCnna(row,authProjCode,authProjCodeName, certNumber, certiEDate, certiStatus, certiStatusName, orgName, rzjgId, rzjgIdName, zersda):

    try:
        cursor = db.cursor()
        sql = 'insert into cnna(row,authProjCode,authProjCodeName, certNumber, certiEDate, certiStatus, certiStatusName, orgName, rzjgId, rzjgIdName, zersda) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            row,authProjCode, authProjCodeName, certNumber, certiEDate, certiStatus, certiStatusName, orgName, rzjgId,
            rzjgIdName, zersda);  # 插入数据库的SQL语句
        cursor.execute(sql)
        db.commit()
    except Exception as  e:
        print (e)
        db.rollback()
def addCnnaAll(values):
    for value in values:
        row=value['row']
        authProjCode=value['authProjCode']
        authProjCodeName = value['authProjCodeName']
        certNumber = value['certNumber']
        certiEDate = value['certiEDate']
        certiStatus = value['certiStatus']
        certiStatusName = value['certiStatusName']
        orgName = value['orgName']
        rzjgId = value['rzjgId']
        rzjgIdName = value['rzjgIdName']
        zersda = value['zersda']
        addCnna(row,authProjCode, authProjCodeName, certNumber, certiEDate, certiStatus, certiStatusName, orgName, rzjgId,
                rzjgIdName, zersda)
'''
CREATE TABLE `error` (
  `className` varchar(255) NOT NULL default '',
  `errorNum` int(11) NOT NULL default '0',
  `errorType` varchar(255) default NULL,
  PRIMARY KEY  (`className`,`errorNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
def add_error(className,errorNum,errorType):
    try:
        cursor = db.cursor()
        sql = 'insert into error(className,errorNum,errorType) values ("%s","%d","%s")' % (className,
            errorNum,errorType);  # 插入数据库的SQL语句
        cursor.execute(sql)
        db.commit()
    except Exception as e :
        print (e)
        db.rollback()

#遍历页数获取公司信息 参数用于传数据库error的证书类型
def getByPage(strName):
    for i in range(3952,4240):
        try:
            detail,flage=getInfoByPage(i,3)
            if flage=='-1':
                add_errorAll(strName,i, "-1")
            else:
                addCnnaAll(detail)
                print ('numpage:%s' % i)
                add_errorAll(strName,i, flage)
        except BaseException as e:
            print  (e.message)
            add_errorAll(strName,i, "0")
#公司名称 爬虫 excel存储
def getGSByName(excelname):
    nofind=[]
    findl=[]
    errorl=[]
    with open(r'companyData/nx_company.txt',encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(0,len(lines)):
                try:
                    name=lines[i].strip()
                    print (r"正在获取%s :|%s|" % (i,name))
                    details,tar = getInfoByName(name,3)
                    if tar=='-1':
                        nofind.append(name)
                    else:
                        findl.append(name)
                        write2Excel(details,excelname)
                except Exception as  e:
                    print(e)
                    errorl.append(name)
    print(findl)
    print(nofind)
    print(errorl)
    writeExcelPandas(findl, 'excelData/find.xls')
    writeExcelPandas(nofind,'excelData/nofind.xls')
    writeExcelPandas(errorl, 'excelData/errorl.xls')
#页数 爬虫 mysql存储 需要修改data=后面的证书名称
def getbypage(strName):
    for i in range(1,4348):
        try:
            detail,flage=getInfoByPage(i,3)
            if flage=='-1':
                add_error(strName,i, "-1")
            else:
                addCnnaAll(detail)
                print ('numpage:%s' % i)
                add_error(strName,i, flage)
        except BaseException as  e:
            print  (e.message)
            add_error(strName,i, "0")

if __name__=='__main__':
    #getGSByName('excelData/excelName.xls')
    getByPage('iso')


