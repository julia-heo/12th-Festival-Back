import boto3
import uuid

from festival.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file, folder, name):
        return self.client.upload(file, folder, name)


class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key
        )
        self.s3_client   = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file, folder, name):
        try: 
            file_id    = name
            path = folder+'/'+file_id
            file_extension = name.split('.')[-1]
            # print(file.content_type )
            # extra_args = { 'ContentType' : file.content_type }
            extra_args = { 'ContentType' : 'image/'+file_extension }

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    path,
                    ExtraArgs = extra_args
                )
            return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{path}'
        except Exception as e:
            print("Error:", e)
            return None


# MyS3Client instance
s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)