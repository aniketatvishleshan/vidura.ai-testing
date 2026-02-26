import subprocess
import json
import re
from pathlib import Path

BASE_BRANCH = "origin/main"
OUTPUT_FILE = "ChangeDelta.json"


# ---------------- GIT HELPERS ----------------
def run_git(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def get_merge_base():
    return run_git(["git", "merge-base", BASE_BRANCH, "HEAD"])


def get_changed_files(base):
    output = run_git(["git", "diff", "--name-status", f"{base}...HEAD"])
    files = []

    for line in output.splitlines():
        status, path = line.split("\t")
        files.append({"status": status, "path": path})

    return files


def get_diff(base, path):
    return run_git(["git", "diff", f"{base}...HEAD", "--", path])


# ---------------- FILE CLASSIFICATION ----------------
def classify_file(path):
    suffix = Path(path).suffix.lower()

    if suffix in [".py", ".js", ".ts", ".java", ".kt"]:
        return "code"
    if suffix in [".yaml", ".yml", ".json", ".env"]:
        return "config"
    if suffix in [".md"]:
        return "docs"
    if suffix in [".graphql", ".gql"]:
        return "schema"
    if "model" in path.lower():
        return "schema"

    return "other"


# ---------------- GENERIC CHANGE PARSER ----------------
def extract_line_changes(diff_text):
    additions = []
    deletions = []

    for line in diff_text.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            additions.append(line[1:].strip())
        elif line.startswith("-") and not line.startswith("---"):
            deletions.append(line[1:].strip())

    return additions, deletions


# ---------------- MAIN PIPELINE ----------------
def run_extraction():
    print("🔎 Finding merge base...")
    base = get_merge_base()

    print("📂 Detecting changed files...")
    changed_files = get_changed_files(base)

    delta = {
        "files": [],
        "codeChanges": [],
        "configChanges": [],
        "docsChanges": [],
        "schemaChanges": []
    }

    for file in changed_files:
        file_type = classify_file(file["path"])

        print(f"⚙️ Processing {file['path']} ({file_type})")

        diff_text = get_diff(base, file["path"])
        added, removed = extract_line_changes(diff_text)

        change_record = {
            "file": file["path"],
            "status": file["status"],
            "addedLines": added,
            "removedLines": removed
        }

        delta["files"].append(change_record)

        if file_type == "code":
            delta["codeChanges"].append(change_record)
        elif file_type == "config":
            delta["configChanges"].append(change_record)
        elif file_type == "docs":
            delta["docsChanges"].append(change_record)
        elif file_type == "schema":
            delta["schemaChanges"].append(change_record)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(delta, f, indent=2)

    print("\n✅ ChangeDelta.json generated\n")
    print(json.dumps(delta, indent=2))


if __name__ == "__main__":
    run_extraction()