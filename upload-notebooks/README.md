# Upload notebooks to TileDB Cloud

Insert this action into your GitHub Actions workflow to upload your notebooks to
your TileDB Cloud account. Generate a TileDB Cloud API token (minimal scope:
`array:admin`) and save it as a GitHub repository secret, eg
`TILEDB_CLOUD_TOKEN`

Example:

```yaml
    - uses: TileDB-Inc/github-actions/upload-notebooks@main
      with:
        notebooks_local: >-
          path/to/notebook-1.ipynb
          path/to/notebook-2.ipynb
          path/to/notebook-3.ipynb
        notebooks_remote: >-
          tiledb://namespace/s3://cloud-path/notebook-1
          tiledb://namespace/s3://cloud-path/notebook-2
          tiledb://namespace/s3://cloud-path/notebook-3
        TILEDB_CLOUD_TOKEN: ${{ secrets.TILEDB_CLOUD_TOKEN }}
        TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME: <name-of-aws-credential-saved-on-tiledb-cloud>
```

**Important:** If you don't provide the name of your registered cloud
credentials via `TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME`, then your TileDB Cloud
API token must have scope `*`. This is required in order to query your user
profile to obtain the name  of your default cloud credentials

Local usage example. This passes all the values via arguments, but note that
alternatively you can define the env vars `TILEDB_CLOUD_TOKEN` and
`TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME`

```sh
pip install tiledb-cloud
python upload-notebooks.py --help

python upload-notebooks.py \
  --notebooks-local \
    path/to/notebook-1.ipynb \
    path/to/notebook-2.ipynb \
    path/to/notebook-3.ipynb \
  --notebooks-remote \
    tiledb://namespace/s3://cloud-path/notebook-1 \
    tiledb://namespace/s3://cloud-path/notebook-2 \
    tiledb://namespace/s3://cloud-path/notebook-3 \
  --tiledb-cloud-token <token> \
  --tiledb-cloud-storage-credential-name <name-of-aws-credential-saved-on-tiledb-cloud>
```
