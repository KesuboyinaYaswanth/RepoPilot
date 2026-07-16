import os

from modules.constants import (
    IGNORED_DIRECTORIES,
    SUPPORTED_EXTENSIONS,
    LANGUAGE_MAPPING,
    BINARY_EXTENSIONS,
    MAX_FILE_SIZE
)


def load_repository(repo_path):

    loaded_files = []

    folders_scanned = 0
    files_indexed = 0
    skipped_files = 0
    languages = {}

    for root, dirs, files in os.walk(repo_path):
        folders_scanned += 1
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRECTORIES]

        for file in files:

            extension = os.path.splitext(file)[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                skipped_files += 1
                continue


            if extension in BINARY_EXTENSIONS:
                skipped_files += 1
                continue

            file_path = os.path.join(root, file)

            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                skipped_files += 1
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                skipped_files += 1
                continue

            metadata = {
                "path": file_path,
                "relative_path": os.path.relpath(file_path, repo_path),
                "filename": file,
                "extension": extension,
                "language": LANGUAGE_MAPPING.get(extension, "Unknown"),
                "size": os.path.getsize(file_path),
                "lines": len(content.splitlines()),
                "content": content
            }

            loaded_files.append(metadata)
            files_indexed += 1
            language = metadata["language"]
            if language not in languages:
                languages[language] = 0

            languages[language] += 1
    stats = {
        "files_indexed": files_indexed,
        "folders_scanned": folders_scanned,
        "skipped_files": skipped_files,
        "languages": languages
    }
    return loaded_files, stats