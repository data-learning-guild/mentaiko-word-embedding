"""Upload model and user's vector files to Cloud Storage
"""
from pathlib import Path
import os
import sys

from google.cloud import storage


def create_bucket_class_location(
    bucket_name: str, project_id: str, storage_class: str='STANDARD', location: str='asia-northeast1'):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    if bucket.exists(storage_client):
        print('bucket has already existed.')
        return
    bucket.storage_class = storage_class
    new_bucket = storage_client.create_bucket(bucket, location=location)

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def main():
    """Main proc
    """
    bucket_name = os.environ['GAE_DEFAULT_BUCKET_NAME']
    project_id = os.environ['BQ_PROJECT_ID']
    create_bucket_class_location(bucket_name, project_id)
    
    p = Path('./data')
    
    # upload trained model
    p_list = list(p.glob('*.model.pkl'))
    p_model = p_list[0] if len(p_list) > 0 else None
    if p_model is None:
        print('model path is invalid.')
        sys.exit(1)
    upload_blob(bucket_name, str(p_model), p_model.name)

    # upload users table
    p_list = list(p.glob('users.csv'))
    p_users_tbl = p_list[0] if len(p_list) > 0 else None
    if p_users_tbl is None:
        print('users tbl path is invalid.')
        sys.exit(1)
    upload_blob(bucket_name, str(p_users_tbl), p_users_tbl.name) 

    # upload user's vectors
    p_list = list(p.glob('*.json'))
    p_list = [x for x in p_list if x.stem not in ['dataset', 'test_dataset', 'train_dataset']]
    p_vectors = p_list

    for p_vector in p_vectors:
        upload_blob(bucket_name, str(p_vector), 'vectors/' + p_vector.name)


if __name__ == "__main__":
    main()
