from hdfs import InsecureClient
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print("Error: .env file not found at", env_path)
load_dotenv(dotenv_path=env_path)

HADOOP_HOST = os.getenv("HADOOP_HOST")
NAMENODE_WEB_PORT = os.getenv("NAMENODE_WEB_PORT")
HADOOP_USER = os.getenv("HADOOP_USER")

print("HADOOP_HOST:", HADOOP_HOST)
print("NAMENODE_WEB_PORT:", NAMENODE_WEB_PORT)
print("HADOOP_USER:", HADOOP_USER)

if None in (HADOOP_HOST, NAMENODE_WEB_PORT, HADOOP_USER):
    raise ValueError("Environment variables not loaded correctly. Check .env file.")

client = InsecureClient(f'http://{HADOOP_HOST}:{NAMENODE_WEB_PORT}', user=HADOOP_USER)

file_path = '/user/hadoop/text.txt'
folder_path = '/user/hadoop/'

data_to_write = "Hello HDFS! This is the initial data."
with client.write(file_path, encoding='utf-8', overwrite=True) as writer:
    writer.write(data_to_write)
print("File created in HDFS!")

with client.read(file_path, encoding='utf-8') as reader:
    content = reader.read()
print("\nRead from HDFS:")
print(content)

new_data = "This is updated data for HDFS."
with client.write(file_path, encoding='utf-8', overwrite=True) as writer:
    writer.write(new_data)
print("\nFile updated in HDFS!")

append_data = "\nAppending a new line to the file."
with client.write(file_path, encoding='utf-8', append=True) as writer:
    writer.write(append_data)
print("\nData appended to HDFS file!")

with client.read(file_path, encoding='utf-8') as reader:
    content = reader.read()
print("\nAfter update/append, file content:")
print(content)

files = client.list(folder_path)
print(f"\nFiles in folder {folder_path}: {files}")

client.delete(file_path)
print("\nFile deleted from HDFS!")

files_after_delete = client.list(folder_path)
print(f"Files after deletion: {files_after_delete}")
