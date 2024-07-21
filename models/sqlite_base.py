import sqlite3

conn = sqlite3.connect('../data/pokemon.sqlite')
conn.row_factory = sqlite3.Row

# Create a cursor object
cursor = conn.cursor()

