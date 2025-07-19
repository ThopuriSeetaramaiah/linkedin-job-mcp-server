# LinkedIn Job Application MCP Server

This MCP (Model Context Protocol) server allows you to search for DevOps engineer jobs on LinkedIn and automate the application process with your details.

## Features

- Search for DevOps engineer jobs on LinkedIn based on various criteria
- Filter jobs by location, experience level, and other parameters
- Automatically apply to selected jobs with your resume and details
- Track application status and history

## Setup

### Prerequisites

- Python 3.8+
- LinkedIn account
- AWS account (optional, for deployment)

### Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your LinkedIn credentials in `config.yaml`
4. Start the MCP server: `python server.py`

## Usage with Amazon Q

Once the MCP server is running, you can use it with Amazon Q CLI:

```bash
q chat --mcp-server http://localhost:8080
```

Then you can ask Amazon Q to:
- "Find DevOps engineer jobs in London"
- "Apply to the first 5 jobs with my profile"
- "Show me all jobs I've applied to"

## Configuration

Edit the `config.yaml` file to customize:
- Your LinkedIn credentials
- Resume and cover letter templates
- Job search preferences
- Application tracking settings

## Security Notice

This tool stores your LinkedIn credentials and personal information. Always ensure:
- The config file is properly secured
- You're running the server on a secure machine
- You review all applications before they're submitted

## License

MIT
