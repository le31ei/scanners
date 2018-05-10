### 扫描工具
#### 0x00 部署方式
1、服务器仅支持linux，python版本为3.x

2、服务器需要先安装好masscan和nmap

3、`pip install -r requirements.txt`

4、使用supervisor启动celery,-c参数是指启动的扫描线程数量，50-80最好，配置文件参考如下：
   ```
   [program:celeryd]
command=/home/py3env/bin/celery -A scanners worker -c 100 -l info
directory=/home/scanners
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
logfile_maxbytes=50MB
logfile_backups=10
user=root
stdout_logfile=/home/logs/out.log
stderr_logfile=/home/logs/error.log
```

5、使用supervisor启动django，参考配置文件如下：
```
[program:djangod]
command=/home/py3env/bin/gunicorn -w 4 -b 127.0.0.1:8000 scanners.wsgi:applicatii
on
directory=/home/scanners
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
logfile_maxbytes=50MB
logfile_backups=10
user=celery
stdout_logfile=/home/logs/django-server.log
stderr_logfile=/home/logs/django-error.log
```

6、安装rabbitmq，修改scanners\settings.py中的CELERY_BROKER_URL参数

7、启动后，在项目目录下执行：`python manage.py migrate`,迁移数据库。
