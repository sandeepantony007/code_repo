import requests


def get_books(subject, page):
    """
    Fetch books from the Open Library Search API.

    Args:
        subject (str): Subject to search.
        page (int): Page number.

    Returns:
        list: List of book dictionaries.
    """

    url = "https://openlibrary.org/search.json"

    params = {
        "q": subject,
        "page": page,
        "limit": 10,
        "fields": "title,author_name,first_publish_year,ratings_average,edition_count"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        books = []

        for book in data.get("docs", []):
            books.append({
                "title": book.get("title", "N/A"),
                "author": ", ".join(book.get("author_name", ["Unknown"])),
                "first_publish_year": book.get("first_publish_year", "N/A"),
                "rating": book.get("ratings_average", "N/A")
            })

        return books

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except ValueError:
        print("Error: Invalid JSON response.")

    return []


if __name__ == "__main__":
    books = get_books("python", 1)

    print("Books:\n")

    for book in books[:5]:
        print(f"Title : {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Year  : {book['first_publish_year']}")
        print(f"Rating: {book['rating']}")
        print("-" * 40)