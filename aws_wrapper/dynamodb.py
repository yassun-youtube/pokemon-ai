import boto3

import boto3

# DynamoDBクライアントの作成
dynamodb = boto3.client('dynamodb', region_name='ap-northeast-1')

# テーブル名とキーを設定
table_name = 'ConnectionId'
key = {
    'player': {'S': 'yassun'}
}

def get_connection_id():
    # アイテムを取得
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key=key
        )

        item = response.get('Item')

        if item:
            # print("Item found:", item)
            return item['connectionId']['S']
        else:
            print("Item not found")
    except Exception as e:
        print("Error fetching item from DynamoDB:", e)
