#!/bin/bash


# メッセージをBase64エンコード
MESSAGE=$(echo '{"action":"save_state"}' | base64)

CONNECTION_ID=$(aws dynamodb get-item --table-name ConnectionId --key '{"player": {"S": "yassun"}}' | jq -r '.Item.connectionId.S')
aws apigatewaymanagementapi post-to-connection --connection-id $CONNECTION_ID --data "$MESSAGE"  --region ap-northeast-1 --endpoint-url https://s07tuceu77.execute-api.ap-northeast-1.amazonaws.com/dev/

