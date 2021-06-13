# SmartChatBot
中文问答机器人

## 项目说明
第一版是基于检索的。使用TFIDF生成向量，用余弦相似度计算最相近的提问，返回提问对应的回答。

## 使用说明
### 启动服务
python api_server.py &

### 测试服务是否正常
python client.py
