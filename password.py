import random, string
# 激活码由A-Z 0-9 随机组成
activation_code = string.ascii_uppercase + '0123456789'
def get(num, length):
    with open("./激活码.txt", "w")as fp:
        for i in range(num):
            code = ''
            for j in range(length):
                # 在备选中随机选取一位
                code += random.choice(activation_code)
            # print(code)
                # 再次运行要清空原文件
                fp.truncate()
                #仅当以 "r+" "rb+" "w" "wb" "wb+"等以可写模式打开的文件才可以执行该功能。
                # 将激活码写入文件
            fp.write(code + '\n')
    fp.close()


if __name__ =='__main__':
    get(20,20)