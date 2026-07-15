import os

def get_repo_info(repo_path):
    file_count = 0
    folder_count = 0

    for root, dirs, files in os.walk(repo_path):
        # Ignore Git internals
        dirs[:] = [d for d in dirs if d != ".git"]

        file_count += len(files)
        folder_count += len(dirs)

    return {
        "Repository Name": os.path.basename(repo_path),
        "Repository Path": repo_path,
        "Files": file_count,
        "Folders": folder_count
    }