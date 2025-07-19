import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

class TestLinkedInJobServer(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        
    def test_get_tools(self):
        response = self.client.get('/mcp/v1/tools')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tools', data)
        self.assertTrue(len(data['tools']) > 0)
        
    @patch('server.linkedin_client')
    def test_search_jobs(self, mock_linkedin):
        # Mock the LinkedIn client
        mock_linkedin.search_jobs.return_value = [
            {
                "job_id": "123456789",
                "title": "DevOps Engineer",
                "company": "Test Company",
                "location": "Test Location",
                "description_snippet": "Test description",
                "date_posted": "2025-07-15",
                "experience_level": "Mid-Senior",
                "job_type": "Full-time",
                "remote": True,
                "url": "https://www.linkedin.com/jobs/view/123456789"
            }
        ]
        
        # Set up the server's LinkedIn client
        server.linkedin_client = mock_linkedin
        
        # Make the request
        response = self.client.post('/mcp/v1/invoke', 
                                   json={
                                       'name': 'search_jobs',
                                       'parameters': {
                                           'title': 'DevOps Engineer',
                                           'location': 'London'
                                       }
                                   })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('jobs', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        
    def test_get_application_history(self):
        # Set up some test data
        server.application_history = [
            {
                "job_id": "123456789",
                "job_title": "DevOps Engineer",
                "company": "Test Company",
                "applied_at": "2025-07-19T10:00:00",
                "status": "applied"
            }
        ]
        
        # Make the request
        response = self.client.post('/mcp/v1/invoke',
                                   json={
                                       'name': 'get_application_history',
                                       'parameters': {}
                                   })
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('applications', data)
        self.assertEqual(len(data['applications']), 1)
        self.assertEqual(data['applications'][0]['job_id'], "123456789")
        
if __name__ == '__main__':
    unittest.main()
