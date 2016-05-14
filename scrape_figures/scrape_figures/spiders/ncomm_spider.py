from scrape_figures.items import JournalFigure
import datetime
import scrapy
import codecs


class NComm_Spider(scrapy.Spider):
    name = "pyjournalfig-ncomm-spider"
    start_urls = [("http://www.nature.com/search?article_type=research&journal"
                   "=ncomms&order=relevance&q=adsorption%20isotherm")]

    def parse(self, response):
        for url in response.xpath('//a[contains(@href,"full")]/@href'
                                  ).extract():

            yield scrapy.Request(url, callback=self.parse_article)
        next = response.xpath('//nav//li[@data-page="next"]/a')
        yield scrapy.Request(response.urljoin(next.xpath('@href'
                                                         ).extract_first()),
                             callback=self.parse)

    def parse_article(self, response):
        url_end = response.xpath('//a[contains(@class, "view-all")]/@href'
                                 ).extract_first()
        url = response.urljoin(url_end)
        info_sel = response.xpath('//article/header')

        title = ''.join(info_sel.xpath('.//h1[@class="article-heading"]'
                                       '//text()').extract()
                        ).encode('ascii', 'ignore').strip()

        auth_sel = response.xpath('//a[@class="name" and '
                                  'contains(@href, "auth")]//text()')
        auth_list = [''.join(i.extract()).encode('ascii', 'ignore').strip()
                     for i in auth_sel]

        pub = info_sel.xpath('.//dt[contains(@class, "published")'
                             ']/following-sibling::*/time/@datetime'
                             ).extract()[0].encode('ascii', 'ignore')

        journal = info_sel.xpath('.//dd[@class="journal-title"]/text()'
                                 ).extract()[0].encode('ascii', 'ignore')

        doi = info_sel.xpath('.//dd[@class="doi"]/text()'
                             ).extract()[0][4:].encode('ascii', 'ignore')

        dat_to_pass = [title, auth_list, pub, journal, doi]

        request = scrapy.Request(url, callback=self.parse_fig_index)
        request.meta['dat'] = dat_to_pass

        yield request

    def parse_fig_index(self, response):
        # print('Now in the view all figures page')
        for u_end in response.xpath('//a[@class="fig-link"]'
                                    '[contains(@href, "_F")]/@href').extract():
            url = response.urljoin(u_end)
            # jFig = response.meta['jFig']
            # print(jFig['journal'])

            request = scrapy.Request(url, callback=self.parse_fig)
            request.meta['dat'] = response.meta['dat']
            yield request

    def parse_fig(self, response):
        # print('now parsing a figure!')
        fttext = response.xpath('//article//h1[@class="main-heading"]//text()'
                                ).extract()

        ftitle = ''.join(fttext).encode('ascii', 'ignore').strip()

        fCap = ''.join(response.xpath('//div[@class="description"]/p//text()'
                                      ).extract()).encode('ascii', 'ignore'
                                                          ).strip()

        im_url_end = response.xpath('//img[@class="fig"]/@src').extract_first()
        im_url = response.urljoin(im_url_end)

        jFig = JournalFigure(title=response.meta['dat'][0],
                             auth_list=response.meta['dat'][1],
                             pubDate=response.meta['dat'][2],
                             journal=response.meta['dat'][3],
                             doi=response.meta['dat'][4],
                             figTitle=ftitle,
                             figCaption=fCap,
                             file_urls=[im_url])
        yield jFig
