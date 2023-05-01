#!/usr/bin/env python

# Upload notebook to TileDB Cloud
#
# Usage:
#     python upload-notebooks.py --help
#     python upload-notebooks.py \
#       --notebooks_local <path/to/notebook.ipynb> \
#       --notebooks_remote <tiledb://namespace/s3://cloud/notebook
#
# Variables read from the environment:
#   - TILEDB_CLOUD_TOKEN: API token for TileDB Cloud account (required via env var or cli arg)
#   - TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME: Storage credentials to use on TileDB Cloud (optional)


import argparse
import os
import sys
from urllib.parse import urlparse

import tiledb
import tiledb.cloud
from tiledb.cloud.notebook import OnExists

# Process input
parser = argparse.ArgumentParser(
    description="Upload notebook to TileDB Cloud",
)
parser.add_argument(
    "--notebooks-local",
    required=True,
    nargs="+",
    help="Notebook file(s) to upload (extension .ipynb)",
)
parser.add_argument(
    "--notebooks-remote",
    required=True,
    nargs="+",
    help="Full URI(s) on TileDB Cloud (no file extension), eg 'tiledb://namespace/s3://path/notebook'",
)
parser.add_argument(
    "--tiledb-cloud-token",
    required=False,
    default=os.environ.get("TILEDB_CLOUD_TOKEN"),
    help="API token for TileDB Cloud account (overrides env var TILEDB_CLOUD_TOKEN)",
)
parser.add_argument(
    "--tiledb-cloud-storage-credential-name",
    required=False,
    default=os.environ.get("TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME"),
    help="Storage credentials to use on TileDB Cloud (overrides env var TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME)",
)
parser.add_argument(
    "--delete-remote-notebooks",
    action="store_true",
    help="(Testing purposes only) Delete test notebook(s) from TileDB Cloud after successful upload",
)
args = parser.parse_args()

notebooks_local = args.notebooks_local
notebooks_remote = args.notebooks_remote
token = args.tiledb_cloud_token
storage_credential_name = args.tiledb_cloud_storage_credential_name
delete_remote_notebooks = args.delete_remote_notebooks

# Verify input
n_notebooks_local = len(notebooks_local)
n_notebooks_remote = len(notebooks_remote)
if n_notebooks_local != n_notebooks_remote:
    sys.stderr.write(
        "Error: number of local notebooks (%d) does not match number of TileDB URIs (%d)\n"
        % (n_notebooks_local, n_notebooks_remote)
    )
    sys.exit(1)

for notebook in notebooks_local:
    if not os.path.exists(notebook):
        sys.stderr.write("Error: Notebook file does not exist: %s\n" % (notebook))
        sys.exit(1)

    notebook_name, ext = os.path.splitext(notebook)
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

# Login
tiledb.cloud.login(token=token)
if storage_credential_name is not None:
    sys.stderr.write(
        "Info: Storage credential name is %s\n" % (storage_credential_name)
    )

# Upload
for i in range(len(notebooks_local)):
    notebook = notebooks_local[i]
    uri = notebooks_remote[i]
    sys.stderr.write("Info: Notebook to upload is %s\n" % (notebook))
    sys.stderr.write("Info: TileDB Cloud URI is %s\n" % (uri))

    scheme, namespace, s3path, _, _, _ = urlparse(uri)
    s3path = s3path.lstrip("/")
    if scheme != "tiledb":
        sys.stderr.write(
            "Error: TileDB Cloud URI must start 'tiledb://', not '%s://'\n" % (scheme)
        )
        sys.exit(1)

    with tiledb.scope_ctx(tiledb.cloud.Ctx()):
        exists = tiledb.array_exists(uri)
    if exists:
        sys.stderr.write("Info: Updating existing notebook file\n")
    else:
        sys.stderr.write("Info: Uploading new notebook file\n")

    uploaded = tiledb.cloud.upload_notebook_from_file(
        ipynb_file_name=notebook,
        namespace=namespace,
        array_name=os.path.basename(s3path),
        storage_path=os.path.dirname(s3path),
        storage_credential_name=storage_credential_name,
        on_exists=OnExists.OVERWRITE if exists else OnExists.FAIL,
    )
    sys.stderr.write("Info: Uploaded to %s\n" % (uploaded))

    if delete_remote_notebooks:
        tiledb.cloud.deregister_array(uri)
        sys.stderr.write("Info: Deregistered remote notebook %s\n" % (uri))
