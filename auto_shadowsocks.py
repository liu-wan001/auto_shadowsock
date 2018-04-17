#coding=utf-8
import os
import requests
import base64
import subprocess

def download_pic(imageurl, filepath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    r = requests.get(imageurl,headers = headers)
    with open(filepath, "wb") as code:
        code.write(r.content)

# Japan
jpg1 = '''https://my.freess.org/images/servers/jp01.png'''
jpg2 = '''https://my.freess.org/images/servers/jp02.png'''
jpg3 = '''https://my.freess.org/images/servers/jp03.png'''
# America
jpg4 = '''https://my.freess.org/images/servers/us01.png'''
jpg5 = '''https://my.freess.org/images/servers/us02.png'''
jpg6 = '''https://my.freess.org/images/servers/us03.png'''

if(__name__ == '__main__'):
    # 检测是否运行了shadowsock 运行则关闭
    os.system('taskkill /F /IM Shadowsocks.exe')
    olddir = os.getcwd()
    # 切换到zbar目录
    os.chdir('zbar')
    # 删除旧的QRcode
    if(os.path.exists("QRcode.png")):
        os.remove("QRcode.png")
    # 下载二维码
    download_pic(jpg1, 'QRcode.png')
    # 解析二维码
    r = os.popen('zbarimg.exe QRcode.png')

    info = "".join(r.readlines())
    if(info == ""):
        print(u"出错了，可能网络连接异常，无法下载到二维码图片")
        print(u"请访问https://my.freess.org手动扫码")
        os.system("pause")
        os._exit()
    # 得到base64编码的字符串
    info = info[13:].strip()
    # 得到base64解码后的数据
    info = base64.b64decode(info).strip()
    # 解码后形如'aes-256-cfb:54383109@139.162.67.43:443'
    # 将解码后的数据按格式切分开单独的字符串
    mylist = []
    info = str(info, 'utf-8')
    for s in info.replace(':', '@').split('@'):
        mylist.append(s)
    # 要写入配置文件中的内容格式
    file_data = '''{
    "configs": [
        {
        "server": "%s",
        "server_port": %s,
        "password": "%s",
        "method": "%s",
        "remarks": "",
        "timeout": 5
        }
    ],
    "strategy": null,
    "index": 0,
    "global": false,
    "enabled": true,
    "shareOverLan": false,
    "isDefault": false,
    "localPort": 1080,
    "pacUrl": null,
    "useOnlinePac": false,
    "secureLocalPac": true,
    "availabilityStatistics": false,
    "autoCheckUpdate": true,
    "checkPreRelease": false,
    "isVerboseLogging": false,
    "logViewer": {
        "topMost": false,
        "wrapText": false,
        "toolbarShown": false,
        "Font": "Consolas, 8pt",
        "BackgroundColor": "Black",
        "TextColor": "White"
    },
    "proxy": {
    	"useProxy": false,
    	"proxyType": 0,
    	"proxyServer": "",
    	"proxyPort": 0,
    	"proxyTimeout": 3
    },
    "hotkey": {
        "SwitchSystemProxy": "",
        "SwitchSystemProxyMode": "",
        "SwitchAllowLan": "",
        "ShowLogs": "",
        "ServerMoveUp": "",
        "ServerMoveDown": ""
    }
    }''' % (mylist[2], mylist[3], mylist[1], mylist[0])
    # 切换回Shadowsock目录
    os.chdir(olddir)
    # 把配置文件'gui-config.json'删除
    if(os.path.exists('gui-config.json')):
        os.remove('gui-config.json')
    # 将config数据写入新的文件中
    try:
        file_object = open('gui-config.json', 'w')
        file_object.write(file_data)
    finally:
        file_object.close()
    # 启动ShadowSock
    if(os.path.exists('Shadowsocks.exe')):
        subprocess.Popen('Shadowsocks.exe')
    else:
        print(u"找不到Shadowsocks.exe")
        os.system('pause')
