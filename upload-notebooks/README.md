# Upload notebooks to TileDB Cloud

Insert this action into your GitHub Actions workflow to upload your notebooks to
your TileDB Cloud account. Generate a TileDB Cloud API token and save it as a
GitHub repository secret, eg `TILEDB_CLOUD_TOKEN`

Minimal example:

```yaml
    - uses: TileDB-Inc/github-actions/upload-notebooks@main
      with:
        notebooks: "notebook-1.ipynb notebook-2.ipynb notebook-3.ipynb"
        TILEDB_CLOUD_TOKEN: ${{ secrets.TILEDB_CLOUD_TOKEN }}
        TILEDB_CLOUD_NAMESPACE: <namespace>
```

Full example

```yaml
    - name: Upload notebooks
      uses: TileDB-Inc/github-actions/upload-notebooks@main
      with:
        notebooks: "notebook-1.ipynb notebook-2.ipynb notebook-3.ipynb"
        TILEDB_CLOUD_TOKEN: ${{ secrets.TILEDB_CLOUD_TOKEN }}
        TILEDB_CLOUD_NAMESPACE: <namespace>
        TILEDB_CLOUD_STORAGE_PATH: s3://<your-s3-bucket>
        TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME: <name-of-aws-credential-saved-on-tiledb-cloud>
```

Local usage (uses command line flags instead of env vars). Note that it only
uploads a single notebook at a time

```sh
pip install tiledb-cloud
python upload-notebook.py --help
python upload-notebook.py --tiledb-cloud-token=<token> --tiledb-cloud-namespace=<namespace> <path/to/notebook.ipynb>
```
