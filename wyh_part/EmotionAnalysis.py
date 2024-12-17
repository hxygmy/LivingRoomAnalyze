from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.functions import MapFunction
from pyflink.datastream.connectors.kafka import KafkaSink, KafkaRecordSerializationSchema, DeliveryGuarantee
import requests
import json
cnt=0
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=SBIcUzxrrpQE2Re2zY8AYqVE&client_secret=vfxooxG7q1JEWbEzEkDXy8UCdpybrTcz"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def get_response(content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()
    emotion=["happy","exciting","middle","sad","angry"]
    payload = json.dumps({
        "messages": [

    {
        "role": "user",
        "content": "你要为接下来我给你的一句话做情感分析，你需要考虑五种情绪：happy,exciting,middle,sad,angry。你只需要返回我以上五种情绪中的一个词！另外不需要句号！例如：happy 输出你对以下句子的答案："+content
    }
    ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        for i in emotion:
            if i in response.json()['result']:
                return {"id{cnt}":{"emotion":i}}
    except:
        pass            
class MyMapFunction(MapFunction):
    def map(self, value):
        return get_response(value)


# 初始化执行环境
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(2)

env.add_jars("file:///opt/flink-1.20.0/lib/flink-sql-connector-kafka-1.17.2.jar")
env.add_jars("file:///opt/Guava-33.3.1/guava-30.0-jre.jar")

# Kafka 源配置
kafka_servers = "209a01:9092,209a02:9092,209a03:9092"
source_topic = "emotion_topic"
consume_group_id = "hxy"

# 创建 Kafka Source
kafka_source = KafkaSource \
    .builder() \
    .set_bootstrap_servers(kafka_servers) \
    .set_topics(source_topic) \
    .set_group_id(consume_group_id) \
    .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

# 添加数据源到流环境中
ds = env.from_source(
    source=kafka_source,
    watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
    source_name="Kafka Source"
)

# ds = ds.map(lambda x: process_function(x))

# 打印从 Kafka 获取的数据到控制台

ds= ds.map(MyMapFunction(), Types.STRING())


schema = SimpleStringSchema()
serializer = KafkaRecordSerializationSchema.builder() \
    .set_topic("EmotionResult") \
    .set_value_serialization_schema(schema) \
    .build()
kafka_sink = KafkaSink.builder() \
    .set_bootstrap_servers(kafka_servers).set_record_serializer(serializer) \
    .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
    .build()

# 将结果写入 Kafka Sink
ds.sink_to(kafka_sink)

# 开始执行程序
env.execute("Flink Kafka Consumer Example")
