import pymysql
from openai import OpenAI

# 1. 基础配置：请替换为你真实的 Kimi 密钥和 MySQL 密码
client = OpenAI(api_key="sk-kengWMoxgQSU9DLEjDv356Vhd6iSqqj4avdvysepkpBnsgfI", base_url="https://api.moonshot.cn/v1")
DB_CONFIG = {
    "host": "112.124.3.144",  # 👈 核心修改：指向你的云端服务器 IP
    "port": 3306,             # 👈 端口号
    "user": "x_agent_market", # 👈 核心修改：使用宝塔面板分配的数据库用户名
    "password": "123456",     # 👈 保持你的密码
    "db": "x_agent_market",   # 👈 数据库名称
    "charset": "utf8mb4"
}
# 2. 核心提示词：将数据库的“骨架”和“查询潜规则”喂给大模型
SCHEMA_INFO = """
你现在可以访问一个实体店的数据库，包含以下表结构：
- t_user_asset (用户资产表): user_id, user_name, member_level(会员等级，如'高级合规账户'), points(积分), balance(余额), total_consumed(总消费)
- t_coupon (卡券表): coupon_id, coupon_name, discount, stock(库存)
- t_order (订单表): order_id, user_id, final_price, status, create_time

【DBA 强制查询规则】：
在处理文本字段（如 member_level, user_name, coupon_name 等）的条件过滤时，请务必使用 LIKE '%关键字%' 进行模糊搜索，绝对不要使用严格的 '='，以防止用户输入的缩写与数据库存储不完全一致。
"""
def text_to_sql_agent(user_question):
    print(f"👨‍💼 业务人员提问: {user_question}\n" + "-"*40)

    # 【步骤一：大模型大脑翻译自然语言 -> SQL】
    sql_prompt = f"作为资深DBA，请根据以下数据库结构，将用户的自然语言问题转化为精准的MySQL查询语句。\n结构：\n{SCHEMA_INFO}\n问题：{user_question}\n【严格要求】只返回纯SQL语句，不要任何解释，不要带 markdown 代码块符号。"

    res = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[{"role": "user", "content": sql_prompt}]
    )
    # 模糊清洗：剥离可能携带的 markdown 标记
    sql_query = res.choices[0].message.content.replace("```sql", "").replace("```", "").strip()
    print(f"⚙️ [Agent 生成 SQL 语句]: {sql_query}")

    # 【步骤二：安全沙盒拦截 (Read-Only 机制)】
    if any(keyword in sql_query.lower() for keyword in ["drop", "delete", "update", "insert", "alter"]):
        return "⚠️ 安全网关拦截：检测到危险的写库操作！BI 分析 Agent 仅拥有只读（Read-Only）权限。"

    # 【步骤三：执行 SQL 查询获取物理数据】
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_query)
        db_results = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"❌ 数据库执行异常：{str(e)}"

    if not db_results:
        return "📊 数据大盘：没有查询到符合条件的数据。"

    # 【步骤四：数据二次组装，生成商业洞察报告】
    insight_prompt = f"用户原始问题：{user_question}\n数据库查询出的生数据：{db_results}\n请作为高级商业数据分析师，用通俗易懂、专业的高级口吻，为业务总监总结一份简短的数据报告。"

    insight_res = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[{"role": "user", "content": insight_prompt}]
    )

    return insight_res.choices[0].message.content

# 测试点火运行
if __name__ == "__main__":
    # 你可以随便换问题，比如："帮我查一下系统里有哪些高级合规账户？" 或者 "系统里剩余库存少于 60 的卡券有哪些？"
    question = "帮我查一下目前系统里有哪些高级合规账户，以及他们的总消费金额？"
    report = text_to_sql_agent(question)
    print("\n📈 [BI Agent 商业洞察报告]:\n" + report)