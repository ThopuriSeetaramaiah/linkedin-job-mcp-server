#!/usr/bin/env python3
"""
Setup Profile Script
This script helps users set up their profile for the LinkedIn Job Application MCP Server.
"""

import os
import yaml
import getpass
from pathlib import Path

def main():
    print("LinkedIn Job Application MCP Server - Profile Setup")
    print("=" * 50)
    print("This script will help you set up your profile for job applications.")
    print("Your information will be stored in the config.yaml file.")
    print("=" * 50)
    
    # Check if config file exists
    config_path = Path("config.yaml")
    config = {}
    
    if config_path.exists():
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        print("Existing configuration found. You can update your information.")
    
    # LinkedIn credentials
    print("\nLinkedIn Credentials")
    print("-" * 20)
    linkedin_username = input("LinkedIn Email/Username: ")
    linkedin_password = getpass.getpass("LinkedIn Password: ")
    
    # Personal information
    print("\nPersonal Information")
    print("-" * 20)
    name = input("Full Name: ")
    email = input("Email: ")
    phone = input("Phone Number: ")
    location = input("Location (e.g., London, United Kingdom): ")
    linkedin_profile = input("LinkedIn Profile URL: ")
    github_profile = input("GitHub Profile URL (optional): ")
    
    # Resume
    print("\nResume")
    print("-" * 20)
    resume_path = input("Path to your resume PDF (leave blank to add later): ")
    
    # Job preferences
    print("\nJob Preferences")
    print("-" * 20)
    print("Enter job titles you're interested in (comma-separated):")
    job_titles_input = input("(e.g., DevOps Engineer, SRE, Cloud Engineer): ")
    job_titles = [title.strip() for title in job_titles_input.split(",")]
    
    print("Enter locations you're interested in (comma-separated):")
    locations_input = input("(e.g., London, Remote): ")
    locations = [location.strip() for location in locations_input.split(",")]
    
    experience_level = input("Experience Level (Entry, Mid-Senior, Director+): ")
    job_type = input("Job Type (Full-time, Part-time, Contract, etc.): ")
    remote_only = input("Remote Only? (yes/no): ").lower() == "yes"
    
    # Update configuration
    config["linkedin"] = {
        "username": linkedin_username,
        "password": linkedin_password
    }
    
    config["personal_info"] = {
        "name": name,
        "email": email,
        "phone_number": phone,
        "location": location,
        "linkedin_profile": linkedin_profile,
        "github_profile": github_profile
    }
    
    if resume_path:
        config["resume_path"] = resume_path
    
    config["job_preferences"] = {
        "titles": job_titles,
        "locations": locations,
        "experience_level": experience_level,
        "job_type": job_type,
        "remote_only": remote_only
    }
    
    # Default cover letter template
    if "default_cover_letter" not in config:
        config["default_cover_letter"] = """
Dear Hiring Manager,

I am writing to express my interest in the [JOB_TITLE] position at [COMPANY_NAME]. With my background in DevOps engineering, cloud infrastructure, and automation, I believe I would be a valuable addition to your team.

My experience includes:
- Designing and implementing CI/CD pipelines
- Managing Kubernetes clusters in production environments
- Infrastructure as Code using Terraform and CloudFormation
- Monitoring and observability solutions
- Cloud security best practices

I am particularly interested in [COMPANY_NAME] because of your innovative approach to technology. I am confident that my skills and enthusiasm would make me a strong candidate for this position.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.

Sincerely,
[YOUR_NAME]
"""
    
    # Save configuration
    with open(config_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False)
    
    print("\nProfile setup complete! Your information has been saved to config.yaml.")
    print("You can edit this file directly to make further changes.")
    print("\nTo start the MCP server, run: python server.py")

if __name__ == "__main__":
    main()
