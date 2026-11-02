# 智扫通 · 扫地机器人智能客服 Agent

基于 LangChain 1.x + LangGraph 的智能客服 Agent 示例项目：ReAct 自主决策、多工具编排、RAG 知识检索、中间件监控与意图驱动的提示词动态切换，前端使用 Streamlit 提供流式对话。

## 功能

- **ReAct Agent**：模型自主判断是否需要工具、调用哪个工具、返回信息是否足够，不足则再次调用
- **7 个工具**：知识检索、天气查询、用户定位、用户 ID、当前月份、使用记录查询、报告上下文注入
- **RAG 检索**：PDF/TXT 解析 → 中文友好分片 → DashScope 向量化 → Chroma 持久化 → top-k 检索
- **增量入库**：按文件 MD5 去重，已入库文件自动跳过
- **中间件层**：工具调用监控、参数日志、异常捕获、模型调用前上下文日志
- **意图驱动的提示词切换**：识别到「生成报告」意图后，`@dynamic_prompt` 自动切换为报告生成提示词
- **个性化报告**：按 `user_id + month` 检索使用记录，生成 Markdown 报告与维护建议

## 架构

```
用户
 └─ Streamlit (app.py)
     └─ ReactAgent (agent/react_agent.py, create_agent)
         ├─ 中间件：monitor_tool / log_before_model / report_context_switch / report_prompt_switch
         ├─ 工具：rag_summarize / get_weather / get_user_location / get_user_id
         │        / get_current_month / fetch_external_data / fill_context_for_report
         └─ RAG：Chroma + DashScope Embedding + DeepSeek Chat（OpenAI 兼容接口）
```

## 目录结构

```
├── app.py                  # Streamlit 前端
├── agent/
│   ├── react_agent.py      # Agent 构建与流式输出
│   └── tools/
│       ├── agent_tools.py  # 工具定义
│       └── middleware.py   # 中间件
├── rag/
│   ├── vector_store.py     # 向量库与增量入库
│   └── rag_service.py      # 检索 + 总结链
├── model/factory.py        # 模型工厂（DeepSeek / DashScope）
├── prompts/                # 系统提示词、RAG 提示词、报告提示词
├── config/                 # YAML 配置
├── data/                   # 知识库文档与结构化记录
└── utils/                  # 路径、日志、配置、文件处理
```

## 快速开始

```bash
pip install -r requirements.txt

# 1. 配置密钥
cp .env.example .env      # Windows: copy .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY 和 DASHSCOPE_API_KEY

# 2. 首次构建知识库（向量库不进仓库，需要本地生成）
python -m rag.vector_store

# 3. 命令行运行
python -m agent.react_agent

# 4. Web 界面
streamlit run app.py
```

## 配置说明

| 文件 | 内容 |
|---|---|
| `config/rag.yml` | 对话模型名、嵌入模型名、服务地址 |
| `config/chroma.yml` | 向量库集合、持久化目录、分片参数、检索 top-k |
| `config/agent.yml` | 外部使用记录数据路径 |
| `config/prompt.yml` | 各提示词文件路径 |

## 说明

- 项目初始框架来自 LangChain 课程实践，在此基础上完成了代码实现与二次开发。
- `get_weather`、`get_user_location`、`get_user_id`、`get_current_month` 为演示用的模拟数据源。
- 不要提交 `.env`；`.env`、`chroma_db/`、`md5.text` 均已在 `.gitignore` 中排除。
