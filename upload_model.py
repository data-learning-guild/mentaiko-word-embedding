"""Upload model and user's vector files to Cloud Storage
"""
from pathlib import Path
import sys

from google.cloud import storage


def create_bucket_class_location(
    bucket_name: str, storage_class: str='STANDARD', location: str='asia-northeast1'):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
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
    p = Path('./data')
    
    p_list = list(p.glob('*.model'))
    p_model = p_list[0] if len(p_list) > 0 else None
    if p_model is None:
        print('model path is invalid.')
        sys.exit(1)
    p_list = list(p.glob('*.json'))
    p_list = [x for x in p_list if x.stem not in ['dataset', 'test_dataset', 'train_dataset']]
    p_vectors = p_list

    bucket_name = 'dlg-doc2vec-modules'
    create_bucket_class_location(bucket_name)

    upload_blob(bucket_name, str(p_model), p_model.name)
    for p_vector in p_vectors:
        upload_blob(bucket_name, str(p_vector), 'vectors/' + p_vector.name)


if __name__ == "__main__":
    main()
