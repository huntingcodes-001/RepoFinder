import requests
import os
import git

# Set your GitHub token here
GITHUB_TOKEN = 'you_github_token'
GITHUB_API_URL = 'https://api.github.com'
PROJECTS_DIR = 'reps'  # Directory where repos will be cloned

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def search_repos(query, max_results=10):
    url = f"{GITHUB_API_URL}/search/repositories?q={query}&sort=stars&order=desc"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()['items'][:max_results]
        return repos
    else:
        print("Failed to retrieve data")
        return None

def clone_repo(repo_url, repo_name):
    # Ensure the projects directory exists
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)

    repo_path = os.path.join(PROJECTS_DIR, repo_name)

    if os.path.exists(repo_path):
        print(f"Repository {repo_name} already exists. Skipping download.")
    else:
        print(f"Cloning {repo_name} into {PROJECTS_DIR}...")
        git.Repo.clone_from(repo_url, repo_path)
        print(f"Repository {repo_name} cloned successfully.")

def main():
    # Ask the user for input
    query = input("Enter a search query (e.g., 'machine learning', 'web development'): ")
    max_results = int(input("Enter the number of repositories to retrieve: "))

    # Search for repositories based on user input
    repos = search_repos(query, max_results=max_results)

    if repos:
        for repo in repos:
            print(f"Repository: {repo['name']}")
            print(f"Owner: {repo['owner']['login']}")
            print(f"Stars: {repo['stargazers_count']}")
            print(f"Description: {repo['description']}")
            print(f"URL: {repo['html_url']}")
            print("-" * 80)

            # Clone the repository
            clone_repo(repo['clone_url'], repo['name'])

if __name__ == "__main__":
    main()
