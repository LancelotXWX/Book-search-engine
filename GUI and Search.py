'''
GUI和serch部分代码，此文件完成的是GUI界面显示以及一些搜索和排序功能的实现
'''
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import datahandler
import jieba
import os

nowpath = os.path.abspath(__file__)
fatherpath = os.path.dirname(nowpath)
datapath = fatherpath + "/清理后的数据.xlsx"
table = datahandler.getdata(datapath)
tindex = table.columns.tolist()
stopwords = ['的',' ','又','啊','系列','嗯']
sortdata = []
textsortlist = []
root = Tk(className = "宇芯图书搜索引擎")
root.geometry('670x400')

#定义用于搜索的函数
def search():
    keywords = entry_key.get()
    typekey = entry_type.get()
    listbox.delete(0,END)
    
    if not keywords:
        tkinter.messagebox.showerror('错误提示', '未输入查找的内容')     #若用户未输入查找的内容则报错
   
    elif typekey == "书名":
        datahandler.savehistory(keywords)
        splitwords = jieba.lcut_for_search(keywords)                   #对用户输入的查找文本进行分词操作
        savewords = []
        for x in range(0,len(splitwords)):
            if splitwords[x] not in stopwords:
                savewords.append(splitwords[x])
        for y in range(0,len(savewords)):
            Aresult = datahandler.titlesearch(table,savewords[y])
            lengthA = len(Aresult)
            colornum = 0
            for i in range(0,lengthA):
                apiece = Aresult[i]
                dvalue = list(apiece.values())
                for m in range(0,len(dvalue)):
                    dvalue[m] = str(dvalue[m])
                content = ""
                textsortlist.append(dvalue[2])
                for k in range(1,len(dvalue)):
                    content = content + tindex[k] + ": " + dvalue[k] + "  "
                listbox.insert(END,content)
                sortdata.append(content)
                if colornum & 2 == 0:
                    listbox.itemconfig('end',bg='yellow')
                colornum += 2

    else:
        datahandler.savehistory(keywords)
        Bresult = datahandler.search(table,keywords)
        lengthB = len(Bresult)
        colornum = 0
        for j in range(0,lengthB):
            apiece = Bresult[j]
            dvalue = list(apiece.values())
            for m in range(0,len(dvalue)):
                dvalue[m] = str(dvalue[m])
            
            content = ""
            textsortlist.append(dvalue[2])
            for k in range(1,len(dvalue)):
                content = content + tindex[k] + ": " + dvalue[k] + "  "
            
            listbox.insert(END,content)
            sortdata.append(content)
            if colornum & 2 == 0:
                listbox.itemconfig('end',bg='yellow')
            colornum += 2
    

#定义查询搜索历史记录的函数
def readhistory():
    historypath = fatherpath + '/history.txt'
    with open(historypath) as f:
        lines = f.readlines()
    printcontent = ""
    for i in range(0,len(lines)):
        printcontent = printcontent + lines[i] + "\n"
    showhistory = Tk(className='您的搜索历史记录')
    showhistory.geometry('800x400')
    hText = Text(showhistory, width=1000)
    hText.grid(row=0, column=0)
    hText.insert(END, printcontent)
    


# 搜索结果：左键双击打开（用在listbox)
def click1(event):
    index = listbox.curselection()  # 查看获取的列表索引
    if index == ():
        tkinter.messagebox.showerror('错误提示', '没有找到相关的书籍，您有可能输错了')
        return
    getcontent = listbox.get(index)
    contentlist = getcontent.split("  ")
    
    try:
        printcontent = ""
        for i in range(0,len(contentlist)):
            printcontent = printcontent + contentlist[i] + "\n"
    
    
    except:
        tkinter.messagebox.showerror('错误提示', '该搜索结果无法显示')
    else:
        showFile = Tk(className='查看完整信息')
        showFile.geometry('1000x400')
        fileText = Text(showFile, width=1000)
        fileText.grid(row=0, column=0)
        fileText.insert(END, printcontent)




#按照信息质量排序
def smartsort():
    listbox.delete(0, END)
    sorteddata = sorted(sortdata,key=len)
    colornum = 0
    for i in range(0,len(sorteddata)):
        listbox.insert(END,sorteddata[i])
        if colornum & 2 == 0:
            listbox.itemconfig('end',bg='yellow')
        colornum += 2

#文本匹配度排序
def textsort():
    keywords = entry_key.get()
    listbox.delete(0, END)
    matchnum = []
    sorteddata = []
    for p in range(0,len(sortdata)):
        sorteddata.append(sortdata[p])
    for i in range(0,len(textsortlist)):
        matchnum.append(datahandler.getmatch(keywords,textsortlist[i]))
    for j in range(0,len(matchnum)):
        for k in range(0,len(matchnum) - 1 - j):
            if matchnum[k] < matchnum[k + 1]:
                matchnum[k],matchnum[k + 1] = matchnum[k + 1],matchnum[k]
                sorteddata[k],sorteddata[k + 1] = sorteddata[k + 1],sorteddata[k]
    colornum = 0
    for n in range(0,len(sortdata)):
        listbox.insert(END,sorteddata[n])
        if colornum & 2 == 0:
            listbox.itemconfig('end',bg='yellow')
        colornum += 2

#价格升序排序
def pricesort():
    listbox.delete(0,END)
    sorteddata = []
    pricedata = []
    for i in range(0,len(sortdata)):
        sorteddata.append(sortdata[i])
    for j in range(0,len(sorteddata)):
        tempstring = sorteddata[j].split("  ")
        tempprice = tempstring[6]
        pricedata.append(tempprice[7:])
    for k in range(0,len(pricedata)):
        try:
            if pricedata[k] == "unknown":
                pricedata[k] = 999999999999
            else:
                pricedata[k] = float(pricedata[k])
        except ValueError:
            pricedata[k] = 99
    for m in range(0,len(pricedata)):
        for n in range(0,len(pricedata) - m - 1):
            if pricedata[n] > pricedata[n + 1]:
                pricedata[n],pricedata[n + 1] = pricedata[n + 1],pricedata[n]
                sorteddata[n],sorteddata[n + 1] = sorteddata[n + 1],sorteddata[n]
    colornum = 0           
    for l in range(0,len(sorteddata)):
        listbox.insert(END,sorteddata[l])
        if colornum & 2 == 0:
            listbox.itemconfig('end',bg='yellow')
        colornum += 2

#刷新用到的数据
def again():
    sortdata.clear()
    textsortlist.clear()

#利用treeview来以表格形式展示搜索结果
def blockshow():
    showblock = Tk(className='您选择以表格形式展示结果')
    showblock.geometry('600x400')
    # 搜索结果：左键双击打开（用在treeview)
    def click2(event):
        index = block.focus()  # 查看获取的表格索引
        if index == ():
            tkinter.messagebox.showerror('错误提示', '没有找到相关的书籍，您有可能输错了')
            return
        getcontent = block.set(index)
    
        try:
            printcontent = ""
            getcontentk = list(getcontent.keys())
            getcontentv = list(getcontent.values())
            for i in range(0,len(getcontent)):
                printcontent = printcontent + getcontentk[i] + ": " + getcontentv[i] + "\n"
        except:
            tkinter.messagebox.showerror('错误提示', '该搜索结果无法显示')
        else:
            showFile = Tk(className='查看完整信息')
            showFile.geometry('1000x400')
            dataText = Text(showFile, width=1000)
            dataText.grid(row=0, column=0)
            dataText.insert(END, printcontent)
    block = ttk.Treeview(showblock,columns=('isbn13编号','中文名','英文名','作者','译者','出版社','价格','页数','出版时间','标签','简介'),show="headings",displaycolumns="#all",height=300)
    block.heading('isbn13编号',text="isbn13",anchor=W)
    block.heading('中文名',text="cn_title",anchor=W)
    block.heading('英文名',text="en_title",anchor=W)
    block.heading('作者',text="author",anchor=W)
    block.heading('译者',text="translator",anchor=W)
    block.heading('出版社',text="publisher",anchor=W)
    block.heading('价格',text="price",anchor=W)
    block.heading('页数',text="page_num",anchor=W)
    block.heading('出版时间',text="publish_time",anchor=W)
    block.heading('标签',text="tag",anchor=W)
    block.heading('简介',text="description",anchor=W)
    block.pack(side=LEFT, fill=NONE)
    scrollx = Scrollbar(showblock)
    scrolly = Scrollbar(showblock)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=block.xview)
    scrolly.config(command=block.yview)
    block['yscrollcommand'] = scrolly.set
    block['xscrollcommand'] = scrollx.set
    block.bind('<Double-Button-1>', click2)
    blockdata = []
    for i in range(0,len(sortdata)):
        temp = listbox.get(i)
        cuttemp = temp.split("  ")
        blockdatapiece = []
        for j in range(0,len(cuttemp)):
            elementdata = cuttemp[j].split(": ")
            try:
                blockdatapiece.append(elementdata[1])
            except IndexError:
                continue
        blockdata.append(blockdatapiece)
    colornum = 0
    for needdata in blockdata:
        if colornum % 2 == 0:
            block.insert("",END,values=needdata,tags='changecol')
            block.tag_configure('changecol',background='yellow')
        else:
            block.insert("",END,values=needdata)
        colornum += 1

#定义顶部菜单栏：History(搜索历史)
menubar = Menu(root)
menubar.add_command(label='History',command=readhistory)
root.config(menu=menubar)
        
# 定义listbox 为搜索结果 并且设成可滚动的窗口
listbox = Listbox(root, width=400, height=380)
scrollyy = Scrollbar(root)
scrollyy.config(command=listbox.yview)
scrollyy.pack(side=RIGHT, fill=Y, pady=95)
listbox.pack(side=LEFT, fill=NONE, pady=95)
listbox['yscrollcommand'] = scrollyy.set  
scrollxx = Scrollbar(root)
scrollxx.config(command=listbox.xview)
scrollxx.pack(side=BOTTOM, fill=X,pady=300)
listbox['xscrollcommand'] = scrollxx.set 
listbox.bind('<Double-Button-1>', click1)  # 绑定双击事件

# 定义搜索关键字
Label(root, text='搜索关键字：',bg='blue',fg='white').place(x=5, y=0)
entry_key = Entry(root, relief='flat')  # 文件搜索关键字输入框
entry_key.place(x=80, y=0)

# 定义搜索关键字的类型，因为如果是书名搜索要用到模糊搜索
Label(root, text='搜索类型:可不填，使用模糊匹配和优化匹配需填写\"书名\"',bg='blue',fg='white').place(x=230, y=0)  # 类型标签
entry_type = Entry(root, relief='flat')  # 搜索类型输入框
entry_type.place(x=540, y=0)


# 定义搜索按钮
button = Button(root, text='搜索',fg = 'red',command=search).place(x=630, y=0)  # 绑定搜索函数

#定义智能排序按钮
buttonsmartsort = Button(root,text='智能排序',fg='purple',command=smartsort).place(x=0,y=55)#绑定排序函数

#定义匹配度排序按钮
buttontextsort = Button(root,text='按文本匹配度排序',fg='brown',command=textsort).place(x=100,y=55)#绑定排序函数

#定义价格升序排序按钮
buttontextsort = Button(root,text='按价格升序排序',fg='green',command=pricesort).place(x=240,y=55)#绑定排序函数


#定义刷新按钮
button = Button(root, text='刷新',command=again).place(x=630, y=35)  # 绑定搜索函数

#定义另一种格式实现按钮
botton = Button(root,text='以表格形式展现',command=blockshow).place(x=400,y=55)

# 循环窗口
root.mainloop()


