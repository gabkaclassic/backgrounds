import boto3

from os.path import join, isfile
from os import rename, listdir, remove
from botocore.client import Config


class Handler:

    DEFAULT_FILENAME = 'file'

    def __init__(self, conf):

        self.access_key_id = conf['key_id']
        self.access_secret_key = conf['secret_key']
        self.bucket_name = conf['bucket_name']
        self.path = conf['path']
        self.count = conf['count']
        self.extension = conf['default_format']
        self.temp_dir = conf['tmp_path']

        self.resource = boto3.resource(
            's3',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.access_secret_key,
            config=Config(signature_version='s3v4')
        )

    def process_directory(self):
        files = [file for file in listdir(self.path) if isfile(join(self.path, file))]
        for file in files:
            filename = self.rename_file(file)
            if len(filename) == 0:
                files.append(file)
                continue
            self.save_file(filename)
            self.remove_file(filename)
            print(filename)

    def save_file(self, file):
        filename = file.split('.')[0]
        with open(join(self.path, file), 'rb') as data:
            self.resource.Bucket(self.bucket_name).put_object(Key=filename, Body=data)

    def rename_file(self, file):
        new_filename = str(self.count) + self.extension
        try:
            rename(join(self.path, file), join(self.path, new_filename))
            self.count += 1
        except WindowsError:
            return ''

        return new_filename

    def remove_file(self, file):
        remove(join(self.path, file))

    def download_file(self, number):
        filename = join(self.temp_dir, Handler.DEFAULT_FILENAME + self.extension)
        self.resource.Bucket(self.bucket_name)\
            .download_file(str(number), filename)

        return filename

