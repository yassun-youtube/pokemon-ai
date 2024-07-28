import asyncio
import websockets
import json
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import numpy as np

# WebSocketのエンドポイントURL
uri = "wss://s07tuceu77.execute-api.ap-northeast-1.amazonaws.com/dev/"

# PyBoyの初期化
pyboy = PyBoy('./roms/pokemon_red.gb', log_level="DEBUG", scale=4)
pyboy.set_emulation_speed(3)
# pyboy.game_wrapper = pyboy._plugin_manager.game_wrapper_pokemon_gen1

with open("state_file.state", "rb") as f:
    pyboy.load_state(f)

async def send_heartbeat(websocket):
    while True:
        await asyncio.sleep(60)  # 60秒ごとにハートビートを送信
        message = json.dumps({"action": "heartbeat"})
        await websocket.send(message)
        print("Sent heartbeat")


async def handle_websocket(websocket):
    await websocket.send(json.dumps({"action": "connect", "message": "Hello, world!"}))
    print("Connected to the WebSocket server")

    # ハートビートメッセージを送信するタスクを作成
    # heartbeat_task = asyncio.create_task(send_heartbeat(websocket))

    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            data = json.loads(message)
            # print(f"Received message: {data}")
            # PyBoyのイベント処理
            if data['action'] == 'move_up':
                pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
                pyboy.tick(30)
                pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
            elif data['action'] == 'move_down':
                print('move_down!!')
                pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
                pyboy.tick(30)
                pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
            elif data['action'] == 'move_left':
                pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
                pyboy.tick(30)
                pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
            elif data['action'] == 'move_right':
                pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
                pyboy.tick(30)
                pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
            elif data['action'] == 'a':
                pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
                pyboy.tick()
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
            elif data['action'] == 'b':
                pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
                pyboy.tick()
                pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
            elif data['action'] == 'save_image':
                pyboy.screen._set_image()
                pyboy.screen.image.show()
                image = pyboy.screen.image
                print(type(image))
                image.save('screen.png')
            elif data['action'] == 'save_state':
                with open("state_file.state", "wb") as f:
                    pyboy.save_state(f)
            elif data['action'] == 'load_state':
                with open("state_file.state", "rb") as f:
                    pyboy.load_state(f)
    except websockets.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("finally!!!")
        handle_websocket(websocket)

    # 接続が切れた場合にはハートビートタスクをキャンセル
    # heartbeat_task.cancel()

async def main():
    actions = []
    async with websockets.connect(uri) as websocket:
        websocket_task = asyncio.create_task(handle_websocket(websocket))

        # PyBoyのメインループ
        while pyboy.tick():
            await asyncio.sleep(0)  # イベントループの他のタスクを実行

            if pyboy.frame_count % 60 == 0:
                image = pyboy.screen.image
                image.save('screen.png')
                game_area = pyboy.game_area()
                # リストをJSON形式で保存
                with open('area.json', 'w') as f:
                    json.dump(convert_array(game_area), f)
                collision_area = pyboy.game_wrapper.game_area_collision()[::2,::2]
                # リストをJSON形式で保存
                with open('collision.json', 'w') as f:
                    json.dump(collision_area.tolist(), f)

        await websocket_task  # WebSocketタスクの終了を待つ


def convert_array(input_array):
    # 入力をnumpy配列に変換
    array = np.array(input_array)
    # 9x10の出力配列を初期化
    output_array = np.zeros((9, 10), dtype=int)

    # 2x2ブロックの情報を9x10配列に変換
    for i in range(9):
        for j in range(10):
            top_left = f"{array[i * 2, j * 2]:03}"
            top_right = f"{array[i * 2, j * 2 + 1]:03}"
            bottom_left = f"{array[i * 2 + 1, j * 2]:03}"
            bottom_right = f"{array[i * 2 + 1, j * 2 + 1]:03}"
            combined_number = int(f"{top_left}{top_right}{bottom_left}{bottom_right}")
            output_array[i, j] = combined_number

    return output_array.tolist()

# メインループを実行
asyncio.get_event_loop().run_until_complete(main())
