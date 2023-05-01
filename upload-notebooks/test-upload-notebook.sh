#!/bin/bash
set -u

echo -e "\n===\nTest: Upload minimal example notebook\n==="
NOTEBOOK_EXAMPLE="notebook-example-$RANDOM.ipynb"
cp notebook-example.ipynb $NOTEBOOK_EXAMPLE
python upload-notebooks.py \
  --notebooks-local $NOTEBOOK_EXAMPLE \
  --notebooks-remote tiledb://jdblischak/s3://tiledb-cloud-jdblischak/notebooks/${NOTEBOOK_EXAMPLE%.ipynb} \
  --tiledb-cloud-storage-credential-name personal-aws \
  --delete-remote-notebooks
rm $NOTEBOOK_EXAMPLE

echo -e "\n===\nTest: Fail for missing remote URI \n==="
python upload-notebooks.py \
  --notebooks-local \
    notebook-1.ipynb \
    notebook-2.ipynb \
  --notebooks-remote \
    tiledb://namespace/s3://notebook-1

echo -e "\n===\nTest: Fail for missing notebook\n==="
python upload-notebooks.py \
  --notebooks-local missing.ipynb \
  --notebooks-remote tiledb://namespace/s3://missing

echo -e "\n===\nTest: Fail for wrong extension\n==="
touch wrong-extension.txt
python upload-notebooks.py \
  --notebooks-local wrong-extension.txt \
  --notebooks-remote tiledb://namespace/s3://wrong-extension
rm wrong-extension.txt

echo -e "\n===\nTest: end of tests\n==="
