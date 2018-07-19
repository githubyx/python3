import pymysql

db = pymysql.connect('localhost', 'root', '123456', 'credit', charset='utf8')
def selectSql(orgNamea):
    info={}
    cursor = db.cursor()
    cursor.execute('select * from nx_reptile_management_system where orgName=%s',orgNamea)
    rowall = cursor.fetchall()
    lista=[]
    n=''
    for r in rowall:
        print(r[7],r[2])
        lista.append(r[2])
        n=r[7]
    info[n]=lista
    db.commit()
    cursor.close()
    return info



# ss=selectSql('南京恒星自动化设备有限公司')
# print(ss)
# print(ss['南京恒星自动化设备有限公司'])

with open(r'companyData/nx_company_add3.txt', encoding='utf-8') as f:
    lines = f.readlines()
    lisInfo=[]
    for i in range(0, len(lines)):
        name = lines[i].strip()
        info=selectSql(name)
        lisInfo.append(info)
    print(lisInfo)