import requests
import shutil
import os
from datetime import datetime
import numpy as np


def calculate_age():
    today = datetime.now()
    birthdate = '2000-05-16'  # Replace with your actual birthdate in 'YYYY-MM-DD' format
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    age_in_years = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    
    # Adjust month calculation based on whether birthday has passed this year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age_in_months = today.month - birthdate.month + 12 - 1
    else:
        age_in_months = today.month - birthdate.month
    
    # Calculate days since last month-day occurrence
    if today.day >= birthdate.day:
        age_in_days = today.day - birthdate.day
    else:
        # To find the last month's number of days, we adjust month and year accordingly
        last_month = today.month - 1 if today.month > 1 else 12
        last_year = today.year if last_month != 12 else today.year - 1
        days_in_last_month = (datetime(last_year, last_month + 1, 1) - datetime(last_year, last_month, 1)).days
        age_in_days = days_in_last_month - (birthdate.day - today.day)

    return age_in_years, age_in_months, age_in_days

def get_commits(username, repo, specific_author):
    """Fetch commit information and tally line statistics from a GitHub repository for a specific author."""
    # Retrieve the token from environment variables
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    url = f"https://api.github.com/repos/{username}/{repo}/commits"
    headers = {'Authorization': f'token {token}'}
    commit_count = 0 
    total_added = 0
    total_removed = 0

    while url:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                commits = response.json()
                for commit in commits:
                    # Check if the author's username matches the specific author
                    author_username = commit['author']['login'] if commit['author'] else None
                    if author_username == specific_author:
                        commit_url = commit['url']
                        commit_data = requests.get(commit_url, headers=headers).json()
                        if 'stats' in commit_data:
                            commit_count += 1
                            total_added += commit_data['stats']['additions']
                            total_removed += commit_data['stats']['deletions']

                # Pagination: Check 'Link' header for next page URL
                links = response.links
                url = links['next']['url'] if 'next' in links else None
            else:
                print("Failed to retrieve commits.")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                break
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            break

    return total_added, total_removed, commit_count

def get_repo_names(username):
    """Fetch a list of repository names from a GitHub user account."""
    # Retrieve the token from environment variables
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    # GitHub API endpoint for user repositories
    url = f"https://api.github.com/users/{username}/repos"
    headers = {'Authorization': f'token {token}'}
    repo_names = []

    # Paginate through all pages of results
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                repo_names.append(repo['name'])

            # Look for the 'next' link in pagination, if it's not present, stop looping
            links = response.links
            url = links['next']['url'] if 'next' in links else None
        else:
            print(f"Failed to retrieve repositories. Status Code: {response.status_code}")
            return []

    return repo_names

def find_positions():
    
    positions = []

    with open('/Users/jakeziegler/Desktop/x/projects/zigg17/asciicopy.txt', 'r') as file:
        content = file.read()

    keyword = ':'

    pos = content.find(keyword)
    while pos != -1:
        positions.append(pos)
        pos = content.find(keyword, pos + 1)
    return np.array(positions) + 2

def copy_file():
    """
    Copies a file from the source path to the destination path.

    Args:
        source_path (str): The path to the source file.
        destination_path (str): The path where the copy of the file will be saved.

    Returns:
        bool: True if the file was copied successfully, False otherwise.
    """

    source_path = '/Users/jakeziegler/Desktop/x/projects/zigg17/ascii.txt'
    destination_path = '/Users/jakeziegler/Desktop/x/projects/zigg17/asciicopy.txt'

    try:
        # Ensure the source file exists
        if not os.path.isfile(source_path):
            print("Error: Source file does not exist.")
            return False
        
        # Copy the file
        shutil.copyfile(source_path, destination_path)
        print(f"File copied successfully.")
        return
    except Exception as e:
        print(f"Failed to copy file: {e}")
        return


def insert_strings(positions, edits):
    """
    Insert strings into specific positions of a file's content.
    
    Args:
    filename (str): The file to edit.
    positions (list of int): The positions at which to insert the strings.
    edits (list of str): The strings to insert at the corresponding positions.
    
    Returns:
    None: Edits the file in-place.
    """
    filename = '/Users/jakeziegler/Desktop/x/projects/zigg17/asciicopy.txt'
    # Read the content of the file
    with open(filename, 'r') as file:
        content = file.read()
    
    # Check if the lengths of positions and edits are the same
    if len(positions) != len(edits):
        raise ValueError("The lengths of positions and edits must match.")
    
    # Sort the positions and edits by positions in descending order
    combined = sorted(zip(positions, edits), reverse=True)
    
    # Insert the edits at the specified positions
    for pos, edit in combined:
        content = content[:pos] + edit + content[pos:]
    
    # Write the modified content back to the file
    with open(filename, 'w') as file:
        file.write(content)


# Replace these with your actual username, repo, and personal access token
if __name__ == '__main__':
    
    username = 'zigg17'
    
    repos = get_repo_names(username)

    total_added = 0
    added = 0

    total_removed = 0
    removed = 0

    total_commits = 0
    commits = 0

    for repo in repos:  
        added, removed, commits = get_commits(username, repo, username)
        print(f"Repo: {repo}, Added: {added}, Removed: {removed}, Commits: {commits}")
        total_added += added
        total_removed += removed
        total_commits += commits
    
    age_in_years, age_in_months, age_in_days = calculate_age()

    existence = str(age_in_years) + ' years, ' + str(age_in_months) + ' months, ' + str(age_in_days) + ' days.'

    copy_file()

    positions = find_positions()

    positions = np.delete(positions, -1)
    positions = np.delete(positions, -1)
    positions = np.delete(positions, -1)
    positions = np.delete(positions, -1)

    insert_strings(positions, [existence, str(len(repos)), str(total_commits), str(total_added - total_removed)])