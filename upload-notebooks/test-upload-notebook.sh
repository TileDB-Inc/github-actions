#!/bin/bash
set -u

echo -e "\n===\nTest: Upload minimal example notebook\n==="
NOTEBOOK_EXAMPLE="notebook-example-$RANDOM.ipynb"
cp notebook-example.ipynb $NOTEBOOK_EXAMPLE
python upload-notebook.py \
  --tiledb-cloud-namespace=jdblischak \
  --tiledb-cloud-storage-path s3://tiledb-cloud-jdblischak/notebooks \
  --tiledb-cloud-storage-credential-name=personal-aws \
  $NOTEBOOK_EXAMPLE
rm $NOTEBOOK_EXAMPLE

echo -e "\n===\nTest: Fail for missing notebook\n==="
python upload-notebook.py missing.ipynb

echo -e "\n===\nTest: Fail for wrong extension\n==="
touch wrong-extension.txt
python upload-notebook.py wrong-extension.txt
rm wrong-extension.txt

echo -e "\n===\nTest: end of tests\n==="
