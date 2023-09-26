import unittest
from unittest.mock import Mock, patch
import requests
import json
from main import GitHubCrawler


class TestGitHubCrawler(unittest.TestCase):
    def setUp(self):
        # Sample input data for testing
        self.keywords = ["openstack", "nova"]
        self.proxies = ["194.126.37.94:8080", "13.78.125.167:8080"]
        self.search_type = "repositories"
        self.json_data = {
            "keywords": self.keywords,
            "proxies": self.proxies,
            "type": self.search_type
        }

    @patch('main.requests.get')
    def test_search_github_with_valid_response(self, mock_requests_get):
        # Mock the requests.get() method to return a valid response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "payload": {
                "results": [
                    {
                        "repo": {
                            "repository": {
                                "owner_login": "olegbuno",
                                "name": "GithubCrawler"
                            }
                        },
                        "language": "Python"
                    }
                ]
            }
        })
        mock_requests_get.return_value = mock_response

        # Initialize the crawler
        crawler = GitHubCrawler(self.keywords, self.proxies, self.search_type)

        # Run the search_github() method
        crawler.search_github()

        # Check if the results contain the expected data
        results = crawler.get_results()
        expected_result = {
            "url": "https://github.com/olegbuno/GithubCrawler",
            "extra": {
                "owner": "olegbuno",
                "language": "Python"
            }
        }
        self.assertIn(expected_result, results)

    @patch('main.requests.get')
    def test_search_github_with_http_error(self, mock_requests_get):
        # Mock the requests.get() method to raise an HTTP error
        mock_requests_get.side_effect = requests.exceptions.HTTPError("HTTP error")

        # Initialize the crawler
        crawler = GitHubCrawler(self.keywords, self.proxies, self.search_type)

        # Run the search_github() method
        crawler.search_github()

        # Check if the results are empty
        results = crawler.get_results()
        self.assertEqual(results, [])

    @patch('main.requests.get')
    def test_search_github_with_invalid_json(self, mock_requests_get):
        # Mock the requests.get() method to return an invalid JSON response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Invalid JSON"
        mock_requests_get.return_value = mock_response

        # Initialize the crawler
        crawler = GitHubCrawler(self.keywords, self.proxies, self.search_type)

        # Run the search_github() method
        crawler.search_github()

        # Check if the results are empty
        results = crawler.get_results()
        self.assertEqual(results, [])

    @patch('main.requests.get')
    def test_search_github_with_value_error(self, mock_requests_get):
        # Mock the requests.get() method to return an invalid Value response
        mock_requests_get.side_effect = ValueError("JSON decoding error")

        # Initialize the crawler
        crawler = GitHubCrawler(self.keywords, self.proxies, self.search_type)

        # Run the search_github() method
        crawler.search_github()

        # Check if the results are empty
        results = crawler.get_results()
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
