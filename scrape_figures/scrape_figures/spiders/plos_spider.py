from scrape_figures.items import JournalFigure
import datetime
import scrapy
import time


class PLOS_Spider(scrapy.Spider):
    name = "pyjournalfig-plos-spider"
    start_urls = [("http://journals.plos.org/plosone/search?q=adsorption"
                   "+isotherm&filterSubjects=Condensed+matter+physics&fi"
                   "lterSubjects=Chemical+compounds&filterSubjects=Chemi"
                   "cal+characterization&filterSubjects=Physics&filterJo"
                   "urnals=PLoSONE&page=1")]

    def parse(self, response):
        for url in response.xpath('//a[contains(@href, "dx.doi.org")]/@href'
                                  ).extract():
            yield scrapy.Request(url, callback=self.parse_article)

        next = response.xpath('//a[contains(@id, "nextPage")]/@href')
        if next.extract() != []:
            print('url next to: ' + next.extract_first())
            yield scrapy.Request(response.urljoin(next.extract_first()),
                                 callback=self.parse)

    def parse_article(self, response):
        title = ''.join(response.xpath('//h1[@id="artTitle"]//text()')
                        .extract()).encode('ascii', 'ignore').strip()

        auth_sel = response.xpath('//a[@class="author-name"]/text()')
        auth_list = [i.extract().encode('ascii', 'ignore').strip() for i in
                     auth_sel]

        pubRaw = ''.join(response.xpath('//li[@id="artPubDate"]//text()')
                         .extract()).encode('ascii', 'ignore')
        pubTemp = time.strptime(pubRaw[11:], "%B %d, %Y")
        pub = time.strftime("%Y-%m-%d", pubTemp)

        journal = response.xpath('body/@class'
                                 ).extract_first().encode('ascii', 'ignore'
                                                          )[8:]
        doi = response.xpath('//li[@id="artDoi"]/a/text()'
                             ).extract_first().encode('ascii', 'ignore')[18:]

        fig_sel = response.xpath('//div[@class="figure"]')
        url_ends = [sel.xpath('.//a[contains(@href, ".g0") and contains(@href,'
                              ' "large")]/@href').extract_first()
                    for sel in fig_sel]
        ftitles = [''.join(sel.xpath('.//div[@class="figcaption"]//text()')
                           .extract()) for sel in fig_sel]
        fcaps = [''.join(sel.xpath('./p[not(@class)]//text()')
                         .extract()) for sel in fig_sel]
        for url_end, ftitle_raw, fcap_raw in zip(url_ends, ftitles, fcaps):
            if url_end is not None:
                ftitle = ftitle_raw.encode('ascii', 'ignore').strip()
                fcap = fcap_raw.encode('ascii', 'ignore').strip()
                im_url = response.urljoin(url_end)
                jFig = JournalFigure(title=title,
                                     auth_list=auth_list[1:-1],
                                     pubDate=pub,
                                     journal=journal,
                                     doi=doi,
                                     figTitle=ftitle,
                                     figCaption=fcap,
                                     file_urls=[im_url])

                yield jFig
