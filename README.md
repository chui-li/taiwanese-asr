# Taiwanese-ASR
## Content structure
```
├── whisper-base/
│   ├── check_missing_audio.py                  
│   ├── check-repeat-sentence.py  
│   ├── delete-repaet-sentence.py    
│   ├── inference.py
│   ├── json-produce.py  
│   ├── MER.py
│   ├── preprocessor_config.json    
│   ├── ref-json-produce.py 
│   ├── train.py  
│   ├── train.sh    
│   └── transcriptions_normalize.py
├── whisper-large-v3-turbo/
│   ├── check_missing_audio.py                  
│   ├── check-repeat-sentence.py  
│   ├── delete-repaet-sentence.py    
│   ├── inference.py
│   ├── json-produce.py  
│   ├── MER.py
│   ├── preprocessor_config.json    
│   ├── ref-json-produce.py 
│   ├── train_TimeStretch_PitchShift.py  
│   ├── train.sh    
│   └── transcriptions_normalize.py
└── TAT-MOE/                                    
    ├── TAT-MOE-eval                              
    ├── TAT-MOE-eval-key
    ├── TAT-MOE-test                       
    ├── TAT-MOE-test-key                    
    └── TAT-MOE-train                      
```

## 1. Download the example code
Please download the whole folder or `git@140.113.30.155:azure005/taiwanese-asr.git`.

## 2. Dataset download

Ministry of Education Complete Corpus (TAT_MOE)：

Corpus Application：https://tggl.naer.edu.tw/corpora_applications/new

Please select the type of corpus you wish to apply for, complete the form below, and submit. Please receive the email you provided and follow the instructions to complete your application. Once approved by the Institute, they will send you a download link to the email address you provided. Please download within 7 days; otherwise, your application will be lost.

How to cite this corpus: Liao, Y.-F. (2022). TAT_MOE Corpus [2022]. Ministry of Education. (Available online at https://tggl.naer.edu.tw . Retrieved on [user-specified date])

If you download successfully, you will receive the following zip files:
```
. TAT-MOE
├── TAT-MOE-eval                              
├── TAT-MOE-eval-key
├── TAT-MOE-test                       
├── TAT-MOE-test-key                    
└── TAT-MOE-train  	

```
Then you can extract the entire file.

- **JSON format** :

    ```JSON
    {
    "id": "43969",
    "出生地": "台灣台中",
    "句編號": "1.1",
    "台羅": "suà-lo̍h lâi-khuànn Sin-tik-tshī bîn-á-tsài gī-tsa̍p-la̍k hō ê thinn-khì",
    "台羅數字調": "sua3-loh8 lai5-khuann3 sin1-tik4-tshi7 bin5-a2-tsai3 gi7-tsap8-lak8 ho7 e5 thinn1-khi3",
    "字數": "17",
    "年齡": "54",
    "性別": "F",
    "提示卡切換速度": "中等",
    "提示卡編號": "A025",
    "教育程度": "碩士",
    "漢羅台文": "紲落來看新竹市明仔載二十六號的天氣",
    "現居地": "臺中市豐原區",
    "發音人": "IUF1001",
    "白話字": "sòa-lo̍h lâi-khòaⁿ Sin-tek-chhī bîn-á-chài gī-cha̍p-la̍k hō ê thiⁿ-khì",
    "總錄音時間(分)": "105",
    "腔調": "混合腔",
    "通過漢羅用字檢查": "True",
    "錄音環境": "錄音室",
    "音檔長度": "8.88"
    }
    ```


## 3. Environment Setup

- Hardware specifications recommendation: NVIDIA 4090 GPU

- Install miniconda:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

```

```bash
conda create -n myenv python=3.10 # "myenv": you can choose the name of environment you like.
conda activate myenv
cd whisper-base # enter the project folder
pip install -r requirements.txt

```

## 4. Data Preprocessing
#### 4.1 Prepare Train/Test/Eval.json

```bash
python json-produce.py
```
Where you should revise in the code:

- **"json_root"** corresponding to the `train.json`, `test.json` and `eval.json` in the TAT-MOE dataset.

- **"mic_dirs"** corresponding to which type of microphone you want, TAT-MOE dataset include six microphones.

- **"output_file"** corresponding to where you want to save the output.

- **"base_audio_path"** corresponding to train/test/eval audio in the TAT-MOE dataset.

- **"hanlo_text"** corresponding to which type of text you want to choose, ex. 漢羅台文 or 台羅 or 台羅數字調.

#### 4.2 Check missing audio

```bash
python check_missing_audio.py
```
- This step just to check if there is no audio existence corresponding to your `train.json`, `test.json` and `eval.json`.

- If the audio do not exist, please delete the one in `train.json`, `test.json` and `eval.json`.

#### 4.3 Data clear

For more objective results, you can follow these two steps:
```bash
python check-repeat-sentence.py
```
- This step is checking for duplicate sentences in the `train.json` and `test.json` files.

```bash
python delete-repeat-sentence.py
```
- This step is deleteing for duplicate sentences in the `train.json` and `test.json` files.

#### 4.4 Prepare reference_txt
```bash
python ref-json-produce.py
```
- This step is prepare the **"reference_txt"** in the `MER.py` which is the answer of test data.

If you have done all steps mentioned above, then you have finished data preprocessing.

## 5. Train the model
You can change the different size of whisper in **"model_name = openai/whisper-base"** in the `train.py`, like whisper-large.
```bash
./train.sh
```
- You can change the number of gpu in **"CUDA_VISIBLE_DEVICES"** in `train.sh`.

```bash
tail -f $LOG_FILE
```
- For example, `tail -f train_20250828_052836.log`, then you can see the training details.

- The log file will exist in your project folder, then you just revise the log file name.

If existing problem, you should go back to resolve, then
```bash
kill PID
``` 
- You can find your PID when you run `nvidia-smi` in environment.

## 6. Inference
When you have trained your model, the next step is inference.

If you find there is no `preprocessor_config.json` in your model, please move the `preprocessor_config.json` which we prepared in your model folder.

```bash
python inference.py
```
Where you should revise in the code:

- **"model_path"** corresponding to where the model you have trained and saved.

- **"audio_folder"** corresponding to where the test audio of the TAT-MOE dataset.

- **"output_file"** corresponding to where you want save the `transcriptions.txt`.

## 7. Transcriptions Normalization
This step is getting rid of the punctuation.
```bash
python transcriptions_normalize.py
```
When you have done this step, you will get the **"hypothesis_txt"** which is needed in `MER.py`

## 8. Calculate
```bash
python MER.py
```
Where you should revise in the code:

- **"reference_txt"** corresponding to the answer of test dataset when you produce this file in the step of **4.4 Prepare reference_txt**.

- **"hypothesis_txt"** corresponding to the result of your model inferencing on test dataset.

## 9. Result and Conclusion
- We train the whisper-base model and set the TrainingArguments below:
    ```
    training_args = TrainingArguments(
        output_dir="./whisper-base-model",
        per_device_train_batch_size=6,         
        gradient_accumulation_steps=2,         
        num_train_epochs=8,                     
        learning_rate=1e-5,                      
        warmup_steps=1000,                       
        logging_steps=10,
        save_steps=500,
        fp16=True,                             
        evaluation_strategy="no",              
        remove_unused_columns=False,
    )
    ```

- We train the whisper-large-v3-turbo model and set the TrainingArguments below:
    ```
    training_args = TrainingArguments(
        output_dir="./whisper-large-v3-turbo-model",
        per_device_train_batch_size=1,         
        gradient_accumulation_steps=10,         
        num_train_epochs=8,                     
        learning_rate=1e-5,                      
        warmup_steps=1000,                       
        logging_steps=10,
        save_steps=500,
        fp16=True,                             
        evaluation_strategy="no",              
        remove_unused_columns=False,
    )
    ```
- We train the whisper-base model on five NVIDIA 4090 GPUs.

- The results:
    
    1. Whisper-base model with audiomentations:
   
        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | 0.2090 | 0.0079 | 0.0230 | 0.1782 | 816630 |
        | sptest1  | 0.4722 | 0.0746 | 0.0899 | 0.3077 | 93647 |
        | sptest2  | 0.7146 | 0.1564 | 0.1631 | 0.3951 | 75325 |

    2. Whisper-large-v3-turbo model with audiomentations:

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test  | 0.1322 | 0.0051 | 0.0159 | 0.1113 | 816630 |
        | sptest1  | 0.3859 | 0.1096 | 0.0738 | 0.2026 | 93647 |
        | sptest2  | 0.5522 | 0.2070 | 0.0885 | 0.2567 | 75325 |

    3. Whisper-large-v3-turbo model with audiomentations on concatenated audios dataset:

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | **0.1234** | 0.0054 | 0.0080 | 0.1101 | 816630 |
        | sptest1  | **0.2764** | 0.0660 | 0.0233 | 0.1871 | 93647 |
        | sptest2  | **0.4189** | 0.1292 | 0.0226 | 0.2670 | 75325 |
    
    4. Whisper-large-v3-turbo model with audiomentations on concatenated audios dataset (add noise):

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | 0.1263 | 0.0053 | 0.0110 | 0.1100 | 816630 |
        | sptest1  | 0.2930 | 0.0600 | 0.0431 | 0.1898 | 93647 |
        | sptest2  | 0.4531 | 0.1179 | 0.0653 | 0.2681 | 75325 |

    5. Whisper-large-v3-turbo model with audiomentations on concatenated audios dataset (inference with logprob):

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | 0.1448 | 0.0063 | 0.0119 | 0.1266 | 816630 |
        | sptest1  | 0.2792 | 0.0594 | 0.0313 | 0.1884 | 93647 |
        | sptest2  | 0.4227 | 0.1279 | 0.0294 | 0.2654 | 75325 |

    6. Whisper-large-v3-turbo model with audiomentations on concatenated audios dataset (inference with logprob and repeat 10 times):

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | 0.1241 | 0.0054 | 0.0090 | 0.1097 | 816630 |
        | sptest1  | **0.2762** | 0.0603 | 0.0298 | 0.1861 | 93647 |
        | sptest2  | 0.4273 | 0.1238 | 0.0345 | 0.2690 | 75325 |

    7. Whisper-large-v3-turbo model with audiomentations on concatenated audios dataset (inference with logprob and repeat 10 times with temperature):

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | 0.1319 | 0.0057 | 0.0093 | 0.1169 | 816630 |
        | sptest1  | 0.2874 | 0.0697 | 0.0178 | 0.1998 | 93647 |
        | sptest2  | 0.4370 | 0.1315 | 0.0245 | 0.2809 | 75325 |

    8. Whisper-large-v3-turbo model with audiomentations on concatenated audios dataset(data-augmentation*5):

        | 資料集名稱 | Overall WER | Deletion Rate | Insertion Rate | Substitution Rate | Total Words |
        |------------|---------|-----------|-------|---------------|---------------|
        | TAT-MOE test | 0.1266 | 0.0048 | 0.0128 | 0.1090 | 816630 |
        | sptest1  | 0.2849 | 0.0814 | 0.0192 | 0.1843 | 93647 |
        | sptest2  | 0.4450 | 0.1425 | 0.0215 | 0.2810 | 75325 |

## 10. Reference

**Corpus Application**：https://tggl.naer.edu.tw/corpora_applications/new

