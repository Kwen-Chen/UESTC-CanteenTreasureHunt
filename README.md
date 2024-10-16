# UESTC-CanteenTreasureHunt
通过自动化爬虫技术，我们收集学生在河畔论坛上关于食堂异物的帖子和评论，然后利用自然语言处理技术分析这些数据，提取事件发生的地点、异物类型以及后续处理情况。最终，我们将这些信息以直观的图表形式展示出来，帮助学校管理层和学生更好地了解食堂的食品安全状况。

## 项目结构

```
project/
│
├── run.py                 # 主执行脚本，负责解析参数并调用其他模块
├── run.sh                 # Shell 脚本，用于快速启动项目
├── utils/                 # 工具目录，包含辅助函数和模块
│   ├── analyse.py         # 分析模块，负责对收集的数据进行统计分析
│   ├── crawler.py         # 爬虫模块，负责从论坛抓取帖子和评论
│   └── generate.py        # 生成模块，负责与API交互生成分析结果
├── config/                # 配置文件目录
│   ├── cookie.txt         # 用于爬虫的cookie文件
│   └── config.yaml        # 配置文件，包含API信息等
├── log/                   # 日志文件目录
├── output/                # 输出文件目录
│   ├── page_link.json     # 保存帖子链接的JSON文件
│   ├── page_detail.jsonl  # 保存帖子详细信息的JSON Lines文件
│   └── data.jsonl         # 保存分析结果的JSON Lines文件
└── README.md              # 项目说明文件
```

## 快速开始

1. **安装依赖**：确保你的环境中安装了`requests`、`beautifulsoup4`、`tqdm`、`matplotlib`、`openai`和`pyyaml`。

2. **配置环境**：
   - 将`config/cookie.txt`替换为有效的论坛cookie。
   - 根据需要修改`config/config.yaml`中的API配置。

3. **运行项目**：
   - 在项目根目录下运行`./run.sh`或直接执行`python run.py`。

## 功能说明

- **爬虫**：自动从电子科技大学论坛抓取食堂异物相关的帖子和评论。
- **生成**：使用OpenAI API对帖子内容进行分析，提取事件发生地点、异物类型和后续处理信息。
- **分析**：对收集的数据进行统计分析，包括异物类型分布、事件地点分布和后续处理情况。

## 输出示例

项目将生成以下输出文件：

- `output/page_link.json`：包含所有帖子链接的JSON文件。
- `output/page_detail.jsonl`：包含帖子详细信息的JSON Lines文件。
- `output/data.jsonl`：包含分析结果的JSON Lines文件。

## 贡献

欢迎对项目进行贡献，包括但不限于：
- 增加新的数据源
- 改进分析算法
- 修复已知问题

