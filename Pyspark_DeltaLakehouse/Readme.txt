This solution reads a query plan and forces a broadcast join, creates a Delta table and travel through its history, rollbacks a mistake back with RESTORE,
compact and ZORDER for speed, builds the bronze, silver and gold layers, and loads a daily batch incrementally with MERGE operation.
