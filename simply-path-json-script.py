import json
import subprocess
import argparse
import time
import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY_ID'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_ACCESS_KEY_ID'

def analyze_json_file(json_file_path):
  """Analyzes a JSON file for Discord tokens and channel IDs.

  Args:
    json_file_path: The path to the JSON file to analyze.

  Returns:
    A list of tuples, where each tuple contains a Discord token and a channel ID.
  """

  with open(json_file_path, "r") as f:
    json_data = json.load(f)

  tokens_and_channel_ids = []
  for bot_name, bot_data in json_data.items():
    token = bot_data["token"]
    channel_id = bot_data["channel_id"]
    tokens_and_channel_ids.append((token, channel_id))

  return tokens_and_channel_ids


def export_discord_chats(tokens_and_channel_ids):
  """Exports Discord chats for the given tokens and channel IDs.

  Args:
    tokens_and_channel_ids: A list of tuples, where each tuple contains a Discord token and a channel ID.
  """
  for token, channel_id in tokens_and_channel_ids:
    process = subprocess.Popen(['docker', 'run', '--rm', '-d', '-v', '/home/ubuntu:/out',
                                'YOUR_DOCKER_EXPORTER_IMAGE', 'export', '-t', token, '-c', channel_id], stdout=subprocess.PIPE)

    # Show the output of the Docker container.
    #for line in process.stdout:
     # print(line.decode())

    # Wait for the process to finish.
    process.wait()

def push_chat_to_s3(chat_file_path, s3_bucket_name):
    s3_client = boto3.client("s3")
    chat_file_name = os.path.basename(chat_file_path)  # Extract the file name from the path
    with open(chat_file_path, "rb") as f:
        s3_client.upload_fileobj(f, s3_bucket_name, chat_file_name)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--json-file-path', required=True, help='The path to the JSON file to analyze.')
  args = parser.parse_args()

  json_file_path = args.json_file_path
  s3_bucket_name = "YOUR_BUCKET_NAME_FOR_CHATS_TO_EXPORT"

  # Export the chat for the given token and channel ID.
  tokens_and_channel_ids = analyze_json_file(json_file_path)
  export_discord_chats(tokens_and_channel_ids)


      # After export, push any .html files in /home/ubuntu/ to S3
  for file in os.listdir("/home/ubuntu/"):
      if file.endswith(".html"):
          file_path = os.path.join("/home/ubuntu/", file)
          push_chat_to_s3(file_path, s3_bucket_name)
          print("DONE")


def update_timestamp_in_json(json_data: dict):
  """Updates each object named as `TIMESTAMP` in a JSON data with the timestamp and updated time.

  Args:
    json_data: A JSON data in dictionary format.
  """

  # Get the current date and time.
  now = datetime.now()

  # Iterate over the JSON data and update each object named `TIMESTAMP` with the current date and time.
  for key, value in json_data.items():
    if isinstance(value, dict):
      update_timestamp_in_json(value)
    elif key == "TIMESTAMP":
      json_data[key] = now.isoformat()

  return json_data

# Load the config.json file into memory.
with open("/home/ubuntu/config-database/config.json", "r") as f:
  json_data = json.load(f)

# Update the timestamps in the JSON data.
json_data = update_timestamp_in_json(json_data)

# Save the updated JSON data to the file.
with open("/home/ubuntu/config-database/config.json", "w") as f:
  json.dump(json_data, f, indent=4)

file_path = ("/home/ubuntu/config-database/config.json")
push_chat_to_s3(file_path, "config-file-data")
