
import os
import httpx
import mysql.connector
from config import db_config
from mcp.server.fastmcp import FastMCP

def test_db_connection():
    """Test the MySQL database connection. Returns True if successful, else False."""
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        print("[INFO] Database connection successful.")
        return True
    except Exception as e:
        print(f"[FATAL] Could not connect to the database: {e}")
        return False

if not test_db_connection():
    import sys
    sys.exit(1)

mcp = FastMCP("naturalquery")

@mcp.tool()
def mysql_list_tables() -> list:
    """Read all tables in the current MySQL schema to find the relevant table based on human input."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        return [f"Error: {e}"]

@mcp.tool()
def mysql_describe_table(table_name: str) -> list:
    """Describe the structure of a given table in the current MySQL schema."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE `{table_name}`")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return [f"Error: {e}"]

@mcp.tool()
def mysql_execute_query(query: str) -> list:
    """Execute a MySQL query on the current schema. Returns result as list of rows."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description:
            result = cursor.fetchall()
        else:
            result = [f"{cursor.rowcount} rows affected."]
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return [f"Error: {e}"]

if __name__ == "__main__":
    mcp.run()
