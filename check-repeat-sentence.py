#找出train.jsonl和test.jsonl有沒有重複的句子內容
import json

train_file = "train.jsonl"
test_file = "test.jsonl"

def load_texts(filepath):
    texts = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            texts.add(data["text"].strip())
    return texts

train_texts = load_texts(train_file)
test_texts = load_texts(test_file)

# 找交集
duplicates = train_texts.intersection(test_texts)

print(f"✅ Train 共有 {len(train_texts)} 筆 unique text")
print(f"✅ Test 共有 {len(test_texts)} 筆 unique text")
print(f"⚠️ Train 和 Test 重複的 text 有 {len(duplicates)} 筆")

if duplicates:
    print("\n部分重複內容預覽：")
    for t in list(duplicates)[:20]:  # 只顯示前 20 筆
        print(t)
