import duckdb

# Connect to the DuckDB file
con = duckdb.connect('taxi_pipeline.duckdb')

# Calculate total trips
total_trips = con.execute('SELECT COUNT(*) FROM nyc_taxi_data_20260223012003.nyc_taxi_trips').fetchone()[0]

# Calculate trips paid with credit card
credit_card_trips = con.execute("SELECT COUNT(*) FROM nyc_taxi_data_20260223012003.nyc_taxi_trips WHERE payment_type = 'Credit'").fetchone()[0]

# Calculate proportion
proportion = (credit_card_trips / total_trips) * 100

# Print the result
print(f'Proportion of trips paid with credit card: {proportion:.2f}%')

# Close the connection
con.close()
