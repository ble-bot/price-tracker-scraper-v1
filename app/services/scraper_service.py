import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
from typing import cast

BASE_URL = "https://books.toscrape.com/"


def get_book_links(page_url: str) -> list:
    soup = fetch_soup(page_url)

    books = soup.find_all("h3")
    links = []

    for book in books:
        relative_url = book.find("a")["href"]
        full_url = urljoin(page_url, relative_url)
        links.append(full_url)

    return links


def fetch_soup(url: str) -> BeautifulSoup:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_categories() -> list:
    soup = fetch_soup(BASE_URL)

    categories_section = soup.find("div", class_="side_categories")

    if categories_section is None:
        raise ValueError("No se encontro la seccion de categorias")

    categories_section = cast(Tag, categories_section)

    links = categories_section.find_all("a")

    categories = []

    for link in links:
        name = link.get_text(strip=True)
        href = link.get("href")

        if href and "category" in href:
            full_url = urljoin(BASE_URL, href)

            categories.append({"name": name, "url": full_url})

    return categories


def get_books_data(book_url: str) -> dict:
    soup = fetch_soup(book_url)

    name_tag = soup.find("h1")
    if name_tag is None:
        raise ValueError("No se encomtro el nombre del libro")

    name = name_tag.get_text(strip=True)

    price_tag = soup.find("p", class_="price_color")
    if price_tag is None:
        raise ValueError("No se encontro el precio")

    price = float(price_tag.get_text(strip=True).replace("£", ""))

    availability_tag = soup.find("p", class_="instock availability")

    availability = (
        availability_tag.get_text(strip=True) if availability_tag else "No disponible"
    )

    rating_tag = soup.find("p", class_="star-rating")

    rating = "Sin rating"

    if rating_tag:
        clases = rating_tag.get("class", [])

        if len(clases) > 1:
            rating = clases[1]

    return {
        "name": name,
        "price": price,
        "availability": availability,
        "rating": rating,
        "url": book_url,
    }


def scrape_category(category: dict) -> list:
    books_data = []
    page_url = category["url"]

    while True:
        print(f"Scraping {page_url}")

        links = get_book_links(page_url)

        for link in links:
            try:
                book = get_books_data(link)
                book["category"] = category["name"]
                books_data.append(book)
            except Exception as e:
                print(f"Error en {link}: {e}")

        soup = fetch_soup(page_url)
        next_button = soup.find("li", class_="next")

        if next_button:
            next_link = next_button.find("a")

            if next_link is None:
                break

            href = next_link.get("href")
            if href is None:
                break

            page_url = urljoin(page_url, href)
        else:
            break

    return books_data
