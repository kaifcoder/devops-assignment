#!/usr/bin/env python3
import os
import json
import subprocess
import requests
import sys
import re

def get_diff_for_pr(base, head):
    result = subprocess.run(["git", "diff", base, head], capture_output=True, text=True)
    return result.stdout

def get_diff_for_push():
    result = subprocess.run(["git", "diff", "HEAD~1", "HEAD"], capture_output=True, text=True)
    return result.stdout

def post_pr_comment(owner, repo, pr_number, comment, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        print("Failed to post comment:", response.text)
    else:
        print("Posted comment successfully.")

def extract_json(response_text):
    # Look for a JSON object containing the key "breaking_changes"
    pattern = r'(\{.*"breaking_changes".*\})'
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            return data
        except Exception as e:
            print("Error parsing JSON:", e)
    return None

def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    diff = ""
    pr_number = None

    if event_name == "pull_request":
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if not event_path:
            print("GITHUB_EVENT_PATH not set.")
            sys.exit(1)
        with open(event_path, "r") as f:
            event_data = json.load(f)
        pr_number = event_data.get("pull_request", {}).get("number")
        base_sha = event_data.get("pull_request", {}).get("base", {}).get("sha")
        head_sha = event_data.get("pull_request", {}).get("head", {}).get("sha")
        if not base_sha or not head_sha:
            print("Missing commit SHAs in PR event.")
            sys.exit(1)
        diff = get_diff_for_pr(base_sha, head_sha)
    elif event_name == "push":
        diff = get_diff_for_push()
    else:
        print("Unsupported event type:", event_name)
        sys.exit(1)

    if not diff:
        print("No diff found.")
        sys.exit(0)  # Nothing to review

    # Construct a prompt that instructs the AI to review and then output a JSON object.
    prompt = (
        "Perform a thorough code review for the following diff. "
        "Point out any issues and improvements. "
        "After your review, on a new line output a JSON object with the following keys: "
        "'breaking_changes' (true if any breaking changes are detected, false otherwise) and "
        "'explanation' (a short explanation for your decision). "
        "Ensure that the JSON is the only content on that line.\n\n"
        "Diff:\n" + diff
    )

    openai_api_key = os.environ.get("GROQ_API_KEY")
    if not openai_api_key:
        print("GROQ_API_KEY not set.")
        sys.exit(1)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an expert code reviewer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 32768
    }
    response = requests.post("https://api.groq.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code != 200:
        print("GroqAI API error:", response.text)
        sys.exit(1)
    
    full_response = response.json()["choices"][0]["message"]["content"]
    print("Full AI Response:\n", full_response)
    
    json_data = extract_json(full_response)
    if not json_data:
        print("No JSON data could be extracted from AI response.")
        sys.exit(1)
    
    # Post the full review as a comment (for PR events).
    if event_name == "pull_request" and pr_number:
        repo_full = os.environ.get("GITHUB_REPOSITORY")
        if repo_full:
            owner, repo = repo_full.split("/")
            github_token = os.environ.get("GITHUB_TOKEN")
            if github_token:
                post_pr_comment(owner, repo, pr_number, full_response, github_token)
    
    if json_data.get("breaking_changes"):
        print("Breaking changes detected:", json_data.get("explanation", "No explanation provided."))
        sys.exit(1)  # Fail the job to block merging.
    else:
        print("No breaking changes detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
