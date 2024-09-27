import os
import subprocess
from pathlib import Path
import sys

def clean_ignored_files(base_path):
    # Convert base_path to a Path object
    base_path = Path(base_path)

    if not base_path.exists() or not base_path.is_dir():
        print(f"Error: {base_path} is not a valid directory.")
        return

    # Find all .gitignore files recursively starting from the base path
    for gitignore_path in base_path.rglob('.gitignore'):
        gitignore_dir = gitignore_path.parent

        # Change the working directory to the directory of the .gitignore file
        print(f"Processing .gitignore in {gitignore_dir}")
        os.chdir(gitignore_dir)

        # Run 'git clean -nX' to do a dry-run and list ignored files that would be removed
        try:
            result = subprocess.run(['git', 'clean', '-fXd'], capture_output=True, text=True)
            print(result.stdout)  # Show files that would be removed

            # If you want to actually remove the files, change '-nX' to '-fX' below
            # subprocess.run(['git', 'clean', '-fX'])

        except subprocess.CalledProcessError as e:
            print(f"Error processing {gitignore_path}: {e}")

        # Change back to the base path after processing
        os.chdir(base_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_gitignore.py <base_path>")
    else:
        base_path = sys.argv[1]
        clean_ignored_files(base_path)
