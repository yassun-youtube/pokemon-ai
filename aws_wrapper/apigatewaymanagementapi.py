import boto3
import base64

# パラメータの設定
region = "ap-northeast-1"
endpoint_url = "https://s07tuceu77.execute-api.ap-northeast-1.amazonaws.com/dev/"

def send_websocket_message(connection_id, message):
    # boto3クライアントの作成
    client = boto3.client('apigatewaymanagementapi', region_name=region, endpoint_url=endpoint_url)

    # メッセージをバイト列に変換
    message_bytes = message.encode('utf-8')
    # base64_string = base64.b64encode(message_bytes)

    # API呼び出し
    try:
        response = client.post_to_connection(
            ConnectionId=connection_id,
            Data=message_bytes
        )
        print("Message posted successfully")
    except client.exceptions.GoneException:
        print("The connection is no longer available.")
    except client.exceptions.LimitExceededException:
        print("You have exceeded a throttling limit.")
    except client.exceptions.PayloadTooLargeException:
        print("The data payload is too large.")
    except client.exceptions.ForbiddenException:
        print("The request is forbidden.")
    except client.exceptions.BadRequestException:
        print("The request is not formatted correctly.")
    except client.exceptions.ServiceUnavailableException:
        print("The service is currently unavailable.")
    except Exception as e:
        print("An unexpected error occurred:", e)
