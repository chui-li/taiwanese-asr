import os
import json

jsonl_path = "train.jsonl"
missing_files = []

with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析錯誤: {e}")
            continue

        # 直接取出 audio_filepath 欄位
        audio_path = data.get("audio_filepath")

        if audio_path:
            # 確保 audio_path 是絕對路徑（如果本來就是就不變）
            abs_path = os.path.abspath(audio_path)

            if not os.path.exists(abs_path):
                missing_files.append(abs_path)
        else:
            print("⚠️ 找不到 audio_filepath 欄位:", data)

# 輸出缺失檔案
if missing_files:
    print(f"\n🚨 總共有 {len(missing_files)} 個檔案缺失：")
    for p in missing_files:
        print(p)

    with open("missing_audio.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(missing_files))
    print("\n✅ 已將缺失檔案清單輸出到 missing_audio.txt")
else:
    print("🎉 所有檔案都存在！")
