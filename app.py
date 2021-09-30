import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def get_page_soup(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup


headers = ["Book Title", "UPC", "Product Type",
           "Price (excl. tax)", "Price (incl. tax)", "Tax", "Availability", "Number of reviews"]


def get_book_detail(book_title, url):
    page_soup = get_page_soup(url)
    all_td = page_soup.find_all("td")
    new_list = [x.text for x in all_td]
    new_list.insert(0, book_title)
    return new_list


def get_books(url):
    # url = 'http://books.toscrape.com/index.html'
    page_soup = get_page_soup(url)
    bookshelf = page_soup.findAll(
        "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    rows = []
    for books in bookshelf:
        detail_url = books.h3.a["href"]
        book_title = books.h3.a["title"]
        book_href = f'http://books.toscrape.com/{detail_url}'
        book = get_book_detail(book_title, book_href)
        rows.append(book)

    with open("tets.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def get_category_links():
    url = 'http://books.toscrape.com/index.html'
    page_soup = get_page_soup(url)
    all_li = page_soup.find("ul", {"class": "nav nav-list"}).find_all("li")
    links = []
    for li in all_li:
        a = li.find("a")
        link = a["href"]
        links.append("http://books.toscrape.com/" + link)
    return links


def get_books_by_category():
    links = get_category_links()
    for index, link in zip(range(len(links)), links):
        page_soup = get_page_soup(link)
        bookshelf = page_soup.findAll(
            "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
        rows = []
        for books in bookshelf:
            book_href = books.h3.a["href"].replace("../", "")
            book_url = f"http://books.toscrape.com/catalogue/{book_href}"
            book_title = books.h3.a["title"]
            book = get_book_detail(book_title, book_url)
            rows.append(book)

        with open(f"categorie{index}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)


get_books_by_category()
# get_books()
