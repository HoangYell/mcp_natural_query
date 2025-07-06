## MCP Natural Query

> Talk to your database like it's human. Natural Language → SQL for MCP
> Basic example for using Model Context Protocol (MCP) with VS Code. This repo shows how to create your own MCP server and interact with it by chatting custom prompts to GitHub Copilot in VS Code.

### Features
- Query your MySQL database using natural language in VS Code chat.
- MCP server exposes tools for listing tables and executing SQL queries.

### Quickstart
1. **Clone & enter the repo**
   ```sh
   git clone git@github.com:HoangYell/mcp-natural-query.git
   cd mcp-natural-query
   ```
2. **Create & activate a virtual environment**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Configure environment**
   - In the project root, create a file named `.env` with your MySQL credentials:
     ```
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=example_password
     DB_NAME=example_schema
     DB_PORT=3306
     ```
4. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
5. **Configure VS Code**
   Add to your [settings.json](vscode://settings/chat.mcp.discovery.enabled):
   ```jsonc
   {
       "chat.mcp.discovery.enabled": true,
       "mcp": {
           "servers": {
               "mcp_natural_query": {
                   "type": "python",
                   "command": "/home/hoangyell/Projects/mcp_natural_query/.venv/bin/python",
                   "args": ["/home/hoangyell/Projects/mcp_natural_query/server.py"],
                   "cwd": "/home/hoangyell/Projects/mcp_natural_query"
               }
           }
       }
   }
   ```
6. **Run the server**  
   Press `CTRL + SHIFT + P` in VS Code
   > Type and select `MCP: List Servers`
   > Select `mcp_natural_query`  → Start Server

### Usage
- Connect via VS Code MCP chat or use the provided tools:
  - `mysql_list_tables()`: List all tables in the database
  - `mysql_describe_table(table_name)`: Show columns and types for a table
  - `mysql_execute_query(sql)`: Run any SQL query

---
**Example queries:**
- User: `use #mcp_natural_query what is the name of the most expensive order about motobike, and how much does it cost?`
- Copilot: 
```
The most expensive order about "motobike" is:

Customer: HoangYell.com
Order number: 10145
Total cost: $40,041.75
```
---
[![Demo Video](https://raw.githubusercontent.com/HoangGeek/store/refs/heads/main/github_copilot/mcp/mysql_mcp.png)](https://www.youtube.com/watch?v=9busJtM8C0A)
