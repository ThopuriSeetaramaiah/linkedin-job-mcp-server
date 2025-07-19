# Using the LinkedIn Job MCP Server with Amazon Q

This guide explains how to use the LinkedIn Job MCP Server with Amazon Q to search for and apply to jobs.

## Setup

1. Start the MCP server:
   ```bash
   python server.py
   ```

2. Connect Amazon Q to the MCP server:
   ```bash
   q chat --mcp-server http://localhost:8080
   ```

## Example Prompts

Here are some example prompts you can use with Amazon Q once connected to the MCP server:

### Searching for Jobs

```
Find DevOps Engineer jobs in London
```

```
Search for remote Cloud Engineer positions
```

```
Look for DevOps jobs that require Kubernetes experience
```

### Getting Job Details

```
Show me details for job ID 3123456789
```

```
What are the requirements for the Cloud DevOps Engineer position?
```

### Applying to Jobs

```
Apply to the Senior DevOps Engineer job at Tech Innovations Ltd
```

```
Submit my application for job ID 3123456790 with a custom cover letter that emphasizes my AWS experience
```

### Tracking Applications

```
Show me all the jobs I've applied to
```

```
What's the status of my recent job applications?
```

## Advanced Usage

### Customizing Job Search

```
Find DevOps jobs in London that are remote and full-time
```

```
Search for entry-level DevOps positions that don't require extensive experience
```

### Tailoring Applications

```
Apply to the Cloud Engineer job and mention my Kubernetes certification in the cover letter
```

```
Submit my application to the Platform Engineer position and highlight my experience with CI/CD pipelines
```

## Tips

- Be specific about job titles, locations, and other criteria when searching
- Ask for job details before applying to ensure it's a good fit
- You can request customized cover letters for specific applications
- Track your application history to follow up appropriately
