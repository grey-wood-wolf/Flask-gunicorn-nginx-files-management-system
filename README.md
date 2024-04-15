## Flask-gunicorn-nginx 文件管理系统开发
利用Flask+gunicorn+nginx框架开发的文件管理系统，其中包括对于文件的上传下载、socket自构的上传和下载


# 1、基于linux系统安装flask、nginx、gunicorn
```
apt-get update
sudo apt-get install nginx
sudo pip3 install Flask
sudo pip3 install gunicorn
```

# 2、运行代码，进入NAS_project文件夹后运行start_web.sh文件
```
cd NAS_project
sudo ./start_web.sh
```
# 3、前端使用，利用ip a等命令获取后端ip地址后，浏览器中输入该地址
```
ip a
http://192.168.xxx.xxx:80
```
# 4、公网映射
如果想要映射到公网中，如果有公网地址可以自己映射，如果没有可以使用cpolar进行内网穿透
cpolar参考如下：
> https://blog.csdn.net/a1657054242/article/details/134779908
