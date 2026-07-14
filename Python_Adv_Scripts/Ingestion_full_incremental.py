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


"""
Sample Output:
Total books loaded: 10
Watermark (Latest Publish Year): 2021

Books from Full Load

{'title': 'Python in a Nutshell', 'author': 'Alex Martelli, Anna Ravenscroft, Steve Holden', 'first_publish_year': 2002, 'rating': 3.0}
{'title': 'Python Programming', 'author': 'Reema Thareja', 'first_publish_year': 2019, 'rating': 'N/A'}
{'title': 'Starting out with Python', 'author': 'Tony Gaddis', 'first_publish_year': 2008, 'rating': 'N/A'}
{'title': 'Deep Learning with Python', 'author': 'Francois Chollet, Matthew Watson', 'first_publish_year': 2017, 'rating': 3.0}
{'title': 'The Python Project', 'author': 'Victor Canning', 'first_publish_year': 1967, 'rating': 'N/A'}
{'title': 'Python for Kids', 'author': 'Jason R. Briggs', 'first_publish_year': 2012, 'rating': 5.0}
{'title': 'PYTHON Exercises', 'author': 'Ray Yao', 'first_publish_year': 2021, 'rating': 'N/A'}
{'title': 'Python programming', 'author': 'John M. Zelle', 'first_publish_year': 2003, 'rating': 'N/A'}
{'title': 'Michael Palin Diaries 1969-1979', 'author': 'Michael Palin', 'first_publish_year': 2006, 'rating': 3.5}
{'title': 'Python Data Science Handbook', 'author': 'Jake VanderPlas', 'first_publish_year': 2016, 'rating': 4.0}

Running Incremental Load...


Reading Incremental Load - Page 5
New Books Found: 1
"""
