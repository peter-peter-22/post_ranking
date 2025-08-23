import json
from minio.commonconfig import ENABLED
from minio.lifecycleconfig import LifecycleConfig, Rule, Expiration
from minio.commonconfig import Filter
from src.minio.client import minio_client

public_bucket = "public"
variants_bucket = "variants"

def create_bucket_if_missing(bucket_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        print(f"Created bucket: {bucket_name}")
    else:
        print(f"Bucket already exists: {bucket_name}")

def set_public_read_policy(bucket_name: str):
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }]
    }
    minio_client.set_bucket_policy(bucket_name, json.dumps(policy))
    print(f"Set public read policy on: {bucket_name}")

def set_expiration_policy(bucket_name: str, days: int = 1):
    rule = Rule(
        rule_id="expire-after-one-day",
        status=ENABLED,
        expiration=Expiration(days=days),
        rule_filter=Filter(prefix="")
    )
    lifecycle = LifecycleConfig([rule])
    minio_client.set_bucket_lifecycle(bucket_name, lifecycle)
    print(f"Set {days}-day expiration on: {bucket_name}")

def initialize_buckets():
    # Public bucket
    create_bucket_if_missing(public_bucket)
    set_public_read_policy(public_bucket)

    # Variants bucket
    create_bucket_if_missing(variants_bucket)
    set_public_read_policy(variants_bucket)
    set_expiration_policy(variants_bucket, days=1)

    print("MinIO buckets initialized.")