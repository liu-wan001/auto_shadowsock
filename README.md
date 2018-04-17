## 背景
为了翻墙，又不想买VPN账号  
一直用的[https://my.freess.org](https://my.freess.org)翻墙，该网站将服务器信息、账号、密码等放在了二维码图片中  
每天都改变密码，新的密码也存在二维码图片中  
所以就需要每天登录扫描二维码翻墙  
扫的多了就变懒了，想要一劳永逸  
本想改源码的，但是一看源码是C#的，看不懂，还是改配置文件吧
## 目标
成功实现一键翻墙，脚本加入开机启动后，实现无需操作，开机即可翻墙。

## 需求
开机自动启动脚本  
从网上下载二维码图片  
识别二维码中的字符串  
从字符串中拿到 服务器地址、密码、端口等信息  
写入shadowsock的配置文件中  
启动shadowsock
判断是否能成功翻墙  
不能则关闭shadowsock，扫描下一个二维码，重复步骤

## 二维码图片地址
Japan：  
https://my.freess.org/images/servers/jp01.png  
https://my.freess.org/images/servers/jp02.png  
https://my.freess.org/images/servers/jp03.png  
America：  
https://my.freess.org/images/servers/us01.png  
https://my.freess.org/images/servers/us02.png  
https://my.freess.org/images/servers/us03.png  


### 识别二维码
得到一个形如ss://YWVzLTI1Ni1jZmI6OTQ1OTA5MTFAMTU5LjIwMy4yMDIuMjUxOjQ0Mw==的字符串  
ss://后边的是base64编码，解码后得到  
aes-256-cfb:94590911@159.203.202.251:443  
格式为 --- 加密方式 : 密码 @ 服务器地址 : 端口号

- 技术点
    - 寻找配置文件保存位置
    - 从图片中识别二维码中的信息
    - 更新后替换配置文件中的信息
    - 如何判断翻墙成功、TCP连接判断 (暂未实现)
- 解决思路
    - 配置文件在当前目录gui-config.json中
    - 知乎专栏有相关介绍https://zhuanlan.zhihu.com/p/21292914
    - 固定格式 仿写
    - python requests 连接 google
### 最终实现
- 没有使用编码实现解析图片中的二维码，通过zbar库中提供的zbarimg.exe直接调用解析图片二维码
- 使用[CSDN博客](http://blog.csdn.net/dkcgx/article/details/46966503)查到的requests库下载二维码图片


### 遇到的困难
- 期间一次可能是网站加强了防护，直接requests.get获取到的数据是403错误。访问被禁止了。搁置了一段时间，从女友那里获得了一些前端知识，给访问的时候加了一个headers就成功get到数据了

User-Agent可以用chrome访问图片网址时自己获取
```
headers = {
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
}


# 下载图片
def dowloadPic(imageUrl,filePath):
    r = requests.get(imageUrl, headers = headers)
    with open(filePath, "wb") as code:
        code.write(r.content)

```
