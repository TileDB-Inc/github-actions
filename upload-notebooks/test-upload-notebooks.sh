#!/bin/bash
set -u

set -e

echo -e "\n===\nTest: Upload minimal example notebook\n==="
NOTEBOOK_EXAMPLE="notebook-example-$RANDOM.ipynb"
cp notebook-example.ipynb $NOTEBOOK_EXAMPLE
python3 upload-notebooks.py \
  --notebooks-local $NOTEBOOK_EXAMPLE \
  --notebooks-remote tiledb://TileDBCITesting/s3://tiledb-test/tiledb-cloud-upload-ci-testing/${NOTEBOOK_EXAMPLE%.ipynb} \
  --tiledb-cloud-storage-credential-name IsaiahCloudKey \
  --delete-remote-notebooks
rm $NOTEBOOK_EXAMPLE

# The below examples purposefully trigger errors
set +e

echo -e "\n===\nTest: Fail for missing remote URI \n==="
python3 upload-notebooks.py \
  --notebooks-local \
    notebook-1.ipynb \
    notebook-2.ipynb \
  --notebooks-remote \
    tiledb://namespace/s3://notebook-1

echo -e "\n===\nTest: Fail for missing notebook\n==="
python3 upload-notebooks.py \
  --notebooks-local missing.ipynb \
  --notebooks-remote tiledb://namespace/s3://missing

echo -e "\n===\nTest: Fail for wrong extension\n==="
touch wrong-extension.txt
python3 upload-notebooks.py \
  --notebooks-local wrong-extension.txt \
  --notebooks-remote tiledb://namespace/s3://wrong-extension
rm wrong-extension.txt

echo -e "\n===\nTest: end of tests\n==="
