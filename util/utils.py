import requests
import re
import json
import time
import urllib.request
import urllib.parse
import http.cookiejar


myheaders = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'Content-Length': '729',
             'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile '
                           'Safari/537.36 MMWEBID/68 MicroMessenger/8.0.16.2040(0x28001053) Process/toolsmp '
                           'WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
             'Content-Type': 'application/json', 'Accept': '*/*', 'Origin': 'https://web.traceint.com',
             'X-Requested-With': 'com.tencent.mm', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors',
             'Sec-Fetch-Dest': 'empty', 'Referer': 'https://web.traceint.com/web/index.html',
             'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
check_library_body = {"operationName": "list",
                      "query": "query list {\n userAuth {\n reserve {\n libs(libType: -1) {\n "
                               "lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n "
                               "lib_group_id\n lib_comment\n lib_rt {\n seats_total\n "
                               "seats_used\n seats_booking\n seats_has\n reserve_ttl\n "
                               "open_time\n open_time_str\n close_time\n close_time_str\n "
                               "advance_booking\n }\n }\n libGroups {\n id\n group_name\n }\n "
                               "reserve {\n isRecordUser\n }\n }\n record {\n libs {\n "
                               "lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n "
                               "lib_group_id\n lib_comment\n lib_color_name\n lib_rt {\n "
                               "seats_total\n seats_used\n seats_booking\n seats_has\n "
                               "reserve_ttl\n open_time\n open_time_str\n close_time\n "
                               "close_time_str\n advance_booking\n }\n }\n }\n rule {\n "
                               "signRule\n }\n }\n}"}
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


def often_seat(cookie):
    myheaders['Cookie'] = cookie
    s = requests.session()
    s.headers.clear()
    s.headers.update(myheaders)
    r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=library_body)
    text = json.loads(r.text)
    info1 = text['data']['userAuth']['oftenseat']['list'][0]['info']
    lib_id1 = text['data']['userAuth']['oftenseat']['list'][0]['lib_id']
    seat_key1 = text['data']['userAuth']['oftenseat']['list'][0]['seat_key']
    info2 = text['data']['userAuth']['oftenseat']['list'][1]['info']
    lib_id2 = text['data']['userAuth']['oftenseat']['list'][1]['lib_id']
    seat_key2 = text['data']['userAuth']['oftenseat']['list'][1]['seat_key']
    return [info1, lib_id1, seat_key1, info2, lib_id2, seat_key2]


def get_cookie(url):
    def get_code(url):
        query = urllib.parse.urlparse(url).query
        codes = urllib.parse.parse_qs(query).get('code')
        if codes:
            return codes.pop()
        else:
            raise ValueError("Code not found in URL")

    def get_cookie_string(code):
        cookiejar = http.cookiejar.MozillaCookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
        response = opener.open(
            "http://wechat.v2.traceint.com/index.php/urlNew/auth.html?" + urllib.parse.urlencode({
                "r": "https://web.traceint.com/web/index.html",
                "code": code,
                "state": 1
            })
        )
        cookie_items = []
        for cookie in cookiejar:
            cookie_items.append(f"{cookie.name}={cookie.value}")
        cookie_string = '; '.join(cookie_items)
        return cookie_string

    code = get_code(url)
    cookie_string = get_cookie_string(code)
    return cookie_string


def get_floor(cookie):
    myheaders['Cookie'] = cookie
    s = requests.session()
    s.headers.clear()
    s.headers.update(myheaders)
    r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=check_library_body)
    floor_msg = json.loads(r.text)['data']['userAuth']['reserve']['libs']
    floors = {}
    for i in floor_msg:
        floors[i['lib_name']] = i['lib_id']
    return floors


def get_av_seats(cookie, floor):
    myheaders['Cookie'] = cookie
    s = requests.session()
    s.headers.clear()
    s.headers.update(myheaders)
    check_floor_body = {"operationName": "libLayout",
                        "query": "query libLayout($libId: Int, $libType: Int) {\n userAuth "
                                 "{\n reserve {\n libs(libType: $libType, libId: $libId) {"
                                 "\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n "
                                 "lib_layout {\n seats_total\n seats_booking\n "
                                 "seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n "
                                 "type\n name\n seat_status\n status\n }\n }\n }\n }\n "
                                 "}\n}", "variables": {"libId": str(floor)}}
    r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=check_floor_body)
    seat_msg = json.loads(r.text)['data']['userAuth']['reserve']['libs'][0]['lib_layout']['seats']
    av_seats = []
    for i in seat_msg:
        if i['type'] == 1 and i['seat_status'] == 1:
            av_seats.append(i['key'])
    return av_seats


def cookie_check(cookie):
    myheaders['Cookie'] = cookie
    s = requests.session()
    s.headers.clear()
    s.headers.update(myheaders)
    try:
        r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=check_library_body)
        if 'errors' not in json.loads(r.text):
            return '有效'
        else:
            return '失效'
    except:
        return '未知错误'


def cookie_loop():
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

    while True:
        try:
            with open('./status.json', 'r', encoding='utf-8') as f:
                status = dict(json.load(f))
            for name in status:
                if len(status[name]) > 2:
                    this_cookie = status[name][2]
                    cookie_status = cookie_check(this_cookie)
                    if cookie_status == '有效':
                        myheaders['Cookie'] = this_cookie
                        s = requests.session()
                        s.headers.clear()
                        s.headers.update(myheaders)
                        r = s.post("https://wechat.v2.traceint.com/index.php/graphql/",
                                    json=library_body)
                        r_cookie = requests.utils.dict_from_cookiejar(r.cookies)
                        status[name][2] = update_cookie(r_cookie, this_cookie)
            with open('./status.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(status, ensure_ascii=False))
        except Exception as e:
            print(e)
        time.sleep(300)


if __name__ == '__main__':
    cookie_loop()