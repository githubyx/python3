#coding=utf-8
import requests

import time
import pandas as pd

import os
import pandas as pd
import sys
import json
import random
from xlrd import open_workbook
from xlutils.copy import copy

import pandas as pd


#对数据进行处理 选取5种证书
excel_path = 'company_find_add.xls'
df = pd.read_excel(excel_path,sheet_name=None)
df2 = df['Sheet1'].copy()
#5家证书编号
df3=df2.loc[df2['authProjCode'].isin(['A010101','A010102','A010103', 'A020101','A020102','A020103','A050101','A050102','A050103','A060101','A060102','A060103','A030101','A030102','A030103'])]
#选择有效的证书
df4=df3.loc[df3["certiStatus"] ==1]
# df4=df3['certiStatus']=='1'
df4.to_excel('company__add.xls')



# df3.to_excel('excelPro.xls')

