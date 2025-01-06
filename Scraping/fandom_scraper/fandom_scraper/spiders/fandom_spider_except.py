import scrapy
import re
import os

class FandomSpider(scrapy.Spider):
    if os.path.exists('output.json'):
      os.remove('output.json')

    name = "fandom_except"
    allowed_domains = ["lotr.fandom.com"]
    start_urls = ["https://lotr.fandom.com/wiki/Main_Page"]

    visited_urls = set()  # Keep track of visited URLs to avoid duplicates

    def clean_text(self, text):
        # Replace more than two consecutive newlines with exactly two
        return re.sub(r'\n{3,}', '\n\n', text)


    def parse(self, response):
        # Add the current URL to the visited set
        self.visited_urls.add(response.url)

        # Extract title and content
        title = response.css("h1.page-header__title::text").get()
        paragraphs = response.css("div.mw-parser-output > p *::text,"
                                  "div.mw-parser-output > ul *::text,"
                                  "div.mw-parser-output > dl *::text,"
                                  "div.mw-parser-output > h1 *::text,"
                                  "div.mw-parser-output > h2 *::text"
                                  ).getall()

        # Exclude content within the External links section
        # Locate the index of the "External links" heading
        content_text = "\n".join(paragraphs)
        if "External links" in content_text:
            content_text = content_text.split("External links", 1)[0]

        # Clean excessive newlines
        content = self.clean_text(content_text)

        # Yield the data for the current pagea
        yield {
            "title": title,
            "content": content,
            "url": response.url
        }

        # Extract and follow links on the page to other wiki pages
        for link in response.css("a::attr(href)").getall():
            full_link = response.urljoin(link)

# Skip links with language codes (e.g., "/pl/wiki/", "/ch/wiki/") or specific file formats and keywords
            if re.search(r"/[a-z]{2}/wiki/|\.jpg$|\.jpeg$|\.JPG$|\.JPEG$|\.png$|\.PNG$|_Entertainment", full_link):
                continue

            # Only follow internal wiki links within the allowed domain and skip unwanted links
            if (
                self.allowed_domains[0] in full_link
                and "/wiki/" in full_link
                and "action=edit" not in full_link
                and "/edit" not in full_link
                and "?veaction=edit" not in full_link
                and "?veaction=editsource" not in full_link
                and "?oldid=" not in full_link
                and "?action=" not in full_link
                and "?file=" not in full_link
                and "?diff=" not in full_link
                and "/Talk" not in full_link
                and "/Other" not in full_link
                and "/Blog" not in full_link
                and "/Special" not in full_link
                and "/User" not in full_link
                and "/Category:Blog_posts" not in full_link
                and "/Category:Community" not in full_link
                and "/LOTR:" not in full_link
                and "/Category:Websites" not in full_link
                and "/Help:Editing/Improper_Words_list" not in full_link
                and "/Forum" not in full_link
            ):
                if full_link not in self.visited_urls:
                    self.visited_urls.add(full_link)
                    yield scrapy.Request(url=full_link, callback=self.parse)
