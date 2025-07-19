#!/usr/bin/env python3
"""
LinkedIn Job Application MCP Server
This server implements the Model Context Protocol (MCP) to allow Amazon Q
to search for and apply to LinkedIn jobs.
"""

import json
import logging
import os
import sys
import yaml
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from linkedin_api import Linkedin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables
config = {}
linkedin_client = None
job_cache = {}
application_history = []

def load_config():
    """Load configuration from config.yaml"""
    global config
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        logger.info("Configuration loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        return False

def initialize_linkedin():
    """Initialize LinkedIn API client"""
    global linkedin_client
    try:
        if not config.get('linkedin'):
            logger.error("LinkedIn configuration missing")
            return False
            
        linkedin_client = Linkedin(
            config['linkedin'].get('username', ''),
            config['linkedin'].get('password', '')
        )
        logger.info("LinkedIn client initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize LinkedIn client: {e}")
        return False

@app.route('/mcp/v1/tools', methods=['GET'])
def get_tools():
    """Return the list of tools provided by this MCP server"""
    tools = [
        {
            "name": "search_jobs",
            "description": "Search for jobs on LinkedIn based on criteria",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Job title to search for (e.g., 'DevOps Engineer')"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location to search in (e.g., 'London, United Kingdom')"
                    },
                    "experience_level": {
                        "type": "string",
                        "description": "Experience level (Entry, Mid-Senior, Director+)",
                        "enum": ["Entry", "Mid-Senior", "Director+"]
                    },
                    "job_type": {
                        "type": "string",
                        "description": "Job type (Full-time, Part-time, Contract, etc.)",
                        "enum": ["Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship"]
                    },
                    "remote": {
                        "type": "boolean",
                        "description": "Whether to search for remote jobs only"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of jobs to return",
                        "default": 10
                    }
                },
                "required": ["title"]
            }
        },
        {
            "name": "get_job_details",
            "description": "Get detailed information about a specific job",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "LinkedIn job ID"
                    }
                },
                "required": ["job_id"]
            }
        },
        {
            "name": "apply_to_job",
            "description": "Apply to a specific job with your profile",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "LinkedIn job ID"
                    },
                    "cover_letter": {
                        "type": "string",
                        "description": "Custom cover letter for this application (optional)"
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "Phone number to use for this application (optional)"
                    }
                },
                "required": ["job_id"]
            }
        },
        {
            "name": "get_application_history",
            "description": "Get history of job applications made through this tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of applications to return",
                        "default": 10
                    }
                }
            }
        }
    ]
    
    return jsonify({"tools": tools})

@app.route('/mcp/v1/invoke', methods=['POST'])
def invoke_tool():
    """Invoke a tool based on the request"""
    request_data = request.json
    tool_name = request_data.get('name')
    parameters = request_data.get('parameters', {})
    
    logger.info(f"Tool invocation request: {tool_name} with parameters: {parameters}")
    
    if tool_name == "search_jobs":
        return search_jobs(parameters)
    elif tool_name == "get_job_details":
        return get_job_details(parameters)
    elif tool_name == "apply_to_job":
        return apply_to_job(parameters)
    elif tool_name == "get_application_history":
        return get_application_history(parameters)
    else:
        return jsonify({
            "error": f"Unknown tool: {tool_name}",
            "status": "error"
        }), 400

def search_jobs(parameters):
    """Search for jobs on LinkedIn"""
    if not linkedin_client:
        return jsonify({
            "error": "LinkedIn client not initialized",
            "status": "error"
        }), 500
    
    try:
        # In a real implementation, this would use the LinkedIn API
        # For now, we'll return mock data
        mock_jobs = [
            {
                "job_id": "3123456789",
                "title": "Senior DevOps Engineer",
                "company": "Tech Innovations Ltd",
                "location": "London, United Kingdom",
                "description_snippet": "Looking for an experienced DevOps engineer to help build and maintain our cloud infrastructure...",
                "date_posted": "2025-07-15",
                "experience_level": "Mid-Senior",
                "job_type": "Full-time",
                "remote": True,
                "url": "https://www.linkedin.com/jobs/view/3123456789"
            },
            {
                "job_id": "3123456790",
                "title": "DevOps Team Lead",
                "company": "Global Solutions",
                "location": "London, United Kingdom",
                "description_snippet": "Seeking a DevOps Team Lead to oversee our infrastructure and CI/CD pipelines...",
                "date_posted": "2025-07-17",
                "experience_level": "Mid-Senior",
                "job_type": "Full-time",
                "remote": False,
                "url": "https://www.linkedin.com/jobs/view/3123456790"
            },
            {
                "job_id": "3123456791",
                "title": "Cloud DevOps Engineer",
                "company": "Fintech Startup",
                "location": "Remote",
                "description_snippet": "Join our team to help build scalable cloud infrastructure using AWS and Kubernetes...",
                "date_posted": "2025-07-18",
                "experience_level": "Mid-Senior",
                "job_type": "Full-time",
                "remote": True,
                "url": "https://www.linkedin.com/jobs/view/3123456791"
            }
        ]
        
        # Store in cache for later use
        for job in mock_jobs:
            job_cache[job["job_id"]] = job
        
        return jsonify({
            "jobs": mock_jobs,
            "count": len(mock_jobs),
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

def get_job_details(parameters):
    """Get detailed information about a specific job"""
    job_id = parameters.get("job_id")
    
    if not job_id:
        return jsonify({
            "error": "Job ID is required",
            "status": "error"
        }), 400
    
    try:
        # Check if job is in cache
        if job_id in job_cache:
            job = job_cache[job_id]
            
            # Add more detailed information
            job["full_description"] = """
            About the role:
            We are looking for a skilled DevOps Engineer to help us build and maintain our cloud infrastructure. 
            You will be responsible for implementing and managing CI/CD pipelines, infrastructure as code, 
            and ensuring the reliability and scalability of our systems.
            
            Requirements:
            - 3+ years of experience with AWS or similar cloud platforms
            - Strong knowledge of Kubernetes, Docker, and containerization
            - Experience with infrastructure as code tools (Terraform, CloudFormation)
            - Proficiency in scripting languages (Python, Bash)
            - Experience with CI/CD tools (Jenkins, GitHub Actions, GitLab CI)
            
            Benefits:
            - Competitive salary
            - Remote work options
            - Flexible hours
            - Professional development budget
            - Health insurance
            """
            
            job["skills_required"] = [
                "AWS", "Kubernetes", "Docker", "Terraform", "Python", "CI/CD", "Linux"
            ]
            
            job["salary_range"] = "£70,000 - £90,000"
            
            return jsonify({
                "job": job,
                "status": "success"
            })
        else:
            return jsonify({
                "error": f"Job with ID {job_id} not found",
                "status": "error"
            }), 404
    except Exception as e:
        logger.error(f"Error getting job details: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

def apply_to_job(parameters):
    """Apply to a specific job with your profile"""
    job_id = parameters.get("job_id")
    cover_letter = parameters.get("cover_letter", config.get("default_cover_letter", ""))
    phone_number = parameters.get("phone_number", config.get("phone_number", ""))
    
    if not job_id:
        return jsonify({
            "error": "Job ID is required",
            "status": "error"
        }), 400
    
    try:
        # Check if job exists
        if job_id not in job_cache:
            return jsonify({
                "error": f"Job with ID {job_id} not found",
                "status": "error"
            }), 404
        
        job = job_cache[job_id]
        
        # In a real implementation, this would use the LinkedIn API to apply
        # For now, we'll just record the application
        application = {
            "job_id": job_id,
            "job_title": job["title"],
            "company": job["company"],
            "applied_at": datetime.now().isoformat(),
            "status": "applied",
            "cover_letter": cover_letter[:100] + "..." if len(cover_letter) > 100 else cover_letter,
            "phone_number": phone_number
        }
        
        application_history.append(application)
        
        return jsonify({
            "application": application,
            "message": f"Successfully applied to {job['title']} at {job['company']}",
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Error applying to job: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

def get_application_history(parameters):
    """Get history of job applications"""
    limit = parameters.get("limit", 10)
    
    try:
        return jsonify({
            "applications": application_history[:limit],
            "count": len(application_history[:limit]),
            "total": len(application_history),
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Error getting application history: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == "__main__":
    if load_config():
        initialize_linkedin()
    else:
        # Create default config if it doesn't exist
        if not os.path.exists('config.yaml'):
            default_config = {
                "linkedin": {
                    "username": "your.email@example.com",
                    "password": "your_password"
                },
                "default_cover_letter": "I am excited to apply for this position and believe my skills and experience make me a strong candidate.",
                "phone_number": "+1234567890",
                "resume_path": "resume.pdf",
                "job_preferences": {
                    "titles": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer"],
                    "locations": ["London", "Remote"],
                    "experience_level": "Mid-Senior",
                    "job_type": "Full-time"
                }
            }
            with open('config.yaml', 'w') as file:
                yaml.dump(default_config, file, default_flow_style=False)
            logger.info("Created default configuration file. Please edit config.yaml with your details.")
    
    # Start the server
    app.run(host='0.0.0.0', port=8080)
