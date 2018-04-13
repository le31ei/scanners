#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2018/4/9 21:34
# @Author: lxflxf
# @File  : scantasks.py
# @Ver   : 0.1
from celery import shared_task
from portscan.models import ScanItems, IPResult
from .core.masscan import PortScan

import gevent
from gevent.pool import Group, Pool
import ipaddress


@shared_task
def start_scan(itemid):
    scanitem = ScanItems.objects.get(itemid=itemid)
    # TODO: 协程扫描
    scan_pool = Pool(5)  # 最大允许100个协程， TODO: 后续可配置
    ips = ipaddress.ip_network(scanitem.scanIP, strict=False)
    for ip in ips:
        # 将ip插入IPresult表
        ipresult = IPResult(scannitem=scanitem, ip=ip)
        ipresult.save()
        scan_pool.add(gevent.spawn(PortScan, str(ip)))
        print(str(ip)+' started! ')
    scan_pool.join()
    scanitem.status = True   # 扫描完成
    scanitem.save()
    return True
