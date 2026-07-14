import os
import math
import time
from concurrent.futures import ProcessPoolExecutor


# ---------------------------------------
# CPU-Heavy Function
# ---------------------------------------

def score_genre(genre):
    """
    Simulates a CPU-intensive scoring calculation
    for a book genre.
    """

    score = 0

    # Heavy computation
    for i in range(1, 5_000_000):
        score += math.sqrt(i) * math.sin(i)

    return (genre, round(score, 2))


# ---------------------------------------
# Serial Version
# ---------------------------------------

def serial_processing(genres):

    results = []

    for genre in genres:
        results.append(score_genre(genre))

    return results


# ---------------------------------------
# Parallel Version
# ---------------------------------------

def parallel_processing(genres):

    with ProcessPoolExecutor() as executor:

        results = list(executor.map(score_genre, genres))

    return results


# ---------------------------------------
# Main Program
# ---------------------------------------

if __name__ == "__main__":

    genres = [
        "Python",
        "Java",
        "SQL",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "Cloud Computing",
        "Cyber Security"
    ]

    print("=" * 50)
    print("CPU Core Information")
    print("=" * 50)

    print(f"Available CPU Cores : {os.cpu_count()}")

    # ---------------------------------------
    # Serial Execution
    # ---------------------------------------

    print("\nRunning Serial Processing...\n")

    start = time.perf_counter()

    serial_results = serial_processing(genres)

    serial_time = time.perf_counter() - start

    print("Serial Results")

    for result in serial_results:
        print(result)

    print(f"\nSerial Time : {serial_time:.2f} seconds")


    # ---------------------------------------
    # Parallel Execution
    # ---------------------------------------

    print("\nRunning Parallel Processing...\n")

    start = time.perf_counter()

    parallel_results = parallel_processing(genres)

    parallel_time = time.perf_counter() - start

    print("Parallel Results")

    for result in parallel_results:
        print(result)

    print(f"\nParallel Time : {parallel_time:.2f} seconds")


    # ---------------------------------------
    # Verify Results
    # ---------------------------------------

    print("\nVerification")
    print("-" * 40)

    if serial_results == parallel_results:
        print("✔ Results Match")
    else:
        print("✘ Results Do Not Match")


    # ---------------------------------------
    # Performance Comparison
    # ---------------------------------------

    print("\nPerformance Comparison")
    print("-" * 40)

    print(f"CPU Cores     : {os.cpu_count()}")
    print(f"Serial Time   : {serial_time:.2f} seconds")
    print(f"Parallel Time : {parallel_time:.2f} seconds")

    if parallel_time < serial_time:
        print("\n✔ Parallel processing is faster.")
    else:
        print("\nParallel processing was not faster. This can happen on systems with a single CPU core or when process startup overhead outweighs the work.")



"""
Output
******
Verification
----------------------------------------
✔ Results Match

Performance Comparison
----------------------------------------
CPU Cores     : 12
Serial Time   : 4.96 seconds
Parallel Time : 2.31 seconds

"""