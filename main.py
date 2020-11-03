import logging
import click

from urllib.parse import urljoin
from requests import get
from lxml.etree import HTML
from json import dumps, loads
from FontIconMappingTable import FontIconMappingTable, translate

from time import localtime

_get = get
logger = logging.Logger("main")
handler = logging.FileHandler(f"logs/"
                              f"{localtime().tm_year}-"
                              f"{localtime().tm_mon}-"
                              f"{localtime().tm_mday}-"
                              f"{localtime().tm_min}-"
                              f"{localtime().tm_min}.log",
                              encoding="utf-8")
formatter = logging.Formatter("[%(levelname)s]-[%(levelno)s行]-%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

TIMEOUT = None
HEADERS = ""
OUTFILE = "out.json"


# 包装get方法
def get(*args, **kwargs):
    retry = 0
    while retry <= 3:
        try:
            if TIMEOUT:
                kwargs["timeout"] = TIMEOUT
            if HEADERS:
                kwargs["headers"] = loads(HEADERS.replace("'", "\""))
            logger.info("[获取网页] {}".format(args[0]))
            return _get(*args, **kwargs)
        except Exception as e:
            logger.error("[获取网页失败] " + str(e))
            retry += 1
    return None


def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chr"
                          "ome/86.0.4240.111 Safari/537.36"}


def get_api(chan_id, sub_cata_id, page):
    url = f"https://www.qidian.com/all?chanId={chan_id}&subcataId={sub_cata_id}&orderId=&page={page}&style=" \
          f"2&pageSize=50&siteid=1&pubflag=0&hiddenField=0"
    return url


class OutFile:
    def __init__(self, filename: str):
        self.f = open(filename, "w+", encoding="utf8")

    def save(self, item: dict):
        self.f.write(dumps(item).encode().decode("unicode_escape") + "\n")
        self.f.flush()

    def close(self):
        self.f.close()


# noinspection PyBroadException
def get_detailed_info(novel_url) -> dict:
    novel_id = novel_url[novel_url.rindex("/") + 1:]
    resp = get(novel_url, headers=get_headers())
    html = HTML(resp.text)

    book_info = html.xpath("//div[@class='book-info ']")[0]

    item = {}

    # 标签
    tag = [e.xpath("./text()")[0] for e in book_info[1]]

    # 描述
    intro = book_info[2].xpath("./text()")[0]

    # 破解字体图标加密
    fimt = FontIconMappingTable(html, get_headers())
    mapping_table = fimt.get_table()

    # 推荐
    num = [translate(i, mapping_table) for i in book_info[3].xpath(".//em/span/text()")]
    unit = book_info[3].xpath(".//cite/text()")
    recommend = list(zip(num, unit))

    # 获取评论
    resp = get(f"https://book.qidian.com/ajax/comment/index?bookId={novel_id}&pageSize=15", headers=get_headers())
    resp_json = resp.json()

    rate = translate(resp_json["data"]["rate"], mapping_table)
    user_counts = translate(resp_json["data"]["userCount"], mapping_table)
    # 这个地方喜欢报错, 现在不报错了,嘿嘿
    try:
        # 先用老api, 在尝试新api
        # 老api, 喜欢报错
        logger.debug("使用老api")
        chapter_counts = translate(html.xpath("//span[@id='J-catalogCount']/text()")[0], mapping_table)
    except Exception as e:
        logger.debug("老api出错 使用新api 原因:")
        logger.exception(e, stacklevel=logging.DEBUG)
        chapter_counts = translate(get(f"https://book.qidian.com/ajax/book/category?bookId={novel_id}",
                                       headers=get_headers()).json()["data"]["chapterTotalCnt"], mapping_table)

    # 把数据添加到item
    item["tag"] = tag
    item["intro"] = intro
    item["recommend"] = recommend
    item["rate"] = rate
    item["user_counts"] = user_counts
    item["chapter_counts"] = chapter_counts
    return item


# noinspection PyBroadException
def _spider(chan_id, sub_cata_id, page):
    # 信任get方法不会报错
    resp = get(get_api(chan_id, sub_cata_id, page), headers=get_headers())

    # 如果 `没有找到符合条件的书` 在网页里面, 则返回
    if not resp or "没有找到符合条件的书" in resp.text:
        logger.info(f"爬行到底了 [{chan_id}]")
        return None

    html = HTML(resp.text)
    novels = []

    # 解析文档
    tbody = html.xpath("//tbody")[0]
    for tr in tbody:
        # 每一个项目的信息
        item = {}

        # 类别
        cata = (tr[0][0].xpath("./text()")[0], tr[0][-1].xpath("./text()")[0])
        # 书名
        name = tr[1][0].xpath("./text()")[0]
        # 链接
        novel_url = urljoin("https://www.qidian.com/", tr[1][0].xpath(".//@href")[0])
        # 解析id
        novel_id = novel_url[novel_url.rindex("/") + 1:]
        # 进入简介页面获取信息

        try:
            detailed_info = get_detailed_info(novel_url).items()
        except Exception as e:
            logger.error(f"[数据抓取错误] {name}")
            logger.exception(e)
            continue

        for key, value in detailed_info:
            item[key] = value

        # 最后一章
        last_chapter = tr[2][0].xpath("./text()")[0]
        # 字数
        # todo 添加单位
        '''
            <span class="total" xpath="1">
                <style>@font-face { font-family: sCAWJsOr; src: url('https://qidian.gtimg.com/qd_anti_spider/sCAWJsOr.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/sCAWJsOr.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/sCAWJsOr.ttf') format('truetype'); } .sCAWJsOr { font-family: 'sCAWJsOr' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }</style>
                <span class="sCAWJsOr">𘜒𘜔𘜙𘜕𘜙𘜙</span>万
            </span>
        '''
        # word_counts = tr[3][0][-1].xpath("./text()")[0]
        # 作者
        author = tr[4][0].xpath("./text()")[0]
        update_date = tr[5].xpath("./text()")[0]

        # 封装数据
        item["cata"] = cata
        item["name"] = name
        item["last_chapter"] = last_chapter
        # item["word_count"] = word_counts
        item["author"] = author
        item["update_date"] = update_date
        item["novel_id"] = novel_id

        novels.append(item)
        outfile.save(item)

        logger.info("[导出数据] {}-{}-{}-{} ...".format(
            item["novel_id"],
            item["name"],
            item["author"],
            item["update_date"]
        ))
    return novels


# 主逻辑
def _main(chan_id, sub_cata_id, headers=None, timeout=None, outfile="out.json"):
    global TIMEOUT
    global HEADERS
    global OUTFILE
    TIMEOUT = timeout
    HEADERS = headers
    OUTFILE = outfile
    for i in range(1, 3):
        _spider(chan_id, sub_cata_id, str(i))


# 包装click
# click组
@click.group()
def main():
    pass


# click spider命令
@click.command()
@click.option("--chan-id", "-ci", prompt="输入大类id", help="大类id")
@click.option("--sub-cata-id", "-sci", prompt="输入小类id", help="小类id")
@click.option("--headers", "-h", help="携带请求头")
@click.option("--timeout", "-t", default=15.0, help="设置请求超时时间")
@click.option("--outfile", "-o", default="out.json", help="设置输出文件")
@click.option("--fromfile", "-f", help="从文件加载数据")
@click.option("--debug", "-d", help="启用调试", default=False)
def spider(chan_id, sub_cata_id, headers=None, timeout=None, outfile="out.json", fromfile=None, debug=False):
    """爬取大类chan_id, 小类sub_cata_id下的所有数据"""
    if debug:
        logger.setLevel(logging.DEBUG)
        console.setLevel(logging.DEBUG)
    logger.debug(f"[接受参数]: {TIMEOUT}, {HEADERS}, {OUTFILE}, {debug}")
    if not fromfile:
        _main(chan_id, sub_cata_id, headers, timeout, outfile)
        return
    else:
        with open(fromfile, "r") as f:
            for line in f:
                a, b = line.split(" ")
                _main(a.strip(), b.strip(), headers, timeout, outfile)


main.add_command(spider)
if __name__ == '__main__':
    outfile = OutFile(OUTFILE)
    # r = spider()
    # r = get_detailed_info("https://book.qidian.com/info/1115277")
    # r = get("http://www.baidu.com")
    # logger.info(r)
    # main()
    # outfile.close()

    r = get_detailed_info("https://book.qidian.com/info/1003306811")
    print(r)
