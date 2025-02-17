#!/usr/bin/env python3
import os
import subprocess
import requests

def get_last_commit():
    """Returns the last commit SHA on the main branch before the current merge."""
    result = subprocess.run(["git", "rev-list", "--parents", "-n", "1", "HEAD"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    commits = result.stdout.strip().split()
    return commits[1] if len(commits) > 1 else None  # Get the parent commit of HEAD

def get_commit_messages(from_commit):
    """Returns commit messages between the specified commit and HEAD."""
    range_spec = f"{from_commit}..HEAD" if from_commit else "HEAD"
    result = subprocess.run(["git", "log", range_spec, "--pretty=format:%s"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_diff():
    """Returns the diff between the last two tags."""
    result = subprocess.run(["git", "diff", "--stat", "HEAD^", "HEAD"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def main():
    # Retrieve commit messages since the last tag.
    last_commit = get_last_commit()
    commit_messages = get_commit_messages(last_commit)
    diff = get_diff()
    if not commit_messages:
        print("No commit messages found.")
        return
    if not diff:
        print("No diff found.")
        return

    # Construct a prompt for the AI to generate a detailed changelog.
    prompt = (
        "Based on the following commit messages & diff, generate a detailed changelog that summarizes the changes in this release:\n\n"
        f"{commit_messages}"
        "\n\n"
        "Diff:\n"
        f"{diff}"
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
    response = requests.post("https://api.groq.com/openapi/v1/chat/completions", headers=headers, json=data)
    if response.status_code != 200:
        print("Groq API error:", response.text)
        return

    changelog = response.json()["choices"][0]["message"]["content"]

    # Write the changelog to a file.
    with open("CHANGELOG.md", "a") as f:
        f.write(f"\n## {last_tag or 'Latest Changes'}\n")
        f.write(changelog + "\n")
    print("Changelog generated and saved to CHANGELOG.md.")

    # Commit the changelog.
    subprocess.run(["git", "add", "CHANGELOG.md"])
    subprocess.run(["git", "commit", "-m", "Update changelog [skip ci]"])
    print("Changelog committed.")

    # Push the changes.
    subprocess.run(["git", "push"])
    print("Changes pushed.")

   

if __name__ == "__main__":
    main()
