import os
import git
from datetime import datetime
import pytz
import time
import random

# Define your local time zone
local_tz = pytz.timezone('Asia/Kolkata')

# Set up repository path (current working directory)
repo_path = os.getcwd()

# Define the range for random commits
min_commits = 20
max_commits = 25

def make_commits():
    try:
        # Pick a random number of commits within the specified range
        num_commits = random.randint(min_commits, max_commits)

        repo = git.Repo(repo_path)
        origin = repo.remote(name='origin')
        
        previous_file_name = None
        
        for i in range(num_commits):
            # Create a new file name based on the current timestamp
            file_name = f"commit_file_{i+1}_{datetime.now(local_tz).strftime('%Y%m%d_%H%M%S')}.txt"

            # Create the new file and write content
            with open(file_name, 'w') as f:
                f.write(f"Commit {i+1} at {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Add changes to the staging area
            repo.git.add(file_name)

            # If there was a previous file, delete it and stage the deletion
            if previous_file_name:
                os.remove(previous_file_name)
                repo.git.rm(previous_file_name)
            
            # Commit changes
            commit_message = f"Automated commit {i+1} at {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')}"
            repo.index.commit(commit_message)
            
            # Push changes
            origin.push()
            
            print(f"✅ Committed and pushed: {commit_message}")
            
            # Set the current file as the previous file for the next iteration
            previous_file_name = file_name
            
            # Wait for 2 seconds before the next commit
            time.sleep(2)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    make_commits()
