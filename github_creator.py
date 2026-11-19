"""
Automated GitHub Repository Creator and Pusher.
Uses GitHub REST API to create the repository and push the initial commit.
"""

import sys
import subprocess
import requests

def create_and_push(token: str, repo_name: str = "JobApplyAutomation", private: bool = False):
    token = token.strip()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    print(f"\n[1/3] Verifying GitHub token and user identity...")
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code != 200:
        print(f"[Error] Invalid GitHub Token or authentication failed: {user_res.status_code}")
        print(user_res.text)
        return False

    username = user_res.json().get("login")
    print(f"   Authenticated as GitHub user: @{username}")

    print(f"\n[2/3] Creating repository '{repo_name}' on GitHub...")
    payload = {
        "name": repo_name,
        "description": "LinkedIn Remote Job & Contract Automation System - Custom built for Baidar Bakht (Penn State IT)",
        "private": private,
        "auto_init": False
    }
    repo_res = requests.post("https://api.github.com/user/repos", json=payload, headers=headers)
    
    if repo_res.status_code == 201:
        print(f"   Successfully created repository: https://github.com/{username}/{repo_name}")
    elif repo_res.status_code == 422:
        print(f"   Repository '{repo_name}' already exists under @{username}. Proceeding to push...")
    else:
        print(f"[Error] Failed to create repo: {repo_res.status_code} - {repo_res.text}")
        return False

    print(f"\n[3/3] Pushing code to GitHub...")
    # Push using authenticated remote URL
    auth_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    clean_url = f"https://github.com/{username}/{repo_name}.git"

    subprocess.run(["git", "remote", "set-url", "origin", auth_url], check=True)
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"])
    
    # Clean up token from git config
    subprocess.run(["git", "remote", "set-url", "origin", clean_url], check=True)

    if push_res.returncode == 0:
        print("\n" + "=" * 70)
        print(f"🎉 SUCCESS! Your code is now live on GitHub:")
        print(f"   👉 https://github.com/{username}/{repo_name}")
        print("=" * 70 + "\n")
        return True
    else:
        print("\n[Error] Git push failed. Please check your token permissions ('repo' scope required).")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = input("Enter your GitHub Personal Access Token (with 'repo' scope): ").strip()
    
    if not token:
        print("No token provided. Exiting.")
        sys.exit(1)

    create_and_push(token)
