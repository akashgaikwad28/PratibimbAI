import os

# Define the backend structure
structure = {
    "backend": {
        "app": {
            "root_files": ["main.py"],
            "graph": ["state.py", "nodes.py", "graph.py"],
            "services": ["web_scraper.py", "youtube_loader.py", "llm_client.py"],
            "schemas": ["content.py"],
            "utils": ["text.py"]
        },
        "root_files": ["requirements.txt", "README.md"]
    }
}

def create_structure(base_path, structure_dict):
    backend_path = os.path.join(base_path, "backend")
    os.makedirs(backend_path, exist_ok=True)

    # Create root files in backend
    for file in structure_dict["backend"]["root_files"]:
        open(os.path.join(backend_path, file), "w").close()

    app_path = os.path.join(backend_path, "app")
    os.makedirs(app_path, exist_ok=True)

    # Create root files in app
    for file in structure_dict["backend"]["app"]["root_files"]:
        open(os.path.join(app_path, file), "w").close()

    # Create subfolders and files
    for folder, files in structure_dict["backend"]["app"].items():
        if folder != "root_files":
            folder_path = os.path.join(app_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file in files:
                open(os.path.join(folder_path, file), "w").close()

if __name__ == "__main__":
    base_dir = os.getcwd()  # Current directory
    create_structure(base_dir, structure)
    print("Backend structure created successfully!")
