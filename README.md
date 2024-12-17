# LivingRoomAnalyze

## 研究目的
- 通过实现一个基于Flink实时数据处理的Demo，来熟悉当代分布式数据系统的理论原理，尤其是实时数据处理，容错机制等。

## 研究方法
- 爬取Bilibili的视频或直播间的弹幕，通过Flink与Kafka协作进行实时分词、情感分析，并实时通过词云的方式对以上分析输出展示。

## 研究结果
- 我们通过PyFlink实现了该项目，组员分工基于个人研究，并均对该处理流程的理解有了显著的提升。
- 验证了Flink的目前实现不是很完善的Checkpoint机制，这也是Flink，乃至数据流系统都在寻求一个Robust的解决方案的研究领域。

## 小组分工
|        | 学号        | 导师   | 负责模块                | 贡献占比 |
| ------ | ----------- | ------ | ----------------------- | -------- |
| 王韩   | 51275903005 | 王晔   | 弹幕爬虫                | 25%      |
| 何晓宇 | 51275903016 | 黄波   | 项目架构搭建 \ 分词部分 | 25%      |
| 史雪涛 | 51275903021 | 王伟   | 时间窗口聚合 \ 实时展示 | 25%      |
| 王一涵 | 51275903047 | 胡文心 | 情感分析                | 25%      |



## Desription

A distributed project which developed by me and my beloved sons to analyze living room data in real time.

##
これは私たちの最高のプロジェクト！万歳！

And this project is build for our 2024-Fall-[Distributed Computing System](https://dasebigdata.github.io/) Course (SWEN6211102015) in DaSE ECNU.
