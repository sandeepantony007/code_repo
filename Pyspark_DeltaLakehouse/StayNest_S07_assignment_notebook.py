# Databricks notebook source
# MAGIC %md
# MAGIC # StayNest - Session 7 Assignment (Delta Lake & Lakehouse)
# MAGIC Work through the 8 tasks in order. Read the Assignment Questions PDF for the full
# MAGIC detail and acceptance criteria. Fill each `# TODO` cell, run it, and keep the output
# MAGIC visible. Runs on Databricks Free Edition (serverless).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Section 0 - Setup (already done for you)
# MAGIC Upload `bookings.csv`, `hotels.csv`, `bookings_updates.csv` to a Volume, set `BASE`,
# MAGIC `CATALOG`, `SCHEMA`, and run this cell. Expect 12000 / 200 / 200.

# COMMAND ----------

BASE    = "/Volumes/workspace/default/staynest"
CATALOG = "workspace"
SCHEMA  = "default"
FQN = lambda name: f"{CATALOG}.{SCHEMA}.{name}"

read_csv = lambda name: (spark.read
    .option("header", True).option("inferSchema", True)
    .csv(f"{BASE}/{name}.csv"))

bookings_df = read_csv("bookings")
hotels_df   = read_csv("hotels")
updates_df  = read_csv("bookings_updates")

print(f"bookings: {bookings_df.count()}, hotels: {hotels_df.count()}, "
      f"updates: {updates_df.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 1 - Read the plan and force a broadcast join
# MAGIC Join bookings to hotels and call `.explain()` to see the plan. Then force a
# MAGIC broadcast join with `broadcast(hotels_df)` and `.explain()` again. In a comment,
# MAGIC say which join each plan used and why broadcast avoids a shuffle.
# MAGIC (Tip: hotels also has a `city` column, so `hotels_df.drop("city")` before joining.)

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 2 - Create a Delta table, then read its history
# MAGIC Write `bookings_df` as a managed Delta table with `saveAsTable`. Then create some
# MAGIC history: run an `UPDATE` (set pending to completed) and a `DELETE` (remove
# MAGIC cancelled). Show `DESCRIBE HISTORY` and point out the versioned commits.

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 3 - Time travel and RESTORE
# MAGIC Read the table as it was at **version 0** (before your UPDATE and DELETE) and show
# MAGIC its count. Then `RESTORE` the table to version 0 and confirm the count is back.
# MAGIC Show that RESTORE appears as a new commit in the history.

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 4 - OPTIMIZE and ZORDER
# MAGIC Run `OPTIMIZE` on your Delta table to compact files. Then run
# MAGIC `OPTIMIZE ... ZORDER BY (city)`. In a comment, say what OPTIMIZE does and why
# MAGIC `city` is a good ZORDER column but `status` would not be.

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5 - Bronze: land the raw data
# MAGIC Write the raw bookings to a `bronze_bookings` Delta table, keeping every row and
# MAGIC adding an `ingested_at` timestamp column.

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 6 - Silver: clean and conform
# MAGIC Build `silver_bookings` from bronze: keep only completed bookings and join the
# MAGIC hotel dimension to add `category`, `star_rating`, and the hotel name. Drop the
# MAGIC duplicate `city` from the hotel side so the join has a single `city`.

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 7 - Gold: business-ready aggregate
# MAGIC From silver, build a `gold_city_revenue` Delta table: bookings and total revenue
# MAGIC per city, ordered by revenue.

# COMMAND ----------

# TODO


# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 8 - Incremental load with MERGE
# MAGIC You have today's batch in `updates_df` (150 changed bookings + 50 new ones).
# MAGIC `MERGE` it into your Delta table: update matched booking_ids, insert new ones, in
# MAGIC one command. Report the row count before and after (it should grow by the 50 new).

# COMMAND ----------

# TODO

