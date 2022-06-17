import urllib.request
import urllib.error
from lxml import etree
import wget
import os
import time

def make_url():
    global get_page_url
    url = "https://sc.chinaz.com/moban/"
    n = 1
    # 页面规则信息 默认包含首页
    urllist = ['https://sc.chinaz.com/moban/']
    get_page_url = []
    # 从第一页爬到199页
    for i in range(0,199):
        n += 1
        name = 'index_' + str(n) + '.html'
        urllist.append(url + name)
    # 查看组合的页面
    # print(urllist)
    for x in urllist:
        url = x
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'Cookie': 'UM_distinctid=17ffdf74bf1300-0a9bd18437839e-1f343371-1fa400-17ffdf74bf29d3; toolbox_words=mi.fiime.cn; CNZZDATA300636=cnzz_eid%3D1939574942-1649307441-%26ntime%3D1651196126; user-temp=ff83bd25-fcbc-ae79-f517-80e679c62fba; qHistory=aHR0cDovL3JhbmsuY2hpbmF6LmNvbV/nu7zlkIjmnYPph43mn6Xor6J8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbV/nq5nplb/lt6Xlhbd8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS93ZWJzY2FuL1/nvZHnq5nlronlhajmo4DmtYt8aHR0cDovL3Nlby5jaGluYXouY29tX1NFT+e7vOWQiOafpeivonxodHRwOi8vd2hvaXMuY2hpbmF6LmNvbS9yZXZlcnNlP2RkbFNlYXJjaE1vZGU9MF/mibnph4/mn6Xor6J8Ly9udG9vbC5jaGluYXouY29tL3Rvb2xzL2xpbmtzX+atu+mTvuaOpeajgOa1iy/lhajnq5lQUuafpeivonxodHRwOi8vdG9vbC5jaGluYXouY29tL25zbG9va3VwL19uc2xvb2t1cOafpeivonxodHRwOi8vdG9vbC5jaGluYXouY29tL25vdGlmaWNhdGlvbl/mm7TmlrDlhazlkYp8aHR0cDovL3JhbmsuY2hpbmF6LmNvbV/mnYPph43ljoblj7Lmn6Xor6J8aHR0cDovL3dob2lzLmNoaW5hei5jb20vX1dob2lz5p+l6K+ifGh0dHA6Ly93aG9pcy5jaGluYXouY29tL3JldmVyc2U/ZGRsU2VhcmNoTW9kZT0yX+azqOWGjOS6uuWPjeafpQ==; inputbox_urls=%5B%22mi.fiime.cn%22%5D; auth-token=a496d647-d0b7-4745-9bb0-cf54708f5730; toolbox_urls=www.szmgwx.com|mi.fiime.cn|br.hemumeirong.cn|y.hemumeirong.cn|u.hemumeirong.cn|s.hemumeirong.cn|www.geligw.com|g.5ewl.com|a.5ewl.com|ar.cqdajinkt.com; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1653015614,1655276039,1655429327; Hm_lvt_398913ed58c9e7dfe9695953fb7b6799=1652966343,1654433064,1655082610,1655444268; ASP.NET_SessionId=0125qj2fj05anx2ogj1jm4e2; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1655446442; Hm_lpvt_398913ed58c9e7dfe9695953fb7b6799=1655447097'
        }
        request = urllib.request.Request(url=url, headers=headers)
        handler = urllib.request.HTTPHandler()
        opener = urllib.request.build_opener(handler)
        response = opener.open(request)
        content = etree.HTML(response.read().decode("utf-8"))
        content = content.xpath('//div[@id="container"]//p/a[@target="_blank" and @alt]/@href') # 获取模板下载页面
        for add in content:
            get_page_url.append(add)
    # 查看下载页面
    # print(get_page_url)
    # 查看下载数量
    # print(len(get_page_url))

def make_download() :
    for url in get_page_url:
        try :
            url = 'https:' + url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
                'Cookie': 'UM_distinctid=17ffdf74bf1300-0a9bd18437839e-1f343371-1fa400-17ffdf74bf29d3; toolbox_words=mi.fiime.cn; CNZZDATA300636=cnzz_eid%3D1939574942-1649307441-%26ntime%3D1651196126; user-temp=ff83bd25-fcbc-ae79-f517-80e679c62fba; qHistory=aHR0cDovL3JhbmsuY2hpbmF6LmNvbV/nu7zlkIjmnYPph43mn6Xor6J8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbV/nq5nplb/lt6Xlhbd8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS93ZWJzY2FuL1/nvZHnq5nlronlhajmo4DmtYt8aHR0cDovL3Nlby5jaGluYXouY29tX1NFT+e7vOWQiOafpeivonxodHRwOi8vd2hvaXMuY2hpbmF6LmNvbS9yZXZlcnNlP2RkbFNlYXJjaE1vZGU9MF/mibnph4/mn6Xor6J8Ly9udG9vbC5jaGluYXouY29tL3Rvb2xzL2xpbmtzX+atu+mTvuaOpeajgOa1iy/lhajnq5lQUuafpeivonxodHRwOi8vdG9vbC5jaGluYXouY29tL25zbG9va3VwL19uc2xvb2t1cOafpeivonxodHRwOi8vdG9vbC5jaGluYXouY29tL25vdGlmaWNhdGlvbl/mm7TmlrDlhazlkYp8aHR0cDovL3JhbmsuY2hpbmF6LmNvbV/mnYPph43ljoblj7Lmn6Xor6J8aHR0cDovL3dob2lzLmNoaW5hei5jb20vX1dob2lz5p+l6K+ifGh0dHA6Ly93aG9pcy5jaGluYXouY29tL3JldmVyc2U/ZGRsU2VhcmNoTW9kZT0yX+azqOWGjOS6uuWPjeafpQ==; inputbox_urls=%5B%22mi.fiime.cn%22%5D; auth-token=a496d647-d0b7-4745-9bb0-cf54708f5730; toolbox_urls=www.szmgwx.com|mi.fiime.cn|br.hemumeirong.cn|y.hemumeirong.cn|u.hemumeirong.cn|s.hemumeirong.cn|www.geligw.com|g.5ewl.com|a.5ewl.com|ar.cqdajinkt.com; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1653015614,1655276039,1655429327; Hm_lvt_398913ed58c9e7dfe9695953fb7b6799=1652966343,1654433064,1655082610,1655444268; ASP.NET_SessionId=0125qj2fj05anx2ogj1jm4e2; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1655446442; Hm_lpvt_398913ed58c9e7dfe9695953fb7b6799=1655447097'
            }
            request = urllib.request.Request(url=url, headers=headers)
            handler = urllib.request.HTTPHandler()
            opener = urllib.request.build_opener(handler)
            response = opener.open(request)
            content = etree.HTML(response.read().decode("utf-8"))
            download_pack_url = content.xpath('//div[@class="dian"]/a/@href') # 获取下载节点
            get_download_relurl = download_pack_url[0] # 选取第一个节点下载
            path = os.getcwd()
            filepath = path + "//muban//" # 保存的路径
            if os.path.exists(filepath) != True:
                os.mkdir(filepath)
            print("开始下载:%s"%(get_download_relurl))
            time.sleep(3)
            wget.download(get_download_relurl, filepath)  # 下载模板文件
        except urllib.error.HTTPError:
            print("资源不存在!")
        except urllib.error.URLError:
            print("链接不存在!")


if __name__ == '__main__':
    # 组合页面
    make_url()
    # 获取并下载
    make_download()
