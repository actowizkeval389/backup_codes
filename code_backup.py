import os
import shutil
import datetime
print("executing python file backup")

# Directory to search
search_path = r"enter_your_path"  # Update as needed

# Directory to store collected Python files (stored *outside* the search path is safer)
backup_dir = "python_file_backups"
os.makedirs(backup_dir, exist_ok=True)

# Timestamp for unique subfolder
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")
os.makedirs(backup_subdir)


# Recursively find and copy .py files while skipping the backup folder itself
def collect_python_files(root_path):
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip backup directory if it's inside the root_path
        dirnames[:] = [d for d in dirnames if os.path.abspath(os.path.join(dirpath, d)) != os.path.abspath(backup_dir)]

        for file in filenames:
            if file.endswith(".py"):
                source_file = os.path.join(dirpath, file)
                try:
                    # Get relative path and recreate folder structure
                    rel_path = os.path.relpath(source_file, root_path)
                    destination_file = os.path.join(backup_subdir, rel_path)
                    destination_folder = os.path.dirname(destination_file)
                    os.makedirs(destination_folder, exist_ok=True)

                    shutil.copy2(source_file, destination_file)
                    print(f"✅ Copied: {source_file} → {os.path.abspath(destination_file)}")
                    count += 1
                except Exception as e:
                    print(f"❌ Failed to copy {source_file}: {e}")
    if count == 0:
        print("⚠️ No Python files found.")
    else:
        print(f"\n✅ Total {count} Python files backed up.")


if __name__ == "__main__":
    collect_python_files(search_path)
