#!/usr/bin/env python
#__author__ == 'Kios':

import requests
import json
import re

def checkip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False

def get_location(ip):
    try:
        if checkip(ip):
            r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=' + ip).text
            res = json.loads(r)
            if res.get('code') == 0:
                return res.get('data').get('region') + res.get('data').get('country') + res.get('data').get('isp')
            else:
                return '请求失败!'
        else:
            return '请输入正确的ip地址!'
    except Exception as e:
        return '接口异常!'


if __name__ == '__main__':
    import sys
    print(get_location(sys.argv[1]))
