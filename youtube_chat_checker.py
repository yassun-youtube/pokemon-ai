from extra.youtube_chat_controller import chat_list
import re
from aws_wrapper.dynamodb import get_connection_id
from aws_wrapper.apigatewaymanagementapi import send_websocket_message
import json
import time

connection_id = get_connection_id()

etags = set()

def check_chat_and_control_pyboy():
    print('check_chat_and_control_pyboy')
    chats = chat_list()
    for chat in chats:
        if chat['etag'] in etags:
            continue

        etags.add(chat['etag'])

        commands = []

        if re.match(r'a|A', chat['message']):
            commands.append('a')
        if re.match(r'b|B', chat['message']):
            commands.append('b')
        if re.match(r'↑', chat['message']):
            commands.append('move_up')
        if re.match(r'→', chat['message']):
            commands.append('move_right')
        if re.match(r'↓', chat['message']):
            commands.append('move_down')
        if re.match(r'←', chat['message']):
            commands.append('move_left')

        for command in commands:
            send_websocket_message(connection_id, json.dumps({'action': command}))

while True:
    check_chat_and_control_pyboy()
    time.sleep(3)
