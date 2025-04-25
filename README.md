# mcp-docs-rag
A lightweight MCP (Model Context Protocol) server that loads PDF files from a local folder, extracts and chunks their content, builds a semantic search index, and sends relevant passages to Claude Desktop for document-based question answering.

This project is intended to be used with **Claude's MCP desktop feature**.

---

## Features
- Loads and processes PDF documents from a local *docs/* folder
- Extracts text and splits it into semantic chunks
- Generates vector embeddings using SentenceTransformer
- Builds a FAISS-based vector index for semantic search
- Retrieves top-k relevant chunks based on user query
- Constructs a prompt (relevant passages + question) and returns it to Claude
- Minimal setup using [uv](https://github.com/astral-sh/uv)

---

## How to Use

### 1. Install Claude Desktop (if not installed)
- Download [Claude Desktop](https://claude.ai/download) and install it.

### 2. Download `mcp-docs-reader`
**Option 1: Download as ZIP**
- Click **"Code"** > **"Download ZIP"**
- Extract the downloaded ZIP file

**Option 2: Clone with Git**
```sh
git clone https://github.com/AIMIZING/mcp_docs_reader.git
cd mcp_docs_reader
```

### 3. Set Up UV Environment
**Option 1: Manual Setup**
- Install uv (if not installed):
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
- Set up the virtual environment:
```sh
uv venv
.venv\Scripts\activate
```
- Install dependencies:
```sh
pip install -r requirements.txt
```

**Option 2: Automatic Setup (Windows)**
- run the included **"setup.bat"** file

### 4. Configure Claude Desktop
Open the included **"weather_config.json"** file, and copy its content.
Then, open your existing Claude Desktop configuration file and append the copied content.

To locate the Claude Desktop config file:
- Open Claude Desktop
- Go to Menu → File → Settings → Developer Mode → Edit Configuration
- This will open your current **"claude_desktop_config.json"** file
- Paste the additional content at the appropriate position (e.g. within the mcp list or relevant section)

⚠️ Before copying, make sure to replace the path
"C:\\PATH\\TO\\mcp_docs_reader" in docReader_config.json
with your actual local project path (e.g. C:\\Users\\YourName\\Documents\\mcp_docs_reader).

⚠️ Do not overwrite the entire file — make sure to append or merge the content to avoid breaking existing configurations.

### 5. Run Claude Desktop
Launch Claude Desktop.
Once it's running, it will automatically detect and connect to the configured MCP tool.
You can now ask Claude questions based on your local PDF documents, like:

> "Summarize the key points from the registered file contents."