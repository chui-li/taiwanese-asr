import os
import torch
import torchaudio
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from tqdm import tqdm 

os.environ["CUDA_VISIBLE_DEVICES"] = "1,2,3,4,5"  # 或 2~9，選擇空閒 GPU



model_path = "/mnt/usr1/azure005/whisper-code/Belle-whisper-large-v3-turbo-zh-TimeStretch-PitchShift-chinese-concatenated_audios/checkpoint-12000"
audio_folder = "/mnt/usr1/TAT-MOE/TAT-MOE-test"
output_file = "./transcriptions_TAT-MOE-test_Belle-whisper-large-v3-turbo-zh.txt"

# Load processor
try:
    processor = AutoProcessor.from_pretrained(model_path)
    print("✅ Successfully loaded processor and tokenizer.")
except:
    print("⚠️ Tokenizer not found, downloading from original model...")
    processor = AutoProcessor.from_pretrained("openai/whisper-base")
    processor.save_pretrained(model_path)
    print("✅ Tokenizer restored.")

# Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path).to(device)
model.eval()

def transcribe(audio_path):
    """
    Transcribe audio file using forced zh decoding.
    Returns raw transcription (no segmentation).
    """
    try:
        speech_array, sr = torchaudio.load(audio_path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            speech_array = resampler(speech_array)
        speech_array = speech_array.squeeze().numpy()

        input_features = processor.feature_extractor(speech_array, sampling_rate=16000).input_features
        input_features = torch.tensor(input_features).to(device)

        forced_decoder_ids = processor.get_decoder_prompt_ids(language="zh", task="transcribe")

        with torch.no_grad():
            predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids, num_beams=10)

        transcription = processor.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription

    except Exception as e:
        print(f"❌ Failed to transcribe: {audio_path} | Error: {e}")
        return None

def transcribe_folder(root_folder, output_path):
    all_audio_files = []

    # Find all .wav files recursively
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".wav"):
                all_audio_files.append(os.path.join(root, file))

    if not all_audio_files:
        print("⚠️ No .wav files found in folder.")
        return

    print(f"🔄 Starting transcription for {len(all_audio_files)} audio files...\n")

    with open(output_path, "w", encoding="utf-8") as f:
        for audio_path in tqdm(all_audio_files, desc="Processing"):
            transcription = transcribe(audio_path)
            if transcription:
                # Use full path as key
                f.write(f"{audio_path} {transcription}\n")

    print(f"✅ Transcription complete. Results saved to {output_path}")

if __name__ == "__main__":
    transcribe_folder(audio_folder, output_file)
