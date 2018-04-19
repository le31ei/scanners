#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2018/4/10 10:57
# @Author: lxflxf
# @File  : masscan.py
# @Ver   : 0.1
import masscan
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from scanclient.libs.log import logger


from portscan.models import ScanItems, PortResult, IPResult

import requests
import bs4


def PortScan(ip):
    """
    端口扫描函数，丢ip进来, 只负责扫描端口,然后存入数据库,
    默认不扫描c段
    :return:
    """
    print('ok')
    # 插入IP数据库

    mas = masscan.PortScanner()
    # 不扫描c段
    try:
        mas.scan(ip, ports='0-65535', arguments='--max-rate 2000', sudo=True)
        print('masscan start')
    except:
        print('no ports open')
        return
    # 解析扫描结果，nmap指纹识别端口服务
    result = mas.scan_result
    print(result)
    result_port = dict()
    for ips in result['scan']:
        for ports in result['scan'][ips]['tcp']:
            print('ports: '+str(ports))
            try:
                nm = NmapProcess(ip, options="-sV -Pn -p{0} -host-timeout 300".format(ports))
                print('nmap ing')
                rc = nm.run()
                if rc != 0:
                    logger.error("nmap scan failed: {0}".format(nm.stderr))
                    return False
                try:
                    parsed = NmapParser.parse(nm.stdout)
                    print(parsed.hosts)
                    for host in parsed.hosts:
                        for serv in host.services:
                            # 入库
                            result_port[str(ports)] = serv.service
                            print('ip: %s, 端口%s 对应的服务是 %s' % (ips, ports, serv.service))
                            # TODO：如果为http或者https端口，获取title存入数据库
                            title = ''
                            if 'http' in serv.service or 'https' in serv.service:
                                print('gettile ing')
                                title = gettile(ips+':'+str(ports))
                                print('title is'+title)
                            ip_result = IPResult.objects.get(ip=ips)
                            insert_result = PortResult(ip=ip_result, port=str(ports), service=serv, title=title)
                            insert_result.save()
                    print(result_port)
                except NmapParserException as e:
                    logger.error("Exception raised while parsing scan: {0}".format(e.msg))
            except AssertionError:
                result_port[str(ports)] = 'None'
                logger.error('端口：%s，识别不了服务' % ports)
                # DOne: 入库，端口识别不了服务类型
                continue


def gettile(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)'
                             ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2146.0 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    try:
        r = requests.get('http://' + url, headers=headers, timeout=10)
        if r.status_code == 200:
            html = bs4.BeautifulSoup(_decode_response_text(r.text, r.encoding), 'html.parser')
            if html.title is not None:
                return html.title.text
            else:
                return 'None'
        else:
            return 'None'
    except Exception as e:
        logger.error(e)
        return 'None'


def _decode_response_text(strs, lang=None):
    """
    常见编码解码
    :param str:
    :param lang:
    :return:
    """
    languages = ['UTF-8', 'GB2312', 'GBK', 'iso-8859-1', 'big5']
    if lang:
        languages.insert(0, lang)
    for lang in languages:
        try:
            return strs.encode(lang)
        except:
            return 'None'
    raise Exception('Can not decode response text')

