#!/bin/bash

# 設定 Hugging Face 快取路徑到專案資料夾
export HF_HOME=/mnt/usr1/azure005/.cache/huggingface
# 或更細分：
# export TRANSFORMERS_CACHE=/mnt/usr/azure005/.cache/huggingface/transformers
# export HF_DATASETS_CACHE=/mnt/usr/azure005/.cache/huggingface/datasets

# NCCL / CUDA 設定
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1
export CUDA_VISIBLE_DEVICES=5,6,7,8,9

# 生成帶日期時間的 log 檔案名稱
LOG_FILE="train_$(date +%Y%m%d_%H%M%S).log"

# 執行訓練並記錄 log
nohup python ./whisper-code/train_TimeStretch_PitchShift.py > "$LOG_FILE" 2>&1 &

echo "🚀 訓練已啟動！Log 檔案：$LOG_FILE"
echo "👉 用 tail -f $LOG_FILE 可以即時查看進度"

