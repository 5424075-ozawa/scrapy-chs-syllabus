import scrapy


class SyllabusSpider(scrapy.Spider):
    name = 'syllabus'
    allowed_domains = ['syllabus.chs.nihon-u.ac.jp']
    start_urls = [
        # 総合教育科目
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_1.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_2.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_3.html',
    ]

    def parse(self, response):
        for href in response.css('#Main > div.Contents.br_clear > div > table > tbody > tr > td:nth-child(1) > a::attr(href)'):
            url = 'https://syllabus.chs.nihon-u.ac.jp/' + href.get()[3:]
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        record = {}
        fields = zip(
            response.css('.table_1 th, table:nth-child(4) td.norm'),
            response.css('.table_1 td, table:nth-child(4) td.norm + td')
        )
        for key, value in fields:
            key = ' '.join(key.css('*::text').get().strip().split())
            value = ' '.join(value.css('*::text').get().strip().split())
            record[key] = value
        record['授業計画'] = []
        for value in response.css('table:nth-child(3) td.number + td'):
            value = ' '.join(value.css('*::text').get().strip().split())
            record['授業計画'].append(value)
        yield record
