from django.db import models
from datetime import datetime
import uuid


# Create your models here.
class ScanItems(models.Model):
    itemid = models.CharField(unique=True, max_length=100, default=uuid.uuid4, verbose_name='任务编号')
    scanname = models.CharField(max_length=50, verbose_name='扫描项目名', unique=True)
    scanIP = models.CharField(max_length=100, verbose_name='扫描IP段', unique=True)
    status = models.BooleanField(default=False, verbose_name='扫描状态')
    process = models.IntegerField(default=0, verbose_name='扫描进度')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '扫描项目'
        verbose_name_plural = verbose_name


class IPResult(models.Model):
    scannitem = models.ForeignKey(ScanItems, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50, verbose_name='ip地址')

    class Meta:
        verbose_name = 'IP扫描结果'
        verbose_name_plural = verbose_name


class PortResult(models.Model):
    ip = models.ForeignKey(IPResult, on_delete=models.CASCADE)
    port = models.CharField(max_length=10, verbose_name='端口')
    service = models.CharField(max_length=500, verbose_name='服务')
    title = models.CharField(max_length=50, verbose_name='title')

    class Meta:
        verbose_name = '端口结果'
        verbose_name_plural = verbose_name
