from kafka import KafkaProducer
from json import dumps

# Kafka连接配置
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# 读取文件并发送到Kafka
topic = "danmu"
with open('huawei.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 每行代表一条弹幕，去掉换行符
        danmu = line.strip()
        # 发送到Kafka
        producer.send(topic, value=danmu)

# 确保所有消息都已发送
producer.flush()

print("弹幕已发送完毕")
