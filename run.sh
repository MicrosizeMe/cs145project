#!/bin/bash

pip install -r requirements.txt

mkdir data
mkdir models
mkdir data/final_feathers
mkdir data/merged_feathers
mkdir data/merged_feathers/validation
mkdir data/test
mkdir data/validation

bash ./download.sh
bash ./expand.sh

python convert_xmls_to_csv.py
python merge_csvs.py
python create_final_features.py
python create_encoded_feather.py
python process_training_csvs.py
python final_model_train_and_eval.py