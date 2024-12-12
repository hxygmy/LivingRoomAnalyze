from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, DeliveryGuarantee, KafkaOffsetsInitializer, KafkaRecordSerializationSchema
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.functions import MapFunction, FlatMapFunction
from pyflink.common.watermark_strategy import WatermarkStrategy
import jieba
from collections import Counter
import json
import time

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env.add_jars("file:///opt/flink-1.20.0/lib/flink-sql-connector-kafka-1.17.2.jar")
env.add_jars("file:///opt/Guava-33.3.1/guava-30.0-jre.jar")
kafka_servers = "209a01:9092,209a02:9092,209a03:9092"

source_topic = "crawler_topic"
sink_topic = "word_topic"

kafka_source = KafkaSource.builder() \
    .set_bootstrap_servers(kafka_servers) \
    .set_topics(source_topic) \
    .set_group_id("crawler_group") \
    .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

ds = env.from_source(
    source=kafka_source,
    watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
    source_name="Kafka Source"
)

# 注册一个flatmap，使用 jieba 进行分词，并计算词频
class JiebaTokenizerFlatMap(FlatMapFunction):
    def flat_map(self, value):
        words = jieba.lcut(value)
        word_freq = Counter(words)
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = {"time": f'{timestamp_str}'}
        result.update(word_freq)
        yield json.dumps(result, ensure_ascii=False)

word_freq_ds = ds.flat_map(JiebaTokenizerFlatMap(), Types.STRING())

schema = SimpleStringSchema()
serializer = KafkaRecordSerializationSchema.builder() \
    .set_topic(sink_topic) \
    .set_value_serialization_schema(schema) \
    .build()
kafka_sink = KafkaSink.builder() \
    .set_bootstrap_servers(kafka_servers) \
    .set_record_serializer(serializer) \
    .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
    .build()

# 将结果写入 Kafka Sink
word_freq_ds.sink_to(kafka_sink)

# 开始执行程序
env.execute("Crawler Topic Word Frequency Calculation")