# Book-search-engine
# readme


## Description
Name:  宇芯图书搜索引擎
Function:  这是一个用于图书检索的搜索引擎，你可以通过isbn13编号、书名、作者、标签等等进行搜索，然后就会得到匹配到的图书数据，双击就可打开查看完整的图书信息。对于较乱的图书数据，代码中有函数进行清理。
Notes:在每次搜索后如果要进行下一次搜索，请点击一下刷新按钮。


## How to run
首先，确保存有图书数据的excel文件和所有代码文件处于同一目录下，然后运行“GUI and search.py"文件就可以了。


## The libraries you should install
1.jieba
2.pandas
3.fuzzywuzzy


## The steps of running this project
1.数据放在压缩包里,有未处理的图书数据和处理好的图书数据

2.首先进行数据处理得到处理好的干净、有效数据（相关内容见datahandler.py)

3.其次运行GUI and Search.py,就能生成图书搜索引擎

4.在引擎中进行的搜索会保存在历史记录文件history.txt中


## The method of application
1.不需要用到模糊匹配和优化匹配时，直接在搜索关键字后面的框输入搜索内容再点击搜索即可。

2.需要用到模糊匹配和优化匹配时（此功能针对书名），输入搜索内容后在搜索类型填写书名，然后再点击搜索即可。

3.排序方式有三种，用户可以按照喜好选择相应的排序方式。

4.用户还可以点击”以表格形式展现“的按钮，这样搜索结果就会以表格形式展现。

5.双击对应的图书可以查看图书的完整信息。

6.需要注意，每次进行下一次搜索前要刷新。


