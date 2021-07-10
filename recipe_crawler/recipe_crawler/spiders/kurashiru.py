from scrapy.spiders import SitemapSpider
import re


class KurashiruSpider(SitemapSpider):
    name = "kurashiru"
    allowed_domains = ["www.kurashiru.com"]
    sitemap_urls = ["https://www.kurashiru.com/robots.txt"]
    sitemap_rules = [
        (r"/recipes/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$", "parse_recipe"),
    ]

    # strip_pettern = re.compile("^(.)")

    def parse_recipe(self, response):
        uid = response.url.split("/")[-1]
        yield {
            "url": response.url,
            "title": response.xpath(
                '//*[@id="videos_show"]/div/main/article[1]/article/div[2]/h1/text()'
            ).get(),
            "description": response.xpath(
                '//*[@id="videos_show"]/div/main/article[1]/article/p[2]/text()'
            ).get(),
            "ingredients": [
                # 材料から (A) 砂糖 みたいなとき (A) を削除する
                re.sub("^\(.\)", "", ingredient.strip())
                for ingredient in response.xpath(
                    '//*[@id="videos_show"]/div/main/article[1]/article/section[1]/ul/li/a/text()'
                ).extract()
            ],
            "image_url": f"https://video.kurashiru.com/production/videos/{uid}/compressed_thumbnail_square_normal.jpg",
        }
