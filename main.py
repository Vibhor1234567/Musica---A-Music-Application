import oracledb
import traceback

from oracledb import init_oracle_client

conn = None
try:
    init_oracle_client()
    conn = oracledb.connect("mouzikka/music@localhost:1522/xe")
    print("Connected successfully to the database")
    print("Database version:", conn.version)
    print("Database user:", conn.username)

except oracledb.DatabaseError:
    print("Database Error")
    print(traceback.format_exc())

finally:
    if conn is not None:
        conn.close()
        print("Disconnected successfully from the database ")