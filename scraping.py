from bs4 import BeautifulSoup as bs
import requests
import random
import csv

starting_url = "https://quotes.toscrape.com/"
prefix_url = "https://quotes.toscrape.com"

# List of all quotes, authors, tags
quotes = []
authors = []
tags = []

# Scape quotes, authors, tags
def scrape_page(soup, quotes_list, authors_list, tags_list):

    page_quotes = soup.findAll("span", attrs={"class":"text"})
    page_authors = soup.findAll("small", attrs={"class":"author"})

    divs = soup.findAll("div", attrs={"class":"tags"})
    for div in divs:
        tag = div.findChild("meta", recursive=False).get("content")
        tags_list.append(tag)

    for quote, author in zip(page_quotes, page_authors):
        quotes_list.append(quote.text)
        authors_list.append(author.text)

        


# Loop through all pages and extract data
def cycle_page(url, quotes_list, authors_list, tags_list):

    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    li = soup.find("li", attrs={"class":"next"})
    if li is not None:
        # Scrape quotes and authors
        scrape_page(soup, quotes_list, authors_list, tags_list)

        child = li.findChild("a", recursive=False)
        href = child.get("href")
        cycle_page(f"{prefix_url}{href}", quotes_list, authors_list, tags_list)
    else:
        print("Done")

# Write all data to csv file
def write_to_csv(quotes_list, authors_list, tags_list):
    file = open("scraping_quotes.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(file)

    writer.writerow(["QUOTE", "AUTHOR", "TAGS"])

    for quote, author, tag in zip(quotes_list, authors_list, tags_list):
        writer.writerow([quote, author, tag])

    file.close()

def main():
    cycle_page(starting_url, quotes, authors, tags)
    print(f"Scraped {len(quotes)} quotes with {len(tags)} tags from {len(authors)} authors")

    write_to_csv(quotes, authors, tags)

if __name__ == "__main__":
    main()