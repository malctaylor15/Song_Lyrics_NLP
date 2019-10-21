#!/usr/bin/env bash
source songlyric_env/bin/activate
export BERT_BASE_DIR=/home/owner/Documents/Github_projects/Bert_files/wwm_uncased_L-24_H-1024_A-16
export base_path=/home/owner/Documents/Github_projects/Song_Lyrics_NLP
python $base_path/bert/extract_features.py \
  --input_file=$base_path/data_checkpoints/all_lyrics/HIGHEST_IN_THE_ROOM_Travis_Scott.csv \
  --output_file=$base_path/data_checkpoints/embeds/HIGHEST_IN_THE_ROOM_Travis_Scott.jsonl \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --layers=-1,-2,-3,-4 \
  --max_seq_length=128 \
  --batch_size=8