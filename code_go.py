import execjs
import yagmail
import requests
from bs4 import BeautifulSoup
import json
import re
import time
import datetime
import yagmail
import pyperclip
from send_email import send_mail
# from request_test import get_wechatSESS_ID
from util.utils import get_cookie,cookie_check
from util.utils import *
from pywebio.input import TEXT, input, textarea, select, actions, input_group, radio


myheaders = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'Content-Length': '729',
             'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile '
                           'Safari/537.36 MMWEBID/68 MicroMessenger/8.0.16.2040(0x28001053) Process/toolsmp '
                           'WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
             'Content-Type': 'application/json', 'Accept': '*/*', 'Origin': 'https://web.traceint.com',
             'X-Requested-With': 'com.tencent.mm', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors',
             'Sec-Fetch-Dest': 'empty', 'Referer': 'https://web.traceint.com/web/index.html',
             'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}

library_body = {"operationName": "index",
                  "query": "query index($pos: String!, $param: [hash]) {\n "
                          "userAuth {\n oftenseat {\n list {\n id\n info\n lib_id\n seat_key\n status\n }\n }\n "
                          "message {\n new(from: \"system\") {\n has\n from_user\n title\n num\n }\n indexMsg {\n "
                          "message_id\n title\n content\n isread\n isused\n from_user\n create_time\n }\n }\n "
                          "reserve {\n reserve {\n token\n status\n user_id\n user_nick\n sch_name\n lib_id\n "
                          "lib_name\n lib_floor\n seat_key\n seat_name\n date\n exp_date\n exp_date_str\n "
                          "validate_date\n hold_date\n diff\n diff_str\n mark_source\n isRecordUser\n isChooseSeat\n "
                          "isRecord\n mistakeNum\n openTime\n threshold\n daynum\n mistakeNum\n closeTime\n "
                          "timerange\n forbidQrValid\n renewTimeNext\n forbidRenewTime\n forbidWechatCancle\n }\n "
                          "getSToken\n }\n currentUser {\n user_id\n user_nick\n user_mobile\n user_sex\n "
                          "user_sch_id\n user_sch\n user_last_login\n user_avatar(size: MIDDLE)\n user_adate\n "
                          "user_student_no\n user_student_name\n area_name\n user_deny {\n deny_deadline\n }\n sch {\n "
                          "sch_id\n sch_name\n activityUrl\n isShowCommon\n isBusy\n }\n }\n }\n "
                          "ad(pos: $pos, param: $param) {\n name\n pic\n url\n }\n}","variables": {"pos": "App-首页"}}

class Config():
    def __init__(self):
        ###########################################只用修改两行符号之间的值#######################################################
        self.seat_room = ''       # 自习室
        self.seat_where = ''    # 座位646
        self.mylove_seat = []
        # self.seat_room = '20099'       # 自习室测试
        # self.seat_where = '40,33'    # 座位646
        self.epassword = ''  # 邮箱密码
        self.code = ''
        self.my_cookies = {
            ''
            # 'FROM_TYPE': 'weixin',
            # 'wechatSESS_ID': '24408bda042ca3a6798cc32d2fd2db93662a9273157d7d7d',
            # # 'wechatSESS_ID':'',
            # 'SERVERID': 'e3fa93b0fb9e2e6d4f53273540d4e924|1651201402|1651201399',
            # 'Authorization':'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjIzNzM3MDc4LCJzY2hJZCI6MjEsImV4cGlyZUF0IjoxNjUxMjM3NjQzfQ.xnE4Amr_RXcGLdierbrGXHFlM - ovmb9pmEinM - zyyxIv58CsAoJrrfEexF9UC_Gr8CM - nxdbJaOkW8ut97jnQ4u3vIKSsjfG2pvg9xk6CxUMK2xjSk4aSaywyX2aRaxC8OT_HN - WVyVIOu_UWZvajv35lVAC8iJOom6f1ntKcr8qP4Ak7kUpInRtwZuWIiZl - -B1QzTdngn2EEpGoDOw82QwpRrcZYyy2mjPyhI6IGEJfQ5gw2PpksHAK35HBmdHkCTNF9zLdrd9ox1Sz9ZVe4_diz0_nxbTyzI - dZXhBjiVZWcfJRhuNsg5ub9O5VKSrvyHFStTkeDSg_PxC - baqg;'
        }
        # self.my_cookies = {
        #     'FROM_TYPE': 'weixin',
        #     'wechatSESS_ID': 'c3a2c4f6545cce660603ea16582fb1a8e68e5df96e21e285',
        #     # 'wechatSESS_ID':'',
        #     'SERVERID': 'e3fa93b0fb9e2e6d4f53273540d4e924|1651201402|1651201399'
        # }                               # cookie相关，只用改 'wechatSESS_ID' 和 'SERVERID' 填入两个引号之间
        # self.hostmail = 'smtp.qq.com'  # 邮箱服务器地址
        self.hostmail = 'smtp.qq.com'  # 邮箱服务器地址
        self.email = ''  # 邮箱账号
        ########################################只用修改两行符号之间的值##########################################################
        # self.get_seattime = '2021-01-1 6:00:00'
        self.get_seattime = '2022-04-28 6:00:01'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000233) NetType/WIFI Language/zh_CN'}
        self.sum_url = {'reserve_url': '\"https://' + "wechat.v2.traceint.com" + '/index.php/reserve/get/\"',
                        'room_url': 'https://wechat.v2.traceint.com/index.php/reserve/index.html?f=wechat',
                        'into_room': 'https://wechat.v2.traceint.com/index.php/reserve/layout/libid=',
                        'person_url': 'https://wechat.v2.traceint.com/index.php/center.html',
                        'js_url': ''}
        self.pick_sign = 'no'


def scan_room(config):
    list_room = {}
    requests.packages.urllib3.disable_warnings()
    url=config.sum_url['into_room']+config.seat_room+'&'+str(int(time.time()))
    # r = requests.get(url, cookies=config.my_cookies,
    #                  headers=config.headers, verify=False, timeout=5)
    r = requests.get(url, cookies=config.my_cookies,
                     headers=config.headers, verify=False, timeout=5)
    r.encoding = 'utf-8'
    html = r.text
    print('获取页面：',url)
    return list_room, html


def scan_script(html, config):
    soup = BeautifulSoup(html, 'lxml')
    scripts = soup.find_all('script')
    for script in scripts:
        try:
            if 'layout' in script.get('src') and 'cache' in script.get('src'):
                config.sum_url['js_url'] = script.get('src')
                print('获取加密js地址：', config.sum_url['js_url'])
                break
        except:
            pass


def scan_person(config):
    url = config.sum_url['person_url']
    r = requests.get(url, headers=config.headers,
                     cookies=config.my_cookies, verify=False, timeout=5)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('div', class_='nick')
    print('个人信息：', name.string)
    return name.text


def encode(config, a, b):
    js_url = config.sum_url['js_url']
    reserve_url = config.sum_url['reserve_url']
    while js_url == '':
        return 'js_url_error'

    hexch_js_code = requests.get(
        js_url, cookies=config.my_cookies, headers=config.headers, verify=False, timeout=5)
    # hexch_js_code = requests.session().get(
    #     js_url, cookies=config.my_cookies, headers=config.headers, verify=False, timeout=5)
    # print(hexch_js_code.headers)
    hexch_js_code.encoding = 'gbk'
    hexch_js_code = hexch_js_code.text
    hexch_js_code = hexch_js_code.replace('\n', '')
    # yzm = hexch_js_code.split(',')[0].split('\"')[1]
    yzm = hexch_js_code.split('var r=JSON.parse')[-1].split(']")')[0].strip('[("').strip('")]')
    yzm_tmp = ''
    if len(yzm)<500:
        # yzm_dict = '{'+hexch_js_code.split('{')[1].split('}')[0]+'}'
        yzm_dict = hexch_js_code.split('{')[1].split('}')[0]
        yzm_dict={i.split(':')[0]:i.split(':')[1] for i in yzm_dict.split(',')}
        for i in yzm:
            if i==',':
                continue
            else:
                yzm_tmp = yzm_tmp+str(yzm_dict[i])
    pattern = re.compile(r'(?<=T\.ajax_get\().*?(?=,)')
    ajax_url = pattern.search(hexch_js_code).group(
        0).replace('AJAX_URL', reserve_url)
    hexch_js_code = re.sub(
        r'T\.ajax_get', 'return %s ; T.ajax_get' % ajax_url, hexch_js_code)
    tmp = execjs.compile(hexch_js_code)
    # submint_url = tmp.call('reserve_seat', a, b)
    # b=list(b)
    # if len(yzm)<500:
    try:
        submint_url = tmp.call('reserve_seat', a, b,int(yzm_tmp))
    except:
        return 'TypeError: \'JSON\' 未定义'

    # else:
    #     submint_url=tmp.call('reserve_seat', a, b)
    print('提交地址：', submint_url)
    return submint_url

def time_change():
    now=int(time.time())
    SERVERID=config.my_cookies['SERVERID'].split('|')
    config.my_cookies['SERVERID']=SERVERID[0]+'|'+str(now)+'|'+SERVERID[2]

def submit(a, config):
    requests.packages.urllib3.disable_warnings()
    r = requests.get(a, headers=config.headers,
                     cookies=config.my_cookies, verify=False, timeout=5)
    r.encoding = 'utf-8'
    r = json.loads(r.text)
    x=datetime.datetime.now()
    beijing = datetime.timezone(datetime.timedelta(hours=8))
    x = x.astimezone(beijing)
    x=str(x)[:-13]
    print('提交时间',x)
    print(r['msg'])
    return r['msg']

def get_time(config):
    x=datetime.datetime.now()
    beijing = datetime.timezone(datetime.timedelta(hours=8))
    x = x.astimezone(beijing)
    x=str(x)[:-13]
    x=datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    y=datetime.datetime.strptime(config.get_seattime, "%Y-%m-%d %H:%M:%S")
    print('当前时间',x)
    time=(y-x).seconds
    if y<x:
        time=1
    return int(time)

def sendByEmail(config,subject,to,user,message=''):
    user=config.email
    password=config.epassword
    host=config.hostmail
    message=message

    yag = yagmail.SMTP(user=user, password=password, host=host)
    yag.send(to=to,subject=subject,contents=message)

# def choose(html,config):
#     scan_script(html, config)
#     submint_url = encode(config, config.seat_room, config.seat_where)
#     if 'js_url_error' in submint_url:
#         return 'js_url_error'
#     if submint_url == 'TypeError: \'JSON\' 未定义':
#         main(config)
#     time.sleep(1)  # :)
#     msg = submit(submint_url, config)
#     scan_person(config)
#     return msg

def cookie_loop(config):
    def stodic_cookie(str_cookie):
        temp_list = re.findall('[\w|.|,|\-|;]+', str_cookie)
        dic_cookie = {}
        count = 1
        last = ''
        for string in temp_list:
            if count % 2 == 1:
                last = string
            else:
                if string[-1] != ';':
                    string += ';'
                dic_cookie[last] = string
            count += 1
        return dic_cookie

    def dictos_cookie(dic_cookie):
        str_cookie = str(dic_cookie)
        str_cookie = str_cookie.replace('{', '')
        str_cookie = str_cookie.replace('}', '')
        str_cookie = str_cookie.replace('\'', '')
        str_cookie = str_cookie.replace(',', '')
        str_cookie = str_cookie.replace(': ', '=')
        return str_cookie

    def update_cookie(r_cookie, old_cookie):
        old_cookie = stodic_cookie(old_cookie)
        for i in old_cookie:
            for j in r_cookie:
                if i == j:
                    old_cookie[i] = r_cookie[j]
        return dictos_cookie(old_cookie)


    try:
        # with open('./status.json', 'r', encoding='utf-8') as f:
        #     status = dict(json.load(f))
        # for name in status:
        if len(config.my_cookies['cookie']) > 20:
            this_cookie = config.my_cookies
            cookie_status = cookie_check(this_cookie['cookie'])
            if cookie_status == '有效':
                myheaders['Cookie'] = this_cookie['cookie']
                s = requests.session()
                s.headers.clear()
                s.headers.update(myheaders)
                r = s.post("https://wechat.v2.traceint.com/index.php/graphql/",
                            json=library_body)
                r_cookie = requests.utils.dict_from_cookiejar(r.cookies)
                config.my_cookies['cookie'] = update_cookie(r_cookie, this_cookie['cookie'])
                # print('r_cookie: ',r_cookie)
                with open('./status.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps({"cookie":config.my_cookies['cookie']}, ensure_ascii=False))

    except Exception as e:
        print(e)

def choose(cookie, floor, seat):
    myheaders['Cookie'] = cookie
    libnum = floor
    seatkey = seat
    reserve_body = {"operationName": "reserveSeat",
                    "query": "mutation reserveSeat($libId: Int!, $seatKey: String!, "
                             "$captchaCode: String, $captcha: String!) {\n userAuth {\n "
                             "reserve {\n reserveSeat(\n libId: $libId\n seatKey: "
                             "$seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n "
                             ")\n }\n }\n}", "variables": {"seatKey": seatkey,
                                                           "libId": libnum,
                                                           "captchaCode": "",
                                                           "captcha": ""}}
    s = requests.session()
    s.headers.clear()
    s.headers.update(myheaders)
    r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=reserve_body)
    msg = json.loads(r.text)
    if 'errors' in msg:
        return msg['errors'][0]['msg']
    else:
        return '选座成功'
    # return msg

def pick(config,floor):
    loop_signs = 1
    def pick_seat(ck, f, num,loop_signs):
        for i in range(num):
            av_seats = get_av_seats(ck, f)
            if len(av_seats) > 0:
                s = av_seats[0]
                msg = choose(ck, f, s)
                # print(msg)
                if msg == '选座成功':
                    send_mail('选座成功：  %s' % s, config.email)
                    while True:
                        time.sleep(2)
                        import sys
                        sys.exit(0)
                elif '退选或自动释放座位 3 分钟内不可选座!' in msg:
                    print('Seats are not available within 3 minutes: ')
                    time.sleep(10)
                elif '您已经预定了座位' in msg:
                    print('You have reserved a seat', datetime.datetime.now())
                    send_mail('您已经预定了座位：选座系统已退出，如有需要，可再次运行', config.email)
                    while True:
                        time.sleep(2)
                        import sys
                        sys.exit(0)
                if loop_signs % 300 == 0:
                    cookie_loop(config)
                    # print('get cookie_loop')
                    loop_sign = 1
                loop_signs+=1
            time.sleep(3)

    cookie = config.my_cookies['cookie']
    pick_seat(cookie, floor, 600,loop_signs)



def main(config):

    # my_love = ['34,39','34,37','36,38','40,35','36,38','36,36','36,34','34,37','34,35',
    #            '32,39','32,37','30,40','30,38','49,49','49,51','45,49','45,51']
    loop_time =0
    my_love =[config.mylove_seat[1],config.mylove_seat[3]]
    config.seat_where=config.mylove_seat[1]
    config.seat_room = config.mylove_seat[0]
    seat_room = config.seat_room
    seat_where = config.seat_where
    if config.email == '773916295@qq.com':
        my_love = ['40,33','38,34','40,35','36,38','32,39','34,39','30,40','36,36','34,37',
               '32,37','36,34','34,35','49,49','49,51','45,49','45,51']
        config.seat_where='40,33'
    # my_love = ['40,33','38,34','40,35','36,38','32,39','34,39','30,40','36,36','34,37',
    #            '32,37','36,34','34,35','49,49','49,51','45,49','45,51']
    spare=get_time(config)
    t0 = time.time()
    # print('时间间隔：',spare)
    # send_wx('时间间隔：：  %s' % spare)
    # time.sleep(spare)  # 测试的话，把这行注释掉。正式运行的时候在取消注释
    # send_wx('开始时间：：  %s' % time.time())
    # html = scan_room(config)[1]
    time.sleep(1)
    cookie_loop(config)
    # list_room, html=scan_room(config)
    # print(list_room)
    # print(html)
    # if spare <= 300:
    if True:
        try:
            d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '6:00', '%Y-%m-%d%H:%M')
            d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '22:00', '%Y-%m-%d%H:%M')
            # 当前时间
            n_time = datetime.datetime.now()
            # 判断当前时间是否在范围时间内
            loop_sign = 1
            # while n_time < d_time or n_time > d_time1:
            while not d_time<n_time<d_time1:
                # print('False:sleep,mo time:',n_time)
                if loop_sign % 300 == 0:
                    cookie_loop(config)
                    # print('get cookie_loop')
                    loop_sign = 1
                loop_sign+=1
                time.sleep(1)
                d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '6:00', '%Y-%m-%d%H:%M')
                d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '22:00', '%Y-%m-%d%H:%M')
                n_time = datetime.datetime.now()
            # msg =choose(config.my_cookies['cookie'],config.seat_room,config.seat_where)
            # print(msg,config.seat_where)
            msg = '该座位已经被人预定了!'
            while '选座成功' not in msg:
                t1 = time.time()
                tspend = t1 - t0
                if tspend > 300:
                    t0 = time.time()
                    # print('XXXXXXXXXXXX',time.time())
                    cookie_loop(config)

                    # wcid, seid = get_wechatSESS_ID()
                if '不存在' in msg:
                    # sendByEmail(config,'图书馆cookie到期，请及时更新',config.email,config.email,msg)
                    # print(config,'图书馆cookie到期，请及时更新',config.email,config.email,msg)
                    # print('发送邮件成功')
                    pass
                elif '退选或自动释放座位 3 分钟内不可选座!' in msg:
                    print('Seats are not available within 3 minutes: ',seat_where)
                    time.sleep(10)
                    msg =choose(config.my_cookies['cookie'],seat_room,seat_where)
                elif '参数不正确' in msg:
                    # print(msg)
                    config = Config()
                    main(config)
                    time.sleep(1)
                    continue
                # elif 'js_url_error' or '场馆尚未开放，无法操作' in msg:
                elif '场馆尚未开放，无法操作' in msg:
                    time.sleep(1)
                    msg =choose(config.my_cookies['cookie'],config.seat_room,config.seat_where)
                    print('The venue is not open and cannot be operated: ',datetime.datetime.now())
                elif '您已经预定了座位' in msg:
                    print('You have reserved a seat', seat_where,datetime.datetime.now())
                    send_mail('您已经预定了座位：选座系统已退出，如有需要，可再次运行', config.email)
                    while True:
                        time.sleep(2)
                        import sys
                        sys.exit(0)


                elif '该座位已经被人预定了!' in msg:
                    for seat_where in my_love:
                        if loop_time>240:
                            send_mail('位置已连续一小时有人，系统已自动停止，若有需要，可以重新抢座',config.email)
                            while True:
                                time.sleep(2)
                                import sys
                                sys.exit(0)
                        loop_time+=1
                        if '该座位已经被人预定了!' in msg:
                            if config.email=='773916295@qq.com':
                                seat_room = config.seat_room
                            else:
                                seat_room = config.mylove_seat[config.mylove_seat.index(seat_where)-1]
                            # print('changguan :: ',seat_room,datetime.datetime.now())
                            msg =choose(config.my_cookies['cookie'],seat_room,seat_where)
                            
                            print('The seat has been reserved by others: ',seat_where)
                        # elif '场馆尚未开放，无法操作' in msg:
                        #     time.sleep(1)
                        #     msg =choose(config.my_cookies['cookie'],seat_room,seat_where)
                        #     print(msg, seat_where)
                        # elif '退选或自动释放座位 3 分钟内不可选座'in msg:
                        #     time.sleep(10)
                        #     msg =choose(config.my_cookies['cookie'],seat_room,seat_where)
                        #     print(msg, seat_where)
                        elif '选座成功' in msg:
                            send_mail('选座成功：  %s'%seat_where,config.email)
                            while True:
                                time.sleep(2)
                                import sys
                                sys.exit(0)
                                # time.sleep(120)
                                # wcid, seid = get_wechatSESS_ID()
                    if config.pick_sign == 'yes':
                        pick(config,seat_room)
                        send_mail('连续20分钟未发现空位，系统已自动停止，若有需要，可以重新抢座', config.email)
                        while True:
                            time.sleep(2)
                            import sys
                            sys.exit(0)
                    time.sleep(30)
            if '选座成功' in msg:
                send_mail('选座成功：  %s' % config.seat_where,config.email)
                while True:
                    time.sleep(2)
                    import sys
                    sys.exit(0)
                    # time.sleep(120)
                    # wcid, seid = get_wechatSESS_ID()
                # time.sleep(1)
                # import sys
                # sys.exit(0)

        except Exception as e:
            print(e)
            if 'TypeError: \'JSON\' 未定义' == str(e):
                main(config)
    else:
        print('未到时间')
        scan_room(config)


def main_handler(event, context,config):
    try:
        main(config)
    except Exception as e:
        raise e
    else:
        return 'success'


# # def parse_opt(known=False):
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--code', type=str, default='http://wechat.v2.traceint.com/index.php/graphql/?operationName=index&query=query%7BuserAuth%7BtongJi%7Brank%7D%7D%7D&code=081WPjHa1Wik4D0twNIa1XytE84WPjHg&state=1', help='code_id')
#     opt = parser.parse_known_args()[0] if known else parser.parse_args()
#     return opt

def go_main(cookie,email,oftenseat,pick_sign):
    config = Config()
    config.my_cookies = {'cookie':cookie}
    config.email = email
    config.pick_sign = pick_sign
    config.mylove_seat =[oftenseat[1],oftenseat[2],oftenseat[4],oftenseat[5]]
    cookie_use = cookie_check(config.my_cookies['cookie'])
    # print('cookie check:  ', cookie_use)
    if cookie_use != '有效':
        # print('请更新cookie')
        send_mail('地址失效，请更新',config.email)
        time.sleep(2)
        import sys
        sys.exit(0)
    elif cookie_use == '有效':
        # floors = get_floor(cookie)
        # floor = select('选择楼层', options=list(floors.keys()), required=True)
        # oftenseat = often_seat(config.my_cookies)
        main_handler({}, {}, config)


if __name__ == '__main__':
    config = Config()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', type=str, default='http://wechat.v2.traceint.com/index.php/graphql/?operationName=index&query=query%7BuserAuth%7BtongJi%7Brank%7D%7D%7D&code=081WPjHa1Wik4D0twNIa1XytE84WPjHg&state=1', help='code_id')
    args = parser.parse_args()
    config.code = args.code
    print(config.code)
    status = get_cookie(config.code)
    status = {"cookie":status}
    if len(status['cookie'])>100:
        with open('./status.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(status, ensure_ascii=False))
    with open('./status.json', 'r', encoding='utf-8') as f:
        status = dict(json.load(f))
    config.my_cookies = status
    cookie_use = cookie_check(config.my_cookies['cookie'])
    print('cookie check:  ',cookie_use)
    if cookie_use != '有效':
        print('请更新cookie')
        time.sleep(2)
        import sys
        sys.exit(0)

    # while True:
    #     cookie_loop(config)
    #     time.sleep(30)

    print(main_handler({}, {},config))
