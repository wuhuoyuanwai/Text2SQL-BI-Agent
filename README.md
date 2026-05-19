\# 📊 Text2SQL-BI-Agent (智能商业数据洞察引擎)



!\[Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square\&logo=python)

!\[LLM](https://img.shields.io/badge/AI\_Model-Moonshot\_LLM-10b981?style=flat-square)

!\[Database](https://img.shields.io/badge/Database-MySQL\_8.0-4479A1?style=flat-square\&logo=mysql)

!\[Architecture](https://img.shields.io/badge/Architecture-Text--to--SQL-ff453a?style=flat-square)



基于 \*\*大语言模型 (LLM) + 数据库 Schema 提示工程\*\* 构建的下一代交互式商业智能 (BI) Agent。

本项目旨在打破传统数据分析的专业门槛，允许业务运营人员通过自然语言（人话）直接查询底层关系型数据库，并自动生成高管视角的数据洞察报告，实现从“冰冷数据”到“商业决策”的端到端自动化。



\## ✨ 核心硬核特性 (Core Features)



\* \*\*🧠 精准 Text-to-SQL 翻译引擎：\*\* 通过深度优化的 Prompt Engineering，将底层 MySQL 的表结构（Schema）与查询潜规则（如：强制使用 LIKE 进行模糊匹配）注入大模型上下文，实现自然语言到复杂 SQL 语句的精准降维转换。

\* \*\*🛡️ 工业级安全沙盒 (Read-Only 拦截)：\*\* 针对 LLM 生成代码的不确定性，在底层执行引擎前置了严格的 SQL 语法沙盒。通过代码层面的硬编码正则校验，强制拦截 `DROP`、`DELETE`、`UPDATE` 等危险指令，确保物理数据库绝对安全。

\* \*\*📈 Data-to-Text 商业洞察重构：\*\* 拒绝返回生硬的 JSON/二维表数据。Agent 会自动将拉取到的生数据回传给 LLM 进行二次消化，以“高级商业数据分析师”的口吻输出排版精良、具有业务指导意义的分析报告。

\* \*\*⚡ 极简高可用架构：\*\* 抛弃繁杂的中间件，采用最纯粹的 Python 驱动，实现秒级响应与公网数据库直连。



\## 🏗️ 引擎运转流 (Architecture Pipeline)



```text

\[ 业务人员 ] ──(自然语言: "帮我查一下高级合规账户的消费额")──▶ 

&#x20;      │

&#x20;      ▼

\[ Schema 提示工程装配中心 ] ──(注入表结构与查询规则)──▶ \[ Moonshot 大模型 ]

&#x20;      │

&#x20;      ◀──(返回生成的原始 SQL 语句)──

&#x20;      │

&#x20;      ▼

\[ 🛡️ 安全沙盒 / 读写隔离层 ] ──(阻断一切非 SELECT 操作)──▶ 

&#x20;      │

&#x20;      ▼

\[ 物理 MySQL 数据库 ] ──(执行查询拉取生数据)──▶ 

&#x20;      │

&#x20;      ▼

\[ 商业逻辑二次组装层 ] ──(生数据 + 业务问题 注入)──▶ \[ Moonshot 大模型 ]

&#x20;      │

&#x20;      ◀──(返回高管级数据分析报告)──

&#x20;      │

&#x20;      ▼

\[ 终端输出展示 ]

