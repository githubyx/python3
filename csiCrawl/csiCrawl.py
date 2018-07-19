from selenium import webdriver
import time
from xlrd import open_workbook
from xlutils.copy import copy
import random

#读取excel 添加数据 一行
def writeExcelDemo(values,excelName):
    rexcel = open_workbook(excelName)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    row = rows
    print (row)
    for i in range(len(values)):
        table.write(row, i, values[i])  # xlwt对象的写方法，参数分别是行、列、值
    excel.save(excelName)
    print ("saved!")
#获取数据存excel
def get_messageDemo(browser,excelName):
    sleeptime = random.uniform(3, 6)
    time.sleep(sleeptime)
    data = browser.find_elements_by_xpath('//*[@id="tablelist"]/tbody/tr')
    # meslist=[i.text for i in data]
    for i in range(1, len(data)):
        mes = data[i].text
        mesl = mes.split(' ')
        # print(mesl)
        writeExcelDemo(mesl,excelName)

#读取excel 添加数据 50行
def writeExcel50(data,excelName):
    rexcel = open_workbook(excelName)  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    print("从行%d开始获取50条"%rows)
    row = rows
    for j in range(1, len(data)):

        mes = data[j].text
        values = mes.split(' ')
        for i in range(len(values)):
            table.write(row, i, values[i])  # xlwt对象的写方法，参数分别是行、列、值
        row+=1
    excel.save(excelName)
    print ("saved!")
#爬取数据 写入excel 添加数据 50行
def get_message50(browser,excelName):
    sleeptime = random.uniform(3, 6)
    time.sleep(sleeptime)
    data = browser.find_elements_by_xpath('//*[@id="tablelist"]/tbody/tr')
    # meslist=[i.text for i in data]
    writeExcel50(data,excelName)

#浏览器点击下一页
def clickNext(browser):
    next=browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div/div/a[3]")
    # next = browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div/div/a[3]")
    print(next)
    next.click()
    return browser



def main():
    driver = webdriver.Firefox()
    url = "http://www.csi-s.org.cn/miitnew_webmap/miitnew_jcqycx/"
    driver.get(url)
    time.sleep(5)
    for i in range(0,257):#247
        get_message50(driver,'csi20180703.xls')
        #浏览器点击下一页
        next = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div/div/a[3]")
        next.click()
    driver.close()
if __name__ == '__main__':
    main()







