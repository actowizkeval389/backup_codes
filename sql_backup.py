import subprocess
import datetime
import os

# SQL credentials
host = "localhost"
user = "root"
password = "actowiz"

# replace base_path if needed
def find_mysql_binaries(base_path=r"C:\Program Files\MySQL"):
    mysql_exe = None
    mysqldump_exe = None

    if not os.path.exists(base_path):
        print("MySQL base path does not exist.")
        return None, None

    # Search subdirectories like 'MySQL Server 8.0', 'MySQL Server 5.7', etc.
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            full_dir = os.path.join(root, dir_name, "bin")
            mysql_path = os.path.join(full_dir, "mysql.exe")
            dump_path = os.path.join(full_dir, "mysqldump.exe")

            if os.path.isfile(mysql_path) and os.path.isfile(dump_path):
                mysql_exe = mysql_path
                mysqldump_exe = dump_path
                return mysql_exe, mysqldump_exe  # Found both, return immediately

        # Don't recurse deeply; just first level subdirs
        break

    return mysql_exe, mysqldump_exe

MYSQL_PATH, DUMP_PATH = find_mysql_binaries()
# Directory to store backups
backup_dir = "mysql_backups"
os.makedirs(backup_dir, exist_ok=True)

# Timestamp for file naming
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Fetch all database names except system ones
def get_database_list():
    try:
        result = subprocess.run(
            [MYSQL_PATH, f"-h{host}", f"-u{user}", f"-p{password}", "-e", "SHOW DATABASES;"],
            capture_output=True,
            text=True,
            check=True
        )
        dbs = result.stdout.splitlines()[1:]  # Skip header
        excluded = {"information_schema", "performance_schema", "mysql", "sys"}
        return [db for db in dbs if db not in excluded]
    except subprocess.CalledProcessError as e:
        print("❌ Error getting database list:", e.stderr)
        return []

# Backup each database
def backup_databases(databases):
    for db in databases:
        backup_file = os.path.join(backup_dir, f"{db}.sql")
        try:
            with open(backup_file, "w") as out_file:
                subprocess.run(
                    [DUMP_PATH, f"-h{host}", f"-u{user}", f"-p{password}", db],
                    stdout=out_file,
                    stderr=subprocess.PIPE,
                    check=True
                )
            print(f"✅ Backup successful for: {db}")
            print(f"\n✅ Backup of your file has been completed at path:: {os.getcwd()} ")
        except subprocess.CalledProcessError as e:
            print(f"❌ Backup failed for: {db}")
            print("Error:", e.stderr)

if __name__ == "__main__":
    dbs = get_database_list()
    if dbs:
        backup_databases(dbs)
    else:
        print("No databases found or failed to connect.")
