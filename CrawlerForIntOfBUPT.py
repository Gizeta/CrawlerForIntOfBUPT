#encoding:utf-8
import re
import requests
import sys
import time

def handleRequests(session, url, method = 'GET', data = None):
    from config import proxies
    from config import headers
    result = ''
    try:
        if method == 'GET':
            result = session.get(url, headers = headers, data = data, proxies = proxies)
        elif method == 'POST':
            result = session.post(url, headers = headers, data = data, proxies = proxies)
        else:
            return None
    except:
        print('连接失败.')
        exit(0)
    return result

def login(session, userInfo):
    result = handleRequests(session, 'http://10.108.134.139/', 'GET').text

    t = re.search(r'id=\"__VIEWSTATE" value=\"(\S+)\"', result)
    if t is None or len(t.groups()) < 1:
        print('登陆失败.')
        return
    userInfo['__VIEWSTATE'] = t.group(1)
    t = re.search(r'id=\"__EVENTVALIDATION" value=\"(\S+)\"', result)
    if t is None or len(t.groups()) < 1:
        print('登陆失败.')
        return
    userInfo['__EVENTVALIDATION'] = t.group(1)

    result = handleRequests(session, 'http://10.108.134.139/default.aspx', 'POST', userInfo).text
    
    t = re.search(r'<a id=\"repPapers_con_0_hlPaper_0\"[\s\S]+>([\s\S]+?)</a>', result)
    if t is None or len(t.groups()) < 1:
        print('登陆失败 或 论文尚未上传.')
        return
    print('学号 '+ userInfo['tbID'] + ' 论文 [' + t.group(1) + '] 已被上传.')

def check(session, userInfo):
    result = handleRequests(session, 'http://10.108.134.139/student/paper.aspx?uid=' + userInfo['tbID'], 'GET').text

    if result.find('我的论文') < 0:
        print('未获得有效cookie，尝试重新登陆...')
        login(session, userInfo)
        return '在审'
    
    t = re.search(r'<span id=\"repPapers_con_0_labFlag_0\" style=\"font-weight:bold;\">([\s\S]+?)</span>', result)
    if t is None or len(t.groups()) < 1:
        print('状态获取异常，请联系作者，出bug啦...')
        return
    print('当前状态：' + t.group(1) + '.')
    return t.group(1)

def focus(userInfo):
    userInfo['ddSave'] = 0
    userInfo['btnLogin'] = '登录'
    with requests.Session() as session:
        login(session, userInfo)
        while '在审' == check(session, userInfo):
            time.sleep(1)

if __name__=='__main__':
    from config import userInfo
    focus(userInfo)