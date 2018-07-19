#coding=utf-8

import os
import pandas as pd

from xlrd import open_workbook
from xlutils.copy import copy

excel_path = 'cmmi20180703temp.xlsx'
df = pd.read_excel(excel_path,sheet_name=None)
df2 = df['Sheet1'].copy()
print(df2.head())
df3=df2.dropna(how='any')
print(df3)
#处理保存为 cmmi20180703.xlsx
df3.to_excel('cmmi20180703.xlsx')
