from urllib import request
import re
class Spider():
    url ='https://www.panda.tv/cate/lol'
    root_pattern = r'<div class="video-info">([\s\S]*?)</div>'
    name_pattern = r'</i>([\s\S]*?)</span>'
    num_pattenrn = r'<span class="video-number">([\s\S]*?)</span>'
    # 网页的爬取
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls =str(htmls,encoding='utf-8')
        return htmls
    # 数据的分析，采集
    def __analysis(self,htmls):
        root_html = re.findall(Spider.root_pattern,htmls)
        anchors =[]
        for html in root_html:
            name = re.findall(Spider.name_pattern,html)
            number = re.findall(Spider.num_pattenrn,html)
            anchor ={'name':name,'number':number} 
            anchors.append(anchor)
        return anchors

    def __refine(self,anchors):
        l = lambda anchor : {
            'name':anchor['name'][0].strip(), 
            'number':anchor['number'][0]
        } 
        return map(l,anchors)
    # 排序
    def __sort(self,anchors):
        anchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self,anchor):
        r=re.findall('\d*',anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number*=10000
        return number
    # 数据的展示
    def __show(self,anchors):
        for rank in range(0,len(anchors)):
            print('排名:'+str(rank+1)+':        '+anchors[rank]['name']+'   '+anchors[rank]['number'])
    # 运行
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)
        
if __name__ == '__main__':
    
    spider = Spider()
    spider.go()