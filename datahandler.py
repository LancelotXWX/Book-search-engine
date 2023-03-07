'''
实现数据处理和搜索部分
'''

import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

#清理图书数据的函数
def cleandata(file):
    dd0 = pd.read_excel(file)   #打开excel文件，并把其存为dataframe
    dd1 = dd0.fillna(value= "No information available")    #填充空缺位置
    dd2 = dd1.drop_duplicates(subset = ['cn_title'],keep = 'first',inplace = False)    #删除重复书籍信息

    
    dd2 = dd2.copy()
    dd2.loc[dd2['price'] == 0,'price'] = 'unknown'        #把未知的price设为unknown
    dd2.loc[dd2['page_num'] == 0,'page_num'] = 'unknown'  #把未知的页数设为unkwown
    return dd2

#存历史记录的函数
def savehistory(record):
    with open('history.txt','r+') as f:
        f.read()
        f.write(record + "\n")

#获取excel文档内容的函数
def getdata(file):
    datatable = pd.read_excel(file)
    return datatable
    
#返回文本匹配值用于排序
def getmatch(a,b):
    return fuzz.partial_ratio(a,b)

#存储清理好的数据
def savedata(table):
    table.to_excel('清理后的数据.xlsx',sheet_name = 'cleaned book_info')  #把处理好的数据放到新的excel表格里

#在数据里进行检索的函数
def search(table,ms):
    listofdata = table.values.T.tolist()
    listofindex = table.columns.tolist()
    dlist = []
    for i in range(0,11):
                if ms in listofdata[i] :
                    listofsearch = table.loc[table[listofindex[i]] == ms].values.T.tolist()
                    dlist = []
                    colnum = len(listofsearch)
                    rownum = len(listofsearch[1])
                    tempdata = []
                    for i in range(0,rownum):
                        for j in range(0,colnum):
                            tempdata.append(listofsearch[j][i])
                        tempd = dict(zip(listofindex,tempdata))
                        dlist.append(tempd)
                        tempdata = []
    return dlist

#实现模糊搜索的函数
def titlesearch(table,ms):
    listofdata = table.values.T.tolist()
    listofname = listofdata[2]
    listofindex = table.columns.tolist()
    dlist = []
    for i in listofname:
        tempjudge = fuzz.partial_ratio(ms,i)
        if tempjudge >= 60:
            listofsearch = table.loc[table['cn_title'] == i].values.T.tolist()
            colnum = len(listofsearch)
            rownum = len(listofsearch[1])
            tempdata = []
            for i in range(0,rownum):
                for j in range(0,colnum):
                    tempdata.append(listofsearch[j][i])
                tempd = dict(zip(listofindex,tempdata))
                dlist.append(tempd)
                tempdata = []
    
    return dlist



