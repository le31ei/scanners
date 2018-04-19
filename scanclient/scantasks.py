#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2018/4/9 21:34
# @Author: lxflxf
# @File  : scantasks.py
# @Ver   : 0.1
from celery import shared_task
from portscan.models import ScanItems, IPResult
from .core.masscan import PortScan
from celery.result import AsyncResult
from time import sleep


import ipaddress


@shared_task
def start_scan(itemid):
    scanitem = ScanItems.objects.get(itemid=itemid)
    # TODO: 协程扫描
    ips = ipaddress.ip_network(scanitem.scanIP, strict=False)
    result = []
    for ip in ips:
        # 将ip插入IPresult表
        ipresult = IPResult(scannitem=scanitem, ip=ip)
        ipresult.save()
        result.append(dispatch_scan.delay(str(ip)))
        print(str(ip) + ' started! ')
    while True:
        for _ in result:
            if AsyncResult(_.task_id).ready():    # 执行完毕，清除
                result.remove(_)
        print('has '+str(len(result))+' not done!')
        if len(result) != 0:
            print(result[0].status)
        if len(result) == 0:
            break
    scanitem.status = True   # 扫描完成
    scanitem.save()
    return True


@shared_task(time_limit=1200)
def dispatch_scan(ip):
    """
    分发到celery去跑
    :param ip:
    :return:
    """
    PortScan(ip)

    return True
