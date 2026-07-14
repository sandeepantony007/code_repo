import pandas as pd

# ------------------------------------------
# File Path
# ------------------------------------------

FILE_NAME = r"C:\Users\sande\codebasics-de\API_Ingestion\sales.csv"

# ------------------------------------------
# Chunk Size
# ------------------------------------------

CHUNK_SIZE = 5000

# Dictionary to store total revenue by genre
genre_revenue = {}

# ------------------------------------------
# Read CSV in Chunks
# ------------------------------------------

print("Reading file in chunks...\n")

for chunk in pd.read_csv(FILE_NAME, chunksize=CHUNK_SIZE):

    # Revenue = Quantity × Unit Price
    chunk["revenue"] = chunk["quantity"] * chunk["price"]

    # Sum revenue by genre for this chunk
    revenue = chunk.groupby("genre")["revenue"].sum()

    # Merge into overall totals
    for genre, total in revenue.items():

        if genre not in genre_revenue:
            genre_revenue[genre] = total
        else:
            genre_revenue[genre] += total

# ------------------------------------------
# Display Final Revenue
# ------------------------------------------

print("Total Revenue by Genre")
print("-" * 35)

for genre, revenue in genre_revenue.items():
    print(f"{genre:20} ${revenue:,.2f}")


# ==========================================
# Memory Optimization Demonstration
# ==========================================

print("\nMemory Optimization Example")
print("-" * 35)

# Read only one chunk
chunk = next(pd.read_csv(FILE_NAME, chunksize=CHUNK_SIZE))

# Memory before optimization
memory_before = chunk.memory_usage(deep=True).sum()

print(f"Memory Before : {memory_before:,} bytes")

# ------------------------------------------
# Optimize Data Types
# ------------------------------------------

# Convert float64 → float32
chunk["price"] = chunk["price"].astype("float32")

# Convert object → category
chunk["genre"] = chunk["genre"].astype("category")

# Memory after optimization
memory_after = chunk.memory_usage(deep=True).sum()

print(f"Memory After  : {memory_after:,} bytes")

reduction = ((memory_before - memory_after) / memory_before) * 100

print(f"Memory Reduced: {reduction:.2f}%")



"""
Output
********

Memory Optimization Example
-----------------------------------
Memory Before : 1,574,703 bytes
Memory After  : 1,277,760 bytes
Memory Reduced: 18.86%
"""