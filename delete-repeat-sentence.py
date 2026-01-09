#刪除train.jsonl和test.jsonl重複內容
import json

train_file = "train.jsonl"
test_file = "test.jsonl"
output_test_file = "test_dedup.jsonl"

def load_texts(filepath):
    texts = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            texts.add(data["text"].strip())
    return texts

# 讀取 train 和 test 的 text 集合
train_texts = load_texts(train_file)
test_texts = load_texts(test_file)

# 找出重複的 text
duplicates = train_texts.intersection(test_texts)
print(f"⚠️ Train 和 Test 重複的 text 有 {len(duplicates)} 筆")

# 過濾 Test
with open(test_file, "r", encoding="utf-8") as f_in, \
     open(output_test_file, "w", encoding="utf-8") as f_out:
    kept = 0
    removed = 0
    for line in f_in:
        data = json.loads(line)
        if data["text"].strip() in duplicates:
            removed += 1
            continue
        f_out.write(json.dumps(data, ensure_ascii=False) + "\n")
        kept += 1

print(f"✅ 新的 Test 檔已生成：{output_test_file}")
print(f"保留 {kept} 筆，刪除 {removed} 筆重複資料")
