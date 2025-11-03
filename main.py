import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider
from starlette.exceptions import HTTPException
from dotenv import load_dotenv

load_dotenv()
MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", 5000))
MCP_PATH = os.getenv("MCP_PATH", "/mcp")
MCP_BASE_URL = os.getenv("MCP_BASE_URL", f"http://{MCP_HOST}:{MCP_PORT}")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REQUIRED_SCOPES = os.getenv("REQUIRED_SCOPES", "openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile")
REDIRECT_PATH = os.getenv("REDIRECT_PATH", "/auth/callback")
ALLOWED_CLIENT_REDIRECT_URIS = os.getenv("ALLOWED_CLIENT_REDIRECT_URIs", "http://localhost:*;http://127.0.0.1:*").split(";")
RESOURCE = f"{MCP_BASE_URL}/{MCP_PATH}"

google_auth = GoogleProvider(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    base_url=MCP_BASE_URL,
    redirect_path=REDIRECT_PATH,
    required_scopes=REQUIRED_SCOPES,
    allowed_client_redirect_uris=ALLOWED_CLIENT_REDIRECT_URIS,
)
mcp = FastMCP(
    name="simple_streamable_http_auth",
    instructions=(
        "This is a Protected MCP Server, that uses Google as an OAuth Provider."
    ),
    auth=google_auth,
)

@mcp.tool()
def my_profile() -> dict[str, str]:
    """
    This function is used whenever we want to get my(current user) profile.
    """

    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # print(token.claims)

    return {
        "name": token.claims.get("name"),
        "email": token.claims.get("email"),
        "picture": token.claims.get("picture"),
    }

@mcp.prompt()                       # MCP Prompts can be though of as Prompt Templates.
def get_cortexhub_mission_prompt(query: str) -> str:
    """
    Provide The Cortex Hub's mission statement.
    This is a static resource containing mission information.

    Args:
        query: The query to get the mission statement for.
    """

    return (
        "The Cortex Hub is a team of technologists who are passionate about building technology that helps people live better lives."
        f"Your query: {query}"
    )

@mcp.resource("data://cortexhub_contact",)
def get_cortexhub_contact() -> str:
    """
    Provide The Cortex Hub's contact information.
    This is a static resource containing contact information.
    """
    return "The Cortex Hub is a team of technologists who are passionate about building technology that helps people live better lives."

@mcp.resource("data://cortexhub_team_csv")
def get_cortexhub_team_csv() -> str:
    """
    Provide The Cortex Hub's team data as a CSV resource.
    This is a static resource containing team data.

    Args:
        arg: The name of the CSV file to read.
    """
    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        with open('sample.csv', 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Error: sample.csv not found in resources directory."
    except Exception as e:
        return f"Error reading sample.csv: {str(e)}"



if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=MCP_HOST,
        port=MCP_PORT,
        path=MCP_PATH,
        stateless_http=True,
    )