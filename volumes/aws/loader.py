import os
import boto3
from botocore.exceptions import ClientError

# Get the S3 bucket name from environment variable
INPUT_BUCKET = os.environ.get('INPUT_BUCKET')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET')

# The objects in the buckets.
DATA_FILES = os.environ.get('DATA_FILES')
ARCHIVE_PATH = os.environ.get('ARCHIVE_PATH')

# Initialize S3 client
s3_client = boto3.client('s3')


def download_directory(from_s3_prefix, to_local_dir):
    """
    Download a directory of files from S3 to a local directory.
    
    :param s3_prefix: The S3 prefix (folder) to download from
    :param local_dir: The local directory to download to
    """
    try:
        # Ensure the local directory exists
        os.makedirs(to_local_dir, exist_ok=True)

        # List objects in the S3 bucket with the given prefix
        response = s3_client.list_objects_v2(Bucket=INPUT_BUCKET,
                                             Prefix=from_s3_prefix)

        # Download each object
        for obj in response.get('Contents', []):
            # Get the relative path of the file
            relative_path = os.path.relpath(obj['Key'], from_s3_prefix)
            # Construct the full local path
            local_file_path = os.path.join(to_local_dir, relative_path)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download the file
            s3_client.download_file(INPUT_BUCKET, obj['Key'], local_file_path)
            print(f"Downloaded: {obj['Key']} to {local_file_path}")

        print("Download completed successfully.")
    except ClientError as e:
        print(f"An error occurred: {e}")


def upload_directory(from_dir, to_s3_prefix):
    """
    Upload a local directory of files to S3.
    
    :param local_dir: The local directory to upload from
    :param to_s3_prefix: The S3 prefix (folder) to upload to
    """
    try:
        # Walk through the local directory
        for root, dirs, files in os.walk(from_dir):
            for filename in files:
                # Construct the full local path
                local_path = os.path.join(root, filename)
                # Construct the S3 key
                relative_path = os.path.relpath(local_path, from_dir)
                s3_key = os.path.join(to_s3_prefix, relative_path)

                # Upload the file
                s3_client.upload_file(local_path, OUTPUT_BUCKET, s3_key)
                print(f"Uploaded: {local_path} to {s3_key}")

        print("Upload completed successfully.")
    except ClientError as e:
        print(f"An error occurred: {e}")


def inject_data(local_dir):
    '''Create some arbitrary data.'''
    import json
    with open(local_dir + '/extra.json', 'w') as f:
        json.dump({'hello': 'world'}, f)


def main():
    # Ensure the S3_BUCKET environment variable is set
    if not OUTPUT_BUCKET or not INPUT_BUCKET:
        print("Error: S3 BUCKET environment variables is not set.")
        return 1

    if not DATA_FILES:
        print("Error: DATA_FILES path not set.")
        return 1

    if not ARCHIVE_PATH:
        print("Error: ARCHIVE_PATH path not set.")
        return 1

    local_dir = './data'
    # Example: Download files from S3
    download_directory(from_s3_prefix=DATA_FILES, to_local_dir=local_dir)

    # Create some sample data.
    inject_data(local_dir)

    # Example: Upload files to S3
    upload_directory(from_dir=local_dir, to_s3_prefix=ARCHIVE_PATH)


# Example usage
# INPUT_BUCKET=labout OUTPUT_BUCKET=labinput DATA_FILES=data ARCHIVE_PATH=input_files python loader.py
if __name__ == "__main__":
    main()
