from openai import OpenAI
import os
import base64

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat_completion(text, prompt, logs):
  base64_image = image_to_base64('./screen.png')
  return client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": prompt },
      {"role": "user", "content": [
        {"type": "text", "text": text},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
          },
        },
      ]},
    ]
  )

def image_to_base64(image_path):
  # 画像をバイナリモードで読み込む
  with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

  # 画像データをBase64でエンコードする
  base64_encoded_data = base64.b64encode(image_data)

  # エンコードされたデータを文字列に変換
  base64_string = base64_encoded_data.decode('utf-8')

  return base64_string
