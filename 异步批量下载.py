import asyncio
import aiohttp
import aiofiles
from lxml import etree
import os
from loguru import logger as log
 
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'Cookie': 'UM_distinctid=17ffdf74bf1300-0a9bd18437839e-1f343371-1fa400-17ffdf74bf29d3; toolbox_words=mi.fiime.cn; CNZZDATA300636=cnzz_eid%3D1939574942-1649307441-%26ntime%3D1651196126; user-temp=ff83bd25-fcbc-ae79-f517-80e679c62fba; qHistory=aHR0cDovL3JhbmsuY2hpbmF6LmNvbV/nu7zlkIjmnYPph43mn6Xor6J8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbV/nq5nplb/lt6Xlhbd8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS93ZWJzY2FuL1/nvZHnq5nlronlhajmo4DmtYt8aHR0cDovL3Nlby5jaGluYXouY29tX1NFT+e7vOWQiOafpeivonxodHRwOi8vd2hvaXMuY2hpbmF6LmNvbS9yZXZlcnNlP2RkbFNlYXJjaE1vZGU9MF/mibnph4/mn6Xor6J8Ly9udG9vbC5jaGluYXouY29tL3Rvb2xzL2xpbmtzX+atu+mTvuaOpeajgOa1iy/lhajnq5lQUuafpeivonxodHRwOi8vdG9vbC5jaGluYXouY29tL25zbG9va3VwL19uc2xvb2t1cOafpeivonxodHRwOi8vdG9vbC5jaGluYXouY29tL25vdGlmaWNhdGlvbl/mm7TmlrDlhazlkYp8aHR0cDovL3JhbmsuY2hpbmF6LmNvbV/mnYPph43ljoblj7Lmn6Xor6J8aHR0cDovL3dob2lzLmNoaW5hei5jb20vX1dob2lz5p+l6K+ifGh0dHA6Ly93aG9pcy5jaGluYXouY29tL3JldmVyc2U/ZGRsU2VhcmNoTW9kZT0yX+azqOWGjOS6uuWPjeafpQ==; inputbox_urls=%5B%22mi.fiime.cn%22%5D; auth-token=a496d647-d0b7-4745-9bb0-cf54708f5730; toolbox_urls=www.szmgwx.com|mi.fiime.cn|br.hemumeirong.cn|y.hemumeirong.cn|u.hemumeirong.cn|s.hemumeirong.cn|[url=http://www.geligw.com]www.geligw.com[/url]|g.5ewl.com|a.5ewl.com|ar.cqdajinkt.com; Hm_lvt_ca96c3507ee04e182fb6d097cb2a1a4c=1653015614,1655276039,1655429327; Hm_lvt_398913ed58c9e7dfe9695953fb7b6799=1652966343,1654433064,1655082610,1655444268; ASP.NET_SessionId=0125qj2fj05anx2ogj1jm4e2; Hm_lpvt_ca96c3507ee04e182fb6d097cb2a1a4c=1655446442; Hm_lpvt_398913ed58c9e7dfe9695953fb7b6799=1655447097'
}
 
async def fetch(url,files=False):
    '''
    异步请求函数
    '''
    async with asyncio.Semaphore(10):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if files:
                    return await response.read(),response.url
                else:
                    return await response.text()
 
async def get_info_url():
    '''
    获取详情页
    '''
    page_url = lambda x :"https://sc.chinaz.com/moban/index_{}.html".format(x)
    all_page_url = [fetch(page_url(i)) for i in range(1,199)]
    res_list = await asyncio.gather(*all_page_url)
    return map(lambda res:['https:' + page_url for page_url in etree.HTML(res).xpath('//div[@id="container"]//p/a[@target="_blank" and @alt]/@href')],res_list)
 
async def get_download_url():
    '''
    获取下载链接
    '''
    url_list = []
    for info_url in await get_info_url():
        if info_url !=[]:
            for url in info_url:
                url_list.append(fetch(url))
    _res_list = await asyncio.gather(*url_list)
    return map(lambda res:etree.HTML(res).xpath('//div[@class="dian"]/a/@href'),_res_list)
 
 
     
async def download_file():
    '''
    下载文件
    '''
    file_contents = await asyncio.gather(*[fetch(url[0],files=True) for url in await get_download_url()])
    await asyncio.gather(*[aiofiles.open(os.path.join(os.getcwd(),'{}.rar'.format(content[1].split('/')[-1])),'wb').write(content[0]) for content in file_contents])
 
 
async def async_main():
    try:
        await download_file()
    except Exception as e:
        log.exception(e)
     
if __name__ == '__main__':
    asyncio.run(async_main())
