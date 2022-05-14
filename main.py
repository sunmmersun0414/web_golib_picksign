import time

from pywebio.input import *
from pywebio.output import *
# from pywebio.pin import *
from pywebio import start_server
import urllib.request
import urllib.parse
import http.cookiejar
import threading
from code_go import go_main

passwordtoid = {}
# th = {}

# class StoppableThread(threading.Thread):
#     """Thread class with a stop() method. The thread itself has to check
#
#     regularly for the stopped() condition."""
#
#     def __init__(self):
#         super(StoppableThread, self).__init__()
#
#         self._stop_event = threading.Event()
#
#     def stop(self):
#         self._stop_event.set()
#
#     def stopped(self):
#         return self._stop_event.is_set()



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

def read_password():
    # with open("./激活码.txt", "w")as fp:
    #     password_strs = fp.readline()
    #     print(password_strs)
    fo1 = open('./激活码.txt', 'r')
    lines2 = [l.split() for l in fo1.readlines() if l.strip()]
    # print(lines2)
    return lines2
def check_pwd():

    def check_id_password(id,pwd):
        global pwd_sign
        if pwd in passwordtoid.values():
            try:
                if passwordtoid[id] == pwd:
                    pwd_sign = 1
                else:
                    return '授权码和账号不匹配，请确认！'
            except:
                return '授权码和账号不匹配，请确认！'
        else:
            passwordtoid[id] = pwd
            print('passwordtoid: ', passwordtoid)
            pwd_sign = 1
            return 'ok'
    # input的合法性校验
    # 自定义校验函数
    # 密码框
    global pwd_sign
    pwd_sign = 0
    # pwd = input('请输入授权码:', type=TEXT, help_text='详情咨询sun.h.w@foxmail.com')
    # id = input('请输入账号(第一次使用可以自定义，自己要记住哦~):', type=TEXT, help_text='详情咨询sun.h.w@foxmail.com')
    def check_passowrd():
        password_strs = read_password()
        # pwd_res = input("请输入授权码:", type=TEXT)
        # print('password:', pwd, '@@', [pwd] in password_strs)
        print('pwd: ',pwd,'   ','id: ',id)
        if [pwd] not in password_strs:
            put_text('授权码错误，请确认！')
            return '授权码错误，请确认！'
        elif [pwd] in password_strs:
            check_return=check_id_password(id,pwd)
            # if pwd in passwordtoid.values():
            #     try:
            #         if passwordtoid[id] == pwd:
            #             pwd_sign = 1
            #         else:
            #             return '授权码和账号不匹配，请确认！'
            #     except:
            #         return '授权码和账号不匹配，请确认！'
            # else:
            #     passwordtoid[id] = pwd
            #     print('passwordtoid: ',passwordtoid)
            put_text(check_return)
            if pwd_sign:
                input_input(id)
                return True
            else:
                put_text(check_return)
                check_pwd()

    # put_image(open('weixing.jpg', 'rb').read(), width='20%', height='20%')
    datas = input_group(
        "获取授权码，请联系:sun.h.w@foxmail.com ",
        inputs=[
            input('请输入授权码:', name='pwd',type=TEXT, help_text='详情咨询sun.h.w@foxmail.com'),
            input('请输入账号(第一次使用可以自定义，自己要记住哦~):', name='id',type=TEXT, help_text='详情咨询sun.h.w@foxmail.com')
        ]
    )
    pwd = datas['pwd']
    id = datas['id']


    check_passowrd()


    return pwd_sign,id



def input_input(id):
    email_pick = input_group(
        '功能选择',
        inputs=[
            input('输入希望接收通知的邮箱地址(不想接收可以不写):', type=TEXT, help_text='详情咨询sun.h.w@foxmail.com',name='email'),
            select("若预选位置均有人，是否随机安排同场馆其他位置:",['no','yes'],help_text='选择no，系统会尝试一小时持续选择预选位置',name='pick_sign')
        ]
    )
    re_mail = email_pick['email']
    pick_sign = email_pick['pick_sign']
    # print(email_pick)
    if str(id) in str(threading.enumerate()):
        put_text('already start:  %s' % id)
        confirm = actions('你已经在选座中，若已经修改座位，点击继续', ['继续', '退出'],
                          help_text='继续后有可能还会抢到之前预设座位！！退出 不影响正在运行的抢座程序')
        # put_markdown('You clicked the `%s` button' % confirm).show()
        # if confirm == '中断':
        #     # th[id].StoppableThread.stop()
        #     put_text('already stop:  %s' % id)
        if confirm == '退出':
            put_text('操作成功！')
            return False


    put_image(open('code.png', 'rb').read(),width='20%',height='20%')
    put_text('请用微信扫一扫，授权登录后复制网址填入！(无需在意网页内容！)')
    myAge = input('输入获得的地址:', type=URL, help_text='详情咨询sun.h.w@foxmail.com')
    print('myAge is:', myAge)
    def check_age(url,re_mail):
        try:
            cookie_string = get_cookie(url)
            put_text(cookie_string)
            # cookie_string = {"cookie":cookie_string}
            # cookie = get_cookie(cookie_string)
            from util.utils import often_seat
            oftenseat = often_seat(cookie_string)
            put_text(oftenseat)
            # seat_tmp=input(label="位置信息", name='seat', type=TEXT, value=oftenseat[0] + '和' + oftenseat[3], readonly=True)
            if id not in str(threading.enumerate()):
                put_text('start:  %s'%id)
                id_tmp=threading.Thread(name=id,target=go_main, args=[cookie_string,re_mail,oftenseat,pick_sign])
                id_tmp.start()
                # th[id] = id_tmp

            else:
                # put_text('already start:  %s' % id)

                id_tmp=threading.Thread(name=id+str(time.time()),target=go_main, args=[cookie_string,re_mail,oftenseat,pick_sign])
                put_text('start:  %s' % id_tmp)
                print(id+str(time.time()))
                id_tmp.start()

            return cookie_string
        except:
            put_text('地址错误：请重试!')
            return '错误：请重试!'

    # myAge = input('输入获得的地址:', type=URL, help_text='详情咨询sun.h.w@foxmail.com')
    # print('myAge is:', myAge)
    # put_text('请用以下内容替换掉status.json文件中cookie:后的内容（注意最后括号保留）')
    print(check_age(myAge,re_mail))



if __name__ == '__main__':
    start_server(applications=[check_pwd, ],
        debug=False,
        auto_open_webbrowser=False,
        remote_access=True,port=54643,reconnect_timeout=5)
    # start_server(
    #     applications=[input_input, ],
    #     debug=True,
    #     auto_open_webbrowser=False,
    #     remote_access=True,
    # )


