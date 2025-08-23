upload_key_prefix="uploadKeys"

def get_upload_key_redis(key:str):
    return f"{upload_key_prefix}/{key}"