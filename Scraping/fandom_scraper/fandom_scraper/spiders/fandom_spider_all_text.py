import scrapy

class FandomSpider(scrapy.Spider):
    name = "fandom_all_text"
    allowed_domains = ["oldschoolrunescape.fandom.com"]
    start_urls = ["https://oldschoolrunescape.fandom.com/wiki/Old_School_RuneScape_Wiki"]

    visited_urls = set()  # Keep track of visited URLs to avoid duplicates

    def parse(self, response):
        # Add the current URL to the visited set
        self.visited_urls.add(response.url)

        # Extract title and content
        title = response.css("h1.page-header__title::text").get()
        # Extract paragraphs, tables, and other text elements
        paragraphs = response.css("div.mw-parser-output > p::text, div.mw-parser-output > li::text, div.mw-parser-output > table *::text").getall()
        content = "\n".join(paragraphs).strip()

        # Yield the data for the current page
        yield {
            "title": title,
            "content": content,
            "url": response.url
        }

        # Extract and follow links on the page to other wiki pages
        for link in response.css("a::attr(href)").getall():
            full_link = response.urljoin(link)

            # Only follow internal wiki links within the allowed domain and skip unwanted links with query parameters
            if (
                self.allowed_domains[0] in full_link
                and "/wiki/" in full_link
                and '?' not in full_link  # Skip links with query parameters
                and full_link not in self.visited_urls  # Avoid duplicates
            ):
                self.visited_urls.add(full_link)
                yield scrapy.Request(url=full_link, callback=self.parse)
