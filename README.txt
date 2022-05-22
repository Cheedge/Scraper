Realized functions:
    0. basic scraper
    1. scrap all pages          -- (1. yeild new url; 2. request follow() 3. crawl follow)
    2. scrap and download       -- (add new piplines)
    3. scrap with links         -- (add new parse func: scrapy.Request)
    4. store into file/database -- (pymysql)
    5. scrap post request       -- (scrapy.FormRequest())

Projects:
1. Arxiv
Description:
    scrap arxiv newest physics paper with (title, authors, abstraction, and download link)

2. Translate
Description:
    scrap translations from Googl Translate (https://translate.google.com/?sl=en&tl=de)