import asyncio
import requests
import time

BASE_URL = "https://openlibrary.org/search.json"


def get_result_count(subject):
    """
    Returns the total number of books found for a subject.
    """

    params = {
        "q": subject,
        "limit": 1
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "subject": subject,
            "count": data.get("numFound", 0)
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching '{subject}': {e}")
        return {
            "subject": subject,
            "count": 0
        }


# ---------------------------
# Sync Version
# ---------------------------

def fetch_sync(subjects):

    results = []

    for subject in subjects:
        results.append(get_result_count(subject))

    return results


# ---------------------------
# Async Version
# ---------------------------

async def fetch_async(subjects):

    tasks = []

    for subject in subjects:
        task = asyncio.to_thread(get_result_count, subject)
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    return results


# ---------------------------
# Main Program
# ---------------------------

if __name__ == "__main__":

    subjects = [
        "python",
        "java",
        "machine learning",
        "data science",
        "artificial intelligence",
        "sql"
    ]

    # ---------------------------
    # Sync Timing
    # ---------------------------

    print("Running Synchronous Calls...\n")

    start = time.perf_counter()

    sync_results = fetch_sync(subjects)

    sync_time = time.perf_counter() - start

    for result in sync_results:
        print(result)

    print(f"\nSync Time : {sync_time:.2f} seconds")


    # ---------------------------
    # Async Timing
    # ---------------------------

    print("\nRunning Asynchronous Calls...\n")

    start = time.perf_counter()

    async_results = asyncio.run(fetch_async(subjects))

    async_time = time.perf_counter() - start

    for result in async_results:
        print(result)

    print(f"\nAsync Time : {async_time:.2f} seconds")


    # ---------------------------
    # Comparison
    # ---------------------------

    print("\nPerformance Comparison")
    print("-" * 30)
    print(f"Sync Time :  {sync_time:.2f} seconds")
    print(f"Async Time:  {async_time:.2f} seconds")

    if async_time < sync_time:
        print("\nAsync execution is faster.")
    else:
        print("\nSync execution was faster (network conditions may vary).")



"""Output
*********

Performance Comparison
------------------------------
Sync Time :  8.08 seconds
Async Time:  4.92 seconds

Async execution is faster.
"""