from http import HTTPStatus
import uuid
import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from env import endpoint, bucket_name, region

# 检查必要的环境变量
if not all([endpoint, bucket_name, region]):
    raise EnvironmentError("Missing required OSS configuration in env.py")

# OSS_ACCESS_KEY_ID and OSS_ACCESS_KEY_SECRET
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

try:
    bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)
except Exception as e:
    raise RuntimeError(f"Failed to initialize OSS bucket: {str(e)}")


def file_path_to_oss_url(file_path: str):
    if file_path.startswith("http"):
        return file_path
    ext = file_path.split('.')[-1]
    object_name = f'studio-temp/mcp-playground/{uuid.uuid4()}.{ext}'
    response = bucket.put_object_from_file(object_name, file_path)
    file_url = file_path
    if response.status == HTTPStatus.OK:
        file_url = bucket.sign_url('GET',
                                   object_name,
                                   60 * 60,
                                   slash_safe=True)
    return file_url
