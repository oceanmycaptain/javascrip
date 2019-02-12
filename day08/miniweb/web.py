import re
import time
from pymysql import *
import urllib.parse
import json


"""
g_url_func = {
    "/index.py": index,
    "/center.py": center
}
"""
g_url_func = dict()

def route(url):
    def set_func(func):

        # key：/index.py
        # value: index
        g_url_func[url] = func

        def call_func():
            func()
        return call_func
    return set_func

# ajax接口
@route(r"/index_data")
def index(file_name,url_param=None,url=None):    
    
    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """select * from info;"""
    cursor.execute(sql)
    data_from_mysql = cursor.fetchall()
    cursor.close()
    db.close()

    jsonData = []

    for row in data_from_mysql:
        result = {}
        result['id'] = str(row[0])
        result['code'] = str(row[1])
        result['sname'] = str(row[2])
        result['rate01'] = str(row[3])
        result['rate02'] = str(row[4])
        result['new_prize'] = str(row[5])
        result['high'] = str(row[6])
        result['date'] = str(row[7])
        jsonData.append(result)

    content = json.dumps(jsonData)
    return content

# jsonp接口
@route(r"/index_jsonp_data")
def index_jsonp(file_name,url_param,url=None):

    # callback=jQuery1124018787969015631711_1522330257607&_=1522330257608
    dat_arr = re.split('[=&]',url_param)
    fnName = dat_arr[1]   
    
    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """select * from info;"""
    cursor.execute(sql)
    data_from_mysql = cursor.fetchall()
    cursor.close()
    db.close()

    jsonData = []

    for row in data_from_mysql:
        result = {}
        result['id'] = str(row[0])
        result['code'] = str(row[1])
        result['sname'] = str(row[2])
        result['rate01'] = str(row[3])
        result['rate02'] = str(row[4])
        result['new_prize'] = str(row[5])
        result['high'] = str(row[6])
        result['date'] = str(row[7])
        jsonData.append(result)

    content = json.dumps(jsonData)
    content = fnName + '(' + str(content) + ')'
    return content

# ajax接口
@route(r"/center_data")
def center(file_name,url_param=None,url=None):

    # data_from_mysql = "这是数据库中的数据信息。。。。。。"
    # 创建Connection连接
    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on f.info_id=i.id;"""
    cursor.execute(sql)
    data_from_mysql = cursor.fetchall()
    cursor.close()
    db.close()

    jsonData = []

    for row in data_from_mysql:
        result = {}
        result['code'] = str(row[0])
        result['sname'] = str(row[1])
        result['rate01'] = str(row[2])
        result['rate02'] = str(row[3])
        result['new_prize'] = str(row[4])
        result['high'] = str(row[5])
        result['bak'] = str(row[6])
        jsonData.append(result)

    content = json.dumps(jsonData)
    return content

# ajax接口
@route(r"/update_data")
def update(file_name,url_param,url=None):
    """显示修改新的页面"""

    stock_code = url_param.split('=')[1]   

    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """select note_info from focus where info_id = (select id from info where code="%s");""" % stock_code
    cursor.execute(sql)
    data_from_mysql = cursor.fetchone()  # ----> ("描述",)
    cursor.close()
    db.close()

    result = {}
    result['code'] = stock_code
    result['info'] = data_from_mysql[0]

    content = json.dumps(result)    

    return content


# ajax接口
@route(r"/change_data")
def update_note_info(file_name,url_param,url=None):
    """显示修改新的页面"""
    dat_arr = re.split('[=&]',url_param)
    stock_code = dat_arr[1]
    stock_note_info = urllib.parse.unquote(dat_arr[3])

    # data_from_mysql = "这是数据库中的数据信息。。。。。。"
    # 创建Connection连接
    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """update focus set note_info = "%s" where info_id = (select id from info where code="%s");""" % (stock_note_info, stock_code)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

    return "更新成功"


# ajax接口
@route(r"/add_data")
def update_note_info(file_name, url_param, url=None):
    
    stock_code = url_param.split('=')[1]  

    # 创建Connection连接
    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """select * from focus where info_id = (select id from info where code="%s");""" % (stock_code)
    cursor.execute(sql)

    if cursor.fetchone():
        cursor.close()
        db.close()
        return "请不要重复添加"

    sql = """insert into focus (info_id) select id from info where code="%s";""" % (stock_code)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

    return "关注成功"

# ajax接口
@route(r"/del_data")
def delete(file_name, url_param, url=None):

    stock_code = url_param.split('=')[1]

    # 创建Connection连接
    db = connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    # 获得Cursor对象
    cursor = db.cursor()
    sql = """delete from focus where info_id = (select id from info where code="%s");""" % (stock_code)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

    return "取消关注成功"


def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)

    # 取出浏览器传递给web服务器的url中的 请求资源路径
    # /a/b/c/index.html
    file_name = environ['PATH_INFO']
    url_param = environ['URL_DAT']     

    try:
        # /update/300268.html
        # r"/update/\d*\.html"
        # g_url_func = {
        #     r"/index\.html":index,
        #     r"/center\.html":center,
        #     r"/update/\d*\.html":update,
        # }

        for url, call_func in g_url_func.items():
            ret = re.match(url, file_name)
            if ret:
                return call_func(file_name,url_param,url)
        else:
            return "没有要访问的页面，请求的页面是：%s" % file_name
    except Exception as ret:
        return "%s,,,,,%s" % (str(environ), ret)
