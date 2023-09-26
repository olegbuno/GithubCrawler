import json
import random

import requests


class GitHubCrawler:
    def __init__(self, keywords: list, proxies: list, search_type: str) -> None:
        self.keywords = keywords
        self.proxies = proxies
        self.search_type = search_type.lower()
        self.base_url = "https://github.com"
        self.results = []

    def _get_random_proxy(self) -> str:
        return random.choice(self.proxies)

    def search_github(self) -> None:
        proxy = self._get_random_proxy()
        for keyword in self.keywords:
            search_url = f"{self.base_url}/search?type={self.search_type}&q={keyword}"

            try:
                response = requests.get(search_url, proxies={'http': proxy, 'https': proxy})

                # Check if the response content is not empty and convert JSON to dict
                if response.status_code == 200:
                    data_dict = json.loads(response.text)
                    for link in data_dict["payload"]["results"]:
                        owner = link["repo"]["repository"].get("owner_login", "")
                        repo_name = link["repo"]["repository"].get("name", "")
                        language = link.get("language", "")
                        url = ""

                        # Get proper URL by search_type
                        if self.search_type == "repositories":
                            url = f"{self.base_url}/{owner}/{repo_name}"
                        elif self.search_type == "issues":
                            issue_number = link["number"]
                            url = f"{self.base_url}/{owner}/{repo_name}/issues/{issue_number}"
                        elif self.search_type == "wikis":
                            wiki_number = link["title"]
                            url = f"{self.base_url}/{owner}/{repo_name}/wiki/{wiki_number}"
                        else:
                            print(f"{self.search_type} is not valid")

                        # Add the output to the result list
                        self.results.append({
                            "url": url,
                            "extra": {
                                "owner": owner,
                                "language": language
                            }
                        })
                else:
                    print(f"No results found for '{keyword}'")
            except requests.exceptions.HTTPError as http_error:
                print(f"HTTP error: {http_error}")
            except requests.exceptions.RequestException as request_exception:
                print(f"Request error: {request_exception}")
            except ValueError as value_error:
                print(f"JSON decoding error: {value_error}")

    def get_results(self) -> list:
        return self.results


if __name__ == "__main__":
    # Load JSON input file
    file_path = "input.json"
    try:
        with open(file_path) as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Get input params from input JSON file
    input_keywords = json_data.get("keywords", [])
    input_proxies = json_data.get("proxies", [])
    input_search_type = json_data.get("type", "")

    # Search appropriate results in GitHub and add them to the dict results
    crawler = GitHubCrawler(input_keywords, input_proxies, input_search_type)
    crawler.search_github()
    results = crawler.get_results()

    # Convert dict results to JSON
    json_result = json.dumps(results)
    print(json_result)
