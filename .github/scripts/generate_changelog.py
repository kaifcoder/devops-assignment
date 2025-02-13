#!/usr/bin/env python3
import os
import subprocess
import requests

def get_last_tag():
    """Returns the most recent git tag, if available."""
    result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def get_commit_messages(from_commit):
    """Returns commit messages between the specified commit and HEAD."""
    range_spec = f"{from_commit}..HEAD" if from_commit else "HEAD"
    result = subprocess.run(["git", "log", range_spec, "--pretty=format:%s"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def main():
    # Retrieve commit messages since the last tag.
    last_tag = get_last_tag()
    commit_messages = get_commit_messages(last_tag)
    if not commit_messages:
        print("No commit messages found.")
        return

    # Construct a prompt for the AI to generate a detailed changelog.
    prompt = (
        "Based on the following commit messages, generate a detailed changelog that summarizes the changes in this release:\n\n"
        f"{commit_messages}"
    )
    
    # Call the OpenAI API to generate the changelog.
    openai_api_key = os.environ.get("GROQ_API_KEY")
    if not openai_api_key:
        print("GROQ_API_KEY not set.")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an expert technical writer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 500
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code != 200:
        print("OpenAI API error:", response.text)
        return

    changelog = response.json()["choices"][0]["message"]["content"]

    # Write the changelog to a file.
    with open("CHANGELOG.md", "w") as f:
        f.write(changelog)
    print("Changelog generated and saved to CHANGELOG.md.")

if __name__ == "__main__":
    main()
