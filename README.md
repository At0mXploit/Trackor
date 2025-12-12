# Trackor

This is a custom MCP (Model Context Protocol) server built with **FastMCP**.  
It provides tools to track expenses, including adding, listing, summarizing, updating, and exporting data.

The server uses a local SQLite database (`expenses.db`) and a `categories.json` file for expense categories.
## Tools & Resources
```bash
TOOLS (callable actions that perform operations):
- add_expense                 : Create a new expense entry
- get_expense                 : Fetch a single expense by ID
- list_expenses               : List expenses with optional filters
- update_expense              : Modify an existing expense
- delete_expense              : Remove one expense by ID
- delete_expenses_by_date_range : Remove all expenses within a date range
- summarize                   : Summarize expenses by category/subcategory
- get_statistics              : Return overall stats and monthly breakdown
- export_expenses             : Export all expenses in JSON or CSV format

RESOURCES (read-only data exposed by the server):
- expense://categories        : Provides the categories.json file (list of categories/subcategories)
```

## Remote Deployment (Easiest)
It is already deployed using FastMCP Cloud, you just need to drag this DXT File  `https://at0mxploit.fastmcp.app/manifest.dxt` to Claude Extension. This automatically configures the server for Claude and includes all tools and resources. (Currently available only in Pro). It's setup for all different models and tools but I use Claude so.

<img width="829" height="366" alt="test" src="https://github.com/user-attachments/assets/bced55ea-eecb-4d9a-bd54-a7c44e498617" />

## Local Development

Claude Connectors (remote MCP URLs) are only available for Pro users. However, **non-Pro Claude Desktop users can still use this MCP server** by running a **local proxy**.

This repository includes a `proxy/` folder with a simple FastMCP STDIO bridge.

Install dependencies:

```bash
uv sync
```
Run MCP:

```bash
uv run main.py
```

Run MCP Proxy:

```bash
uv run proxy/main.py
```

We can also if we want use Inspector to test JSON RPC calls in MCP:

```bash
 uv run fastmcp dev .\main.py
```

Claude Desktop no longer auto-loads raw MCP scripts.  
If you're not using Claude Pro, you must install the included desktop extension:

```bash
npm install -g @anthropic-ai/mcpb
```

```bash
mcpb pack proxy/ trackor-proxy.mcpb
```

This will generate `trackor-proxy.mcpb`.

1. Go to Settings → Extensions → Advanced → Install Extension…
2. Select `trackor-proxy.mcpb`
3. Claude will load the MCP server via the local STDIO proxy.

---

