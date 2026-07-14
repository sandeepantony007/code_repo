import requests


def get_books(subject, page):
    """
    Fetch books from the Open Library Search API.

    Args:
        subject (str): Search keyword.
        page (int): Page number.

    Returns:
        list: List of dictionaries containing book details.
    """

    url = "https://openlibrary.org/search.json"

    params = {
        "q": subject,
        "page": page,
        "limit": 10,
        "fields": "title,author_name,first_publish_year,ratings_average"
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
                "first_publish_year": book.get("first_publish_year"),
                "rating": book.get("ratings_average", "N/A")
            })

        return books

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

    return []


def full_load(subject):
    """
    Full Load:
    Reads only Page 4 and creates a watermark.
    """

    all_books = []

    page = 4

    print(f"\nReading Full Load - Page {page}")

    books = get_books(subject, page)

    if books:
        all_books.extend(books)

    print(f"\nTotal books loaded: {len(all_books)}")

    # Calculate watermark (latest publish year)
    years = []

    for book in all_books:
        if book["first_publish_year"] is not None:
            years.append(book["first_publish_year"])

    watermark = max(years) if years else None

    print(f"Watermark (Latest Publish Year): {watermark}")

    return all_books, watermark


def incremental_load(subject, watermark):
    """
    Incremental Load:
    Reads only Page 5 and loads books newer than watermark.
    """

    page = 5

    print(f"\nReading Incremental Load - Page {page}")

    books = get_books(subject, page)

    incremental_books = []

    for book in books:

        publish_year = book["first_publish_year"]

        if (
            publish_year is not None
            and watermark is not None
            and publish_year > watermark
        ):
            incremental_books.append(book)

    return incremental_books


# -----------------------------
# Main Program
# -----------------------------

if __name__ == "__main__":

    subject = "python"

    # Full Load
    full_books, watermark = full_load(subject)

    print("\nBooks from Full Load\n")

    for book in full_books:
        print(book)

    # Incremental Load
    print("\nRunning Incremental Load...\n")

    new_books = incremental_load(subject, watermark)

    print(f"New Books Found: {len(new_books)}\n")

    for book in new_books:
        print(book)