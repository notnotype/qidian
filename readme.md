# 起点网爬虫

### 使用方法
> 快速开始

> 如果你是有经验的人, 那么你只需要看这里就可以了
进入项目文件夹输入一下命令
```
pip install -r requirements.txt
python main.py spider --chan-id 1 --sub-cata-id 1 
```
即可运行爬虫, 爬取第一个大类, 第一个小类下所有项目
我们可以使用一下命令来加强我们爬虫的爬取策略
```
python main.py spider --outfile 1-1.json --timeout 10 --outfile 1-1.json
```
该命令为爬行设定了时间`10s`, 设定了数据的输出文件`1-1.json`
附上所有命令的解释
```
>python main.py spider --help 
Usage: main.py spider [OPTIONS]

  爬取大类chan_id, 小类sub_cata_id下的所有数据

Options:
  --chan-id TEXT      大类id
  --sub-cata-id TEXT  小类id
  --headers TEXT      携带请求头
  --timeout FLOAT     设置请求超时时间
  --outfile TEXT      设置输出文件
  --fromfile TEXT     从文件加载数据
  --help              Show this message and exit.

```

### 环境的搭建
请务必完成了这一步后在继续
* 安装python
* 安装python模块

##### 安装环境

-  运行软件目录下的`python`安装包,安装好`python`解释器
- 输入`win键 + r键` 输入`cmd`进入命令行, 然后进入项目文件夹, 然后输入以下命令来安装依赖
```
pip install -r requirements.txt
```
- 检测环境是否搭建成功 输入以下命令 如果结果为一下结构, 则搭建成功
```
> python --version
Python 3.8.2
```


###### 文件夹文件解释
![文件夹结构](文档/图片/文件夹结构.PNG)

