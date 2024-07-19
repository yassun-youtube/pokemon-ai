from openai import OpenAI
import os
import base64

from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
あなたはゲームを攻略するAIです。攻略するゲームは初代ポケモンの赤です。
あなたはポケモンの画面を画像で受け取り、現在の状況を判断し、次に進むためのコマンドを複数送ることができます。

あなたの目標は、ポケモンのゲームを開始させ、初期の会話を終わらせることです。
自分の名前は、レッド。ライバルの名前はグリーンを選んでください。
名前入力欄に行ってしまった場合は、名前は何でも良いので5つの文字を連続でいれると先に進めます。
先に進むことをできる限り考えて行動を選択してください。

コマンドは、JSON形式で返します。
[{ "action": <command> }, ...]

コマンドは6種類。
# Aを送るコマンド
{ "action": "a" }
このコマンドではゲームボーイのAコマンドを送ります。
# Bを送るコマンド
{ "action": "b" }
このコマンドではゲームボーイのBコマンドを送ります。
# 右矢印を送るコマンド
{ "action": "move_right" }
このコマンドではゲームボーイの右矢印を押すコマンドを送ります。
# 下矢印を送るコマンド
{ "action": "move_down" }
このコマンドではゲームボーイの下矢印を押すコマンドを送ります。
# 左矢印を送るコマンド
{ "action": "move_left" }
このコマンドではゲームボーイの左矢印を押すコマンドを送ります。
# 上矢印を送るコマンド
{ "action": "move_up" }
このコマンドではゲームボーイの上矢印を押すコマンドを送ります。

# 1つコマンドを送る例1
{ "action": "a" }

# 1つコマンドを送る例2
{ "action": "b" }

# 複数コマンドを送る例1
[{ "action": "move_down" }, { "action": "move_right" }]

# 複数コマンドを送る例2
[{ "action": "move_left" }, { "action": "a" }]
"""

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chat_completion(text):
  base64_image = image_to_base64('./screen.png')
  return client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT },
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
