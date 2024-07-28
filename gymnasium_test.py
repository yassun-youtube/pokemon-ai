import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import tensorflow as tf
from tensorflow.keras import layers
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env

# PyBoyの初期化
pyboy = PyBoy('roms/pokemon_red.gb')

import gymnasium as gym
from gymnasium import spaces
import numpy as np


class PokemonEnv(gym.Env):
    def __init__(self, pyboy):
        super(PokemonEnv, self).__init__()
        self.pyboy = pyboy
        self.action_space = spaces.Discrete(5)  # 上下左右とAボタン
        self.observation_space = spaces.Box(0, 1024, (18, 20), dtype=np.uint32)
        self.state = None

    def step(self, action):
        if action == 0:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
            self.pyboy.tick(18)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
        elif action == 1:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            self.pyboy.tick(18)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        elif action == 2:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            self.pyboy.tick(18)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        elif action == 3:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            self.pyboy.tick(18)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif action == 4:
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            self.pyboy.tick(18)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)

        # 状態と報酬の取得
        obs = self.get_screen()
        reward = self.calculate_reward()
        done = self.is_done()
        truncated = False  # エピソードが途中で打ち切られた場合（今回は常にFalse）
        return obs, reward, done, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
        self.state = "start"
        self.pyboy.tick()  # エミュレータを1フレーム進める
        return self.get_screen(), {}

    def get_screen(self):
        # エミュレータの画面を取得
        return self.pyboy.game_area()

    def calculate_reward(self):
        reward = 0

        # 状態に基づいて報酬を計算
        if self.state == "start":
            if self.check_conversation_with_oak():
                reward += 10
                self.state = "name_selection"

        elif self.state == "name_selection":
            if self.check_name_selected():
                reward += 10
                self.state = "in_room"

        elif self.state == "in_room":
            if self.check_left_room():
                reward += 10
                self.state = "in_house"

        elif self.state == "in_house":
            if self.check_left_house():
                reward += 10
                self.state = "outside"

        elif self.state == "outside":
            if self.check_entered_grass():
                reward += 20
                self.state = "with_oak"

        elif self.state == "with_oak":
            if self.check_received_pokemon():
                reward += 30
                self.state = "end"

        return reward

    def is_done(self):
        return self.state == "end"

    def check_conversation_with_oak(self):
        # オーキド博士との会話が進んでいるかどうかを判定
        return False

    def check_name_selected(self):
        # 名前が選択されたかどうかを判定
        return False

    def check_left_room(self):
        # 部屋から出たかどうかを判定
        return False

    def check_left_house(self):
        # 家から出たかどうかを判定
        return False

    def check_entered_grass(self):
        # 草むらに入ったかどうかを判定
        return False

    def check_received_pokemon(self):
        return False

# 環境のチェック
env = PokemonEnv(pyboy)
check_env(env)

# DQNモデルの作成
model = DQN('MlpPolicy', env, verbose=1)

# 学習
model.learn(total_timesteps=50000)

# モデルの保存
model.save("dqn_pokemon")

# モデルの読み込み
model = DQN.load("dqn_pokemon")

# テスト
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, done, truncated, info = env.step(action)
    if done or truncated:
        obs = env.reset()

print('This is end.')
