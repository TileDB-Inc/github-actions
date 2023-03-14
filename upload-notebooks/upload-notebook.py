#!/usr/bin/env python

# Upload notebook to TileDB Cloud
#
# Usage:
#     python upload-notebook.py <path/to/notebook.ipynb>
#     python upload-notebook.py --help
#
# Variables read from the environment:
#   - TILEDB_CLOUD_TOKEN: API token for TileDB Cloud account (required)
#   - TILEDB_CLOUD_NAMESPACE: Namespace for TileDB Cloud (required)
#   - TILEDB_CLOUD_STORAGE_PATH: Storage path on TileDB Cloud (optional)
#   - TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME: Storage credentials to use on TileDB Cloud (optional)


import argparse
import os
import sys

import tiledb.cloud

# Process input
parser = argparse.ArgumentParser(
    description="Upload notebook to TileDB Cloud",
    epilog="TileDB Cloud options may also be set as environment variables, but values set via command line flags will take priority",
)
parser.add_argument(
    "notebook",
    help="Notebook file to upload (extension .ipynb)",
)
parser.add_argument(
    "--tiledb-cloud-token",
    required=False,
    default=os.environ.get("TILEDB_CLOUD_TOKEN"),
    help="API token for TileDB Cloud account",
)
parser.add_argument(
    "--tiledb-cloud-namespace",
    required=False,
    default=os.environ.get("TILEDB_CLOUD_NAMESPACE"),
    help="Namespace for TileDB Cloud",
)
parser.add_argument(
    "--tiledb-cloud-storage-path",
    required=False,
    default=os.environ.get("TILEDB_CLOUD_STORAGE_PATH"),
    help="Storage path on TileDB Cloud",
)
parser.add_argument(
    "--tiledb-cloud-storage-credential-name",
    required=False,
    default=os.environ.get("TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME"),
    help="Storage credentials to use on TileDB Cloud",
)
args = parser.parse_args()

notebook = args.notebook
token = args.tiledb_cloud_token
namespace = args.tiledb_cloud_namespace
storage_path = args.tiledb_cloud_storage_path
storage_credential_name = args.tiledb_cloud_storage_credential_name

# Verify input
if not os.path.exists(notebook):
    sys.stderr.write("Error: Notebook file does not exist: %s\n" % (notebook))
    sys.exit(1)

notebook_name, ext = os.path.splitext(notebook)
notebook_name = os.path.basename(notebook_name)
if ext != ".ipynb":
    sys.stderr.write(
        "Error: Notebook file extension must be '.ipynb', not '%s'\n" % (ext)
    )
    sys.exit(1)

if token is None:
    sys.stderr.write("Error: Missing API token\n")
    sys.stderr.write(
        "You must define the token as the env var TILEDB_CLOUD_TOKEN or pass it to --tiledb-cloud-token\n"
    )
    sys.exit(1)

if namespace is None:
    sys.stderr.write("Error: Missing namespace\n")
    sys.stderr.write(
        "You must define the namespace as the env var TILEDB_CLOUD_NAMESPACE or pass it to --tiledb-cloud-namespace\n"
    )
    sys.exit(1)

# Login and upload
tiledb.cloud.login(token=token)
user = tiledb.cloud.user_profile()
sys.stderr.write("Info: Logged into TileDB Cloud as %s\n" % (user.username))
sys.stderr.write("Info: Notebook to upload is %s\n" % (notebook))
sys.stderr.write("Info: Namespace is %s\n" % (namespace))
if storage_path is not None:
    sys.stderr.write("Info: Storage path is %s\n" % (storage_path))
if storage_credential_name is not None:
    sys.stderr.write(
        "Info: Storage credential name is %s\n" % (storage_credential_name)
    )

try:
    tiledb.cloud.upload_notebook_from_file(
        ipynb_file_name=notebook,
        namespace=namespace,
        array_name=notebook_name,
        storage_path=storage_path,
        storage_credential_name=storage_credential_name,
        on_exists=tiledb.cloud.notebook.OnExists.OVERWRITE,
    )
except tiledb.cc.TileDBError:
    # If it's a new file, can't use OVERWRITE
    tiledb.cloud.upload_notebook_from_file(
        ipynb_file_name=notebook,
        namespace=namespace,
        array_name=notebook_name,
        storage_path=storage_path,
        storage_credential_name=storage_credential_name,
    )
