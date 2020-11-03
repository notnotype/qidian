from fontTools.ttLib import TTFont
from lxml import etree
import requests
import re
import os
import logging

logger = logging.getLogger("main")


#  这是翻译函数
def translate(string, table):
    string = str(string)
    result = ''
    for s in string:
        key = hex(ord(s))
        # logger.debug("正在翻译%s hex: %s" % (s, key))
        key = hex(ord(s))
        try:
            result += table[key]
        except:
            result += s
    return result
    # 尝试新的translate


#  从这里开始获取映射表
class FontIconMappingTable:

    def __init__(self, html, headers=None):
        self.html = html
        self.headers = headers
        self.style = None
        self.ttf_url = None
        self.ttf = None
        self.xml_filename = None
        self.ttf_filename = None
        self.table = {"zero": '0', "one": '1', "two": '2',
                      "three": '3', "four": '4', "five": '5',
                      "six": '6', "seven": '7', "eight": '8',
                      "nine": '9', "period": '.'}

    #  爬取css
    def get_style(self):
        self.style = self.html.xpath("//em/style/text()")[0]
        logger.debug("style get!")

    #  解析style 获取ttf文件的url
    def get_ttf_url(self):
        self.ttf_url = re.findall("https://qidian.gtimg.com/qd_anti_spider/\w+\.ttf", self.style)[0]
        logger.debug("ttf_url get!")

    #  下载ttf文件
    def download_ttf(self):
        #  ttf文件名
        self.ttf_filename = self.ttf_url.split("/")[-1]
        #  xml文件名
        self.xml_filename = self.ttf_url.split("/")[-1].split('.')[0] + ".xml"
        #  测试用 因为懒得加headers
        #  r = requests.get(self.ttf_url)
        #  下载ttf文件
        r = requests.get(self.ttf_url, headers=self.headers)
        with open(self.ttf_filename, 'wb+') as tf:
            tf.write(r.content)

        self.ttf = TTFont(self.ttf_filename)
        logger.debug("ttf and xml_filename get!")

    #  把ttf文件转为XML文件
    def ttf_to_xml(self):
        self.ttf.saveXML(self.xml_filename)
        logger.debug("turn ttf to xml success!")

    #  生成映射表
    def get_table(self) -> dict:
        self.get_style()
        self.get_ttf_url()
        self.download_ttf()
        self.ttf_to_xml()
        xml = etree.parse(self.xml_filename)
        mappingTable = {k: self.table[v] for k, v in zip(xml.xpath("//map/@code"), xml.xpath("//map/@name"))}
        #  删除ttf和xml文件
        os.remove(self.ttf_filename)
        logger.debug("ttf delete success!")
        os.remove(self.xml_filename)
        logger.debug("xml delete success!")
        return mappingTable


if __name__ == "__main__":
    url = "https://book.qidian.com/info/1010868264"
    r = requests.get(url)
    html = etree.HTML(r.text)
    table = FontIconMappingTable(html).get_table()
    logger.debug(table)
