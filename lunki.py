import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

username = ''
password = ''
headers = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Referer': 'http://10.0.10.184/jwglxt/xspjgl/xspj_cxXspjIndex.html?doType=details&gnmkdm=N401605&layout=default&su='+username,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
cookiesDit = {
    'JSESSIONID': ''
}
formData = {
    '_search': 'false',
    'nd': '1577962034780',
    'queryModel.showCount': 15,
    'queryModel.currentPage': 1,
    'queryModel.sortName': '',
    'queryModel.sortOrder': 'asc',
    'time': 0
}
def login():
    print('正在登陆')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driverChrome = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver", options=chrome_options)
    # driverChrome.get('https://tieba.baidu.com/index.html')
    # driverChrome = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver")
    driverChrome.get("http://10.0.10.184/jwglxt/xtgl/login_slogin.html")
    driverChrome.find_element_by_id('yhm').send_keys(username)
    driverChrome.find_element_by_id('mm').send_keys(password)
    driverChrome.find_element_by_id('dl').click()
    time.sleep(1)
    print(driverChrome.get_cookie('JSESSIONID'))
    cookiesDit['JSESSIONID']=driverChrome.get_cookie('JSESSIONID')['value']
    print(cookiesDit)
    checkLogin()
    driverChrome.quit()

def checkLogin():
    print('检查是否登陆成功')
    rep=requests.post(url='http://10.0.10.184/jwglxt/xspjgl/xspj_cxXspjqk.html?gnmkdm=N401605&su='+username,headers=headers,cookies=cookiesDit)
    if(len(rep.text)>999):
        print("登陆失败")
        return
    print("还差",rep.json()['wpgs'],'个没评价')
    teaching()
def teaching():
    req_obj = requests.post(
        'http://10.0.10.184/jwglxt/xspjgl/xspj_cxXspjIndex.html?doType=query&gnmkdm=N401605&su='+username,
        data=formData, headers=headers, cookies=cookiesDit)
    json = req_obj.json()

    for item in json['items']:
        data={
            'jxb_id':item['jxb_id'],
            'kch_id':item['kch_id'],
            'xsdm':item['xsdm'],
            'jgh_id':item['jgh_id'],
            'tjzt':item['tjzt'],
            'pjmbmcb_id':item.setdefault('pjmbmcb_id',''),
            'sfcjlrjs':item['sfcjlrjs']
        }
        htm = requests.post(
            'http://10.0.10.184/jwglxt/xspjgl/xspj_cxXspjDisplay.html?gnmkdm=N401605&su='+username,
            data=data,headers=headers, cookies=cookiesDit)
        soup = BeautifulSoup(htm.text,'lxml')
        body = soup.find_all(class_='xspj-body')[0]
        ztpjbl = body.attrs['data-ztpjbl']
        jszdpjbl = body.attrs['data-jszdpjbl']
        xykzpjbl = body.attrs['data-xykzpjbl']
        jxb_id = body.attrs['data-jxb_id']
        kch_id = body.attrs['data-kch_id']
        jgh_id = body.attrs['data-jgh_id']
        xsdm = body.attrs['data-xsdm']

        body_item = body.find_all(class_='panel-pjdx')[0]
        pjmbmcb_id = body_item.attrs['data-pjmbmcb_id']
        pjdxdm = body_item.attrs['data-pjdxdm']
        xspfb_id = body_item.attrs['data-xspfb_id']
        py = ''

        table = body_item.find_all(class_='table-xspj')
        j = {
            'ztpjbl': ztpjbl,
            'jszdpjbl':jszdpjbl,
            'xykzpjbl':xykzpjbl,
            'jxb_id':jxb_id,
            'kch_id':kch_id,
            'jgh_id':jgh_id,
            'xsdm':xsdm,
            'modelList[0].pjmbmcb_id': pjmbmcb_id,
            'modelList[0].pjdxdm': pjdxdm,
            'modelList[0].py': py,
            'modelList[0].xspfb_id': xspfb_id,
        }
        for b_index in range(len(table)):
            tds = table[b_index].find_all('tr')
            for t_index in range(len(tds)):
                if(t_index==0):
                    j['modelList[0].xspjList[{b_index}].childXspjList[{t_index}].pfdjdmxmb_id'.format(b_index=b_index, t_index=t_index)] = '7B3EAC351907795DE0530100007F1240'
                else:
                    j['modelList[0].xspjList[{b_index}].childXspjList[{t_index}].pfdjdmxmb_id'.format(b_index=b_index,t_index=t_index)]='7B3EAC351909795DE0530100007F1240'
                j[ 'modelList[0].xspjList[{b_index}].childXspjList[{t_index}].pjzbxm_id'.format(b_index=b_index,t_index=t_index)]=tds[t_index].attrs['data-pjzbxm_id']
                j['modelList[0].xspjList[{b_index}].childXspjList[{t_index}].pfdjdmb_id'.format(b_index=b_index,t_index=t_index)]=tds[t_index].attrs['data-pfdjdmb_id']
                j['modelList[0].xspjList[{b_index}].childXspjList[{t_index}].zsmbmcb_id'.format(b_index=b_index,t_index=t_index)]=tds[t_index].attrs['data-zsmbmcb_id']
            j['modelList[0].xspjList[{b_index}].pjzbxm_id'.format(b_index=b_index)]=table[b_index].attrs['data-pjzbxm_id']

        print(j)

        rep_body=requests.post(url='http://10.0.10.184/jwglxt/xspjgl/xspj_tjXspj.html?gnmkdm=N401605&su='+username,data=j,headers=headers,cookies=cookiesDit)
        print(rep_body.text)




if __name__ == '__main__':
    login()