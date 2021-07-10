fmt:
	poetry run black .  

crawl:
	cd ./recipe_crawler/recipe_crawler; poetry run scrapy crawl kurashiru
