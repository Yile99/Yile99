import streamlit as st
import datetime
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# ---------------------- 页面配置 ----------------------
st.set_page_config(page_title="CTC Cryptocurrency Assistant", layout="wide")

# ---------------------- CSS 样式 ----------------------
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .positive-change {
        color: green;
        font-weight: bold;
    }
    .negative-change {
        color: red;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E90FF;
        color: white;
    }
    .debug-info {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #6c757d;
        font-family: monospace;
        font-size: 0.9em;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- 页面标题 ----------------------
st.markdown('<h1 class="main-header">🚀 CTC Smart Cryptocurrency Recommendation Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# ---------------------- 输入区 ----------------------
col_input, col_result = st.columns([1, 2])

with col_input:
    st.write("Sydney:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 输入代币代码
    token_symbol = st.text_input("请输入加密货币代码 (如 BTC, ETH):", "BTC", key="token_input")

    # 调试模式开关
    debug_mode = st.checkbox("启用调试模式", value=True, key="debug_mode")

    # 按钮
    analyze_price_btn = st.button("分析价格", key="btn_price")
    analyze_news_btn = st.button("获取新闻与情绪分析", key="btn_news")

with col_result:
    result_placeholder = st.empty()

# ---------------------- n8n Webhook 配置 ----------------------
PRICE_WEBHOOK_URL = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
NEWS_WEBHOOK_URL = "https://ct012.app.n8n.cloud/webhook/your-workflow-id/crypto-news"

auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')

# ---------------------- 处理价格分析 ----------------------
if analyze_price_btn:
    with st.spinner('AI正在努力分析价格...'):
        payload = {"token": token_symbol}
        try:
            response = requests.post(PRICE_WEBHOOK_URL, json=payload, auth=auth, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0].get('json', data[0])
            if debug_mode:
                st.markdown("### 调试信息")
                st.write("请求 URL:", PRICE_WEBHOOK_URL)
                st.write("请求 payload:", payload)
                st.write("响应数据:", data)

            # 显示价格
            price = data.get('price')
            change_24h = data.get('change_24h', '0%')
            token_name = data.get('token', token_symbol)

            if price is not None:
                change_value = float(change_24h.strip('%'))
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(label=f"{token_name} 价格", value=f"${price:,.2f}", delta=f"{change_24h}")
                st.markdown('</div>', unsafe_allow_html=True)
                if change_value >= 0:
                    st.info(f"过去24小时内，{token_name}价格上涨了{change_24h}")
                else:
                    st.warning(f"过去24小时内，{token_name}价格下跌了{change_24h.replace('-', '')}")
            else:
                st.error("无法获取价格信息")
                if debug_mode:
                    st.write("可用数据键:", list(data.keys()))

        except Exception as e:
            st.error(f"获取价格时发生错误: {str(e)}")

# ---------------------- 处理新闻与情绪 ----------------------
if analyze_news_btn:
    with st.spinner('AI正在获取新闻与情绪分析...'):
        payload = {"token": token_symbol}
        try:
            response = requests.post(NEWS_WEBHOOK_URL, json=payload, auth=auth, timeout=10)
            response.raise_for_status()
            news_data = response.json()
            if debug_mode:
                st.markdown("### 调试信息")
                st.write("请求 URL:", NEWS_WEBHOOK_URL)
                st.write("请求 payload:", payload)
                st.write("响应数据:", news_data)

            for item in news_data:
                st.subheader(item.get("title", "无标题"))
                st.write(f"📰 来源: {item.get('source', '未知')} | 📅 时间: {item.get('published_at', '未知')}")
                st.write(f"[阅读原文]({item.get('url', '#')})")
                sentiment = item.get("sentiment", {})
                if sentiment:
                    df = pd.DataFrame([sentiment])
                    st.dataframe(df, use_container_width=True)
                st.markdown("---")

        except Exception as e:
            st.error(f"获取新闻时发生错误: {str(e)}")

# ---------------------- 使用说明 ----------------------
with st.expander("使用说明"):
    st.markdown("""
    1. 输入加密货币代码（如BTC、ETH）
    2. 点击“分析价格”按钮获取代币价格
    3. 点击“获取新闻与情绪分析”按钮获取新闻和情绪
    4. 启用调试模式可以查看详细请求和响应信息
    """)

# ---------------------- 页脚 ----------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>CTC Smart Cryptocurrency Recommendation Assistant © 2023</p>", unsafe_allow_html=True)
