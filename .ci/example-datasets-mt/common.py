import sys
import subprocess

S3_BASE_URL = "s3://datasets.kamu.dev/odf/v2/"

# Input
S3_CONTRIB_DATASETS_URL = f"{S3_BASE_URL}contrib/"
S3_EXAMPLE_DATASETS_URL = f"{S3_BASE_URL}example/"
S3_MULTI_TENANT_EXAMPLES_URLS = [
    "s3://datasets.kamu.dev/odf/v2/demo/2022-04-deltares/",
    "s3://datasets.kamu.dev/odf/v2/demo/2023-08-fisheries/"
]

# Output
S3_EXAMPLE_MT_DATASETS_URL = f"{S3_BASE_URL}example-mt/"


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def s3_listdir(url):
    return [
        line.strip().split(' ')[1]
        for line in subprocess.run(
            f"aws s3 ls {url}", 
            shell=True, 
            text=True,
            check=True,
            capture_output=True,
        ).stdout.splitlines()
    ]

def s3_cat(url):
    return subprocess.run(
        f"aws s3 cp {url} -", 
        shell=True, 
        text=True,
        check=True,
        capture_output=True,
    ).stdout.strip()