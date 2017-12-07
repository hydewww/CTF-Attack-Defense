# Quick_Start

## Install

```
pip install -r requirements.txt
```

## Web Server

```
python manage.py shell
>> db.create_all()
>> exit
python manage.py runserver
```

## Dynamic Flag & Check Service

```
python timing.py
```



# Rules

1. 每队各自有相同的服务器，上面有若干服务 (WEB、PWN) 
2. 每个服务有若干漏洞，可通过漏洞拿到flag。
3. 各队可在不关闭服务的前提下修补自己服务器上的漏洞，防止他人拿到己方flag。
4. 回合制，每回合会检测各服务器服务是否开启，同时各服务器上的flag会变更。



---

**说明: Scoreboard趋势图代码基于 [CTFd](https://github.com/CTFd/CTFd)**
