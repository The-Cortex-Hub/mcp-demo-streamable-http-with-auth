# MCP HTTP Auth Server

## Quick Start

### Start the Server
```bash
uv run main.py
```

### Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector http://127.0.0.1:5000/mcp
```

### Test Endpoints
```bash
# Test MCP endpoint
curl -i http://127.0.0.1:5000/mcp

# Test OAuth protected resource discovery
curl -s http://127.0.0.1:5000/.well-known/oauth-protected-resource | jq

# Test OAuth authorization server discovery
curl -s http://127.0.0.1:5000/.well-known/oauth-authorization-server | jq
```

### Workflow for Testing OAuth
1. Run one of the clear methods above
2. Close Cursor completely
3. Reopen Cursor
4. Try connecting to your MCP server again
5. The authentication flow will start fresh

## Configuration

The server uses the following environment variables (with defaults):
- `MCP_HOST`: Server host (default: "127.0.0.1")
- `MCP_PORT`: Server port (default: 5000)
- `MCP_PATH`: MCP endpoint path (default: "/mcp")
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `REQUIRED_SCOPES`: OAuth scopes (default: "openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile")
