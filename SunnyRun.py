#!/usr/bin/python
# encoding=utf8

import requests
import pymysql
from bs4 import BeautifulSoup


__Author__ = '洪德衍 '
# 请求头
headers = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
session_requests = requests.session()
# 存储从数据库读取的用户的信息
users = None
# 数据库连接程序
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hzkjzyjsxy', db='sunnyRun',charset='utf8')
# Cursor 对象
cur = conn.cursor()
# 存放查询次数
queryNum = 0


class User(object):
    # name:用户名
    # sid:学号
    # sex:性别
    # sum_road:总里程
    # avg_speed:平均速度
    # valid: 有效次数
    # group: 所属部门
    # low_speed:最低速度
    # low_road:最低里程
    # awarf_score:奖励次数
    # bad_score: 扣除次数
    # total_score:总数
    def __init__(self, name, sid, sex, sum_road, avg_speed, valid, group, low_speed, low_road, award_score, bad_score,
                 total_score):
        self.name = name
        self.sid = sid
        self.sex = sex
        self.sum_road = sum_road
        self.avg_speed = avg_speed
        self.valid = valid
        self.group = group
        self.low_speed = low_speed
        self.low_road = low_road
        self.award_score = award_score
        self.bad_score = bad_score
        self.total_score = total_score

    def __str__(self):
        return '(User:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % (
            self.name, self.sid, self.sex, self.sum_road, self.avg_speed, self.valid, self.group, self.low_speed,
            self.low_road, self.award_score, self.bad_score, self.total_score)


def login_website(username, password):
    # 登录信息
    payload = {'username': username, 'password': password}
    my_respone = session_requests.post('http://hzaspt.sunnysport.org.cn/login/', data=payload, allow_redirects=False,
                                       verify=False,
                                       headers=headers)
    # 获取sessionid值
    c = my_respone.headers.get('Set-Cookie')
    # 判断用户密码是否正确
    if c is None:
        test_insert(User(username, None, None, None, None, None, None, None, None, None, None,
                         None))
        print('(%s)username or password error!' % username)
        return

    index = c.index(';')
    c = c[0:index]
    index2 = c.index('=')
    cookeis = {'sessionid': c[index2 + 1:]}
    # 获取sessionid值
    r = session_requests.post('http://hzaspt.sunnysport.org.cn/runner/index.html', cookies=cookeis,
                              headers=headers)
    # 得到相应的数据信息
    get_user_info(r.text)


# 解析html文件.解析相应的数据
def get_user_info(r):
    soup = BeautifulSoup(r, "html.parser")
    # 这里要分离出用户的姓名和性别
    human = soup.select('div .thumbnail', limit=1)
    r = human[0]
    # 获取到用户姓名
    name = r.find_all('label')[1].text.encode('utf-8')
    # 获取到性别
    sid = r.find_all('label')[2].text.encode('utf-8')
    sex = r.find_all('label')[3].text.encode('utf-8')

    # 这里分离出相应的用户详情信息
    details = soup.select('.table')
    # 包含总里程 平均速度 有效次数
    table1 = details[0]
    sum_road = table1.find_all('td')[1].text.encode('utf-8')[0:table1.find_all('td')[1].text.index('m')]
    avg_speed = table1.find_all('td')[3].text.encode('utf-8')[0:table1.find_all('td')[3].text.index('m/s')]
    valid = table1.find_all('td')[5].text.encode('utf-8')
    # 包含分组 最低速度 最低里程
    table2 = details[1]
    group = table2.find_all('td')[1].text.encode('utf-8')
    low_speed = table2.find_all('td')[3].text.encode('utf-8')[0:table2.find_all('td')[3].text.index('m/s')]
    low_road = table2.find_all('td')[5].text.encode('utf-8')[0:table2.find_all('td')[5].text.index('m')]
    # 包含奖励加分 惩罚扣分 最终得分
    table3 = details[2]
    award_score = table3.find_all('td')[1].text.encode('utf-8')
    bad_score = table3.find_all('td')[3].text.encode('utf-8')
    total_score = table3.find_all('td')[5].text.encode('utf-8')
    u = User(name, sid, sex, sum_road, avg_speed, valid, group, low_speed, low_road, award_score, bad_score,
             total_score)
    test_insert(u)
    print(u)


def get_user_from_database():
    global queryNum
    cur.execute("SELECT * FROM student")
    for i in cur.fetchall():
        print('get sid:%s' % i[0])
        login_website(i[0], i[0])
        queryNum += 1
        # 休眠请求时间
        print('request times %s', queryNum)
        # time.sleep(500)

    conn.close()


def test_insert(u):
    try:
        cur.execute('insert into student_info values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
            long(u.sid), u.name, u.sex, long(u.sum_road), float(u.avg_speed), int(u.valid),
            u.group, float(u.low_speed),
            float(u.low_road), int(u.award_score),
            int(u.bad_score),
            int(u.total_score)))
        conn.commit()
    except BaseException as e:
        pass


# 启动程序
get_user_from_database()
