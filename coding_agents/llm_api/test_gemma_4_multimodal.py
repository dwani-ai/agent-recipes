import base64
from openai import OpenAI
import os
# Initialize the client pointing to your vLLM server
client = OpenAI(
    base_url=os.environ["LITELLM_API_BASE"],  # Port 80 as per your docker-compose
    api_key="token-is-ignored-by-vllm"
)

def encode_media(path):
    """Helper to encode local files to base64 if not using URLs."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


text_response = client.chat.completions.create(
    model="gemma4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What is your name ?"}
        ]
    }]
)


"""
# 1. Processing Text + Image
image_response = client.chat.completions.create(
    model="gemma4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What is depicted in this image?"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encode_media('scene.jpg')}"}
            }
        ]
    }]
)

# 2. Processing Text + Audio (Transcription/Reasoning)
audio_response = client.chat.completions.create(
    model="gemma4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Listen to this clip and provide a summary."},
            {
                "type": "input_audio",
                "input_audio": {
                    "data": encode_media("voice_note.wav"),
                    "format": "wav"
                }
            }
        ]
    }]
)

# 3. Processing Text + Video
# Note: vLLM expects video via 'video_url' or as a series of frames 
# depending on your specific vLLM version's implementation of the OpenAI spec.
video_response = client.chat.completions.create(
    model="gemma4",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe the movement in this video."},
            {
                "type": "video_url",
                "video_url": {"url": "https://example.com/sample_video.mp4"}
            }
        ]
    }]
)

print(f"Image Analysis: {image_response.choices[0].message.content}")
print(f"Audio Summary: {audio_response.choices[0].message.content}")
print(f"Video Description: {video_response.choices[0].message.content}")

"""

print(f"Text Analysis: {text_response.choices[0].message.content}")