from openai_wrapper.chat_completion import chat_completion
from aws_wrapper.dynamodb import get_connection_id
from aws_wrapper.apigatewaymanagementapi import send_websocket_message
import json
import time
import logging
from openai_wrapper.prompts.transport_prompt import transport_prompt

from openai_wrapper.prompts.battle_prompt import BATTLE_PROMPT

logging.basicConfig(
    level=logging.INFO,  # ログレベルを設定（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # ログメッセージのフォーマットを設定
    filename='logs/app.log',  # 出力先のログファイル名を指定
    filemode='a'  # 'a'は追記モード、'w'は上書きモード
)
logger = logging.getLogger(__name__)


actions = []
actions_logs = []

while True:
    time.sleep(1)
    if len(actions) > 0:
        next_action = actions.pop()
        connection_id = get_connection_id()
        actions_logs.append(json.dumps(next_action))
        if len(actions_logs) > 100:
            actions_logs.pop(0)
        send_websocket_message(connection_id, json.dumps(next_action))
    else:
        with open('array.json', 'r') as f:
            array_list = json.load(f)
            response = chat_completion(
                '次の行動を教えて下さい',
                transport_prompt(json.dumps(array_list), actions_logs)
            )
            content = response.choices[0].message.content
            print(f'content: {content}')
            logger.info(content)
            next_actions = json.loads(content)
            commands = next_actions['commands']
            if isinstance(commands, list):
                actions.extend(commands)
            else:
                actions.append(commands)
