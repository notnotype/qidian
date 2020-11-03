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
  -ci, --chan-id TEXT       大类id
  -sci, --sub-cata-id TEXT  小类id
  -h, --headers FILENAME    携带请求头文件
  -t, --timeout FLOAT       设置请求超时时间
  -o, --outfile TEXT        设置输出文件
  -f, --fromfile TEXT       从文件加载数据继续爬取
  -d, --debug BOOLEAN       启用调试(更加详细)
  --help                    Show this message and exit.

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


##### 文件夹文件解释

![文件夹结构](文档/图片/文件夹结构.png)
你看到的软件目录大体就是这个结构的

### 例子

爬取`玄幻``异世大陆`分类下的的所有小说, 保存数据到`21-73.json`中

##### 第一步: 获取主分类id, 和次分类id
看这个网址

`https://www.qidian.com/all?chanId=21&subCateId=73&orderId=&page=1&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0qi`

- `chanId=21`是主分类
- `subCateId=73`是次分类
- `page=1`是第几页

我们只要主分类,和次分类就可以用了
```
python main.py spider -ci 21 -csi 73 -o 21-73.json
```

### 高阶用法 `从文件读取要爬的位置`
> 从文件读取要爬的位置

```
python main.py spider -f in.json
```

in.json的内容
```
1 1
2 62
21 73
```
每一行有这样的格式
```
主类id 次类id
```
以上命令相当于一下命令
```
python main.py spider -ci 1 -csi 1 -o out.json
python main.py spider -ci 2 -csi 62 -o out.json
python main.py spider -ci 21 -csi 73 -o out.json
```
## 展示

![运行截图](文档\图片\运行截图.png)

![项目结构1](文档\图片\项目结构1.png)

![tree](文档\图片\tree.png)

## 声明

因为网站的源代码是不断更新的, 很难保证爬虫能够一直稳定的运行
