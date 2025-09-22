import streamlit as st
import datetime
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# -------------------- 页面配置 --------------------
st.set_page_config(
    page_title="CTC Cryptocurrency Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CSS 样式 --------------------
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #e0f7fa, #ffffff);
    }
    .main-header {
        font-size: 3rem;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .news-card {
        background-color: #ffffffcc;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
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
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: grey;
        font-size: 0.9em;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- 标题 --------------------
st.markdown('<h1 class="main-header">🚀 CTC Smart Cryptocurrency Assistant</h1>', unsafe_allow_html=True)

# -------------------- 侧边栏 --------------------
st.sidebar.header("用户设置")
token_symbol = st.sidebar.text_input("请输入加密货币代码 (如 BTC, ETH):", "BTC", key="sidebar_token").upper()
debug_mode = st.sidebar.checkbox("启用调试模式", value=True, key="sidebar_debug")

# -------------------- 时间显示 --------------------
st.sidebar.write("🕒 当前时间（Sydney）:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# -------------------- 主体布局 --------------------
col1, col2 = st.columns([1,2])

# --------- 代币价格分析 ---------
with col1:
    if st.button("📈 分析价格", key="btn_price"):
        n8n_price_url = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
        payload = {"token": token_symbol}
        auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')
        
        try:
            response = requests.post(n8n_price_url, json=payload, auth=auth, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 支持列表或字典格式
            if isinstance(data, list) and len(data) > 0 and 'json' in data[0]:
                data = data[0]['json']
            elif isinstance(data, list) and len(data) > 0:
                data = data[0]

            # 展示价格
            price = data.get("price")
            change_24h = data.get("change_24h", "0%")
            token_name = data.get("token", token_symbol)
            
            if price:
                change_value = float(change_24h.strip('%'))
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(label=f"{token_name} 价格", value=f"${price:,.2f}", delta=f"{change_24h}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if change_value >= 0:
                    st.info(f"过去24小时内，{token_name}价格上涨了 {change_24h}")
                else:
                    st.warning(f"过去24小时内，{token_name}价格下跌了 {change_24h.replace('-', '')}")
            else:
                st.error("无法获取价格信息")
            
            if debug_mode:
                st.write("调试信息:", data)
                
        except Exception as e:
            st.error(f"请求价格失败: {str(e)}")

# --------- 新闻与情绪分析 ---------
with col2:
    if st.button("📰 获取新闻与情绪分析", key="btn_news"):
        n8n_news_url = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"  # 替换为你的新闻 webhook
        payload = {"token": token_symbol}
        auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')
        
        try:
            response = requests.post(n8n_news_url, json=payload, auth=auth, timeout=10)
            response.raise_for_status()
            news_data = response.json()
            
            # 支持列表格式
            if isinstance(news_data, dict):
                news_data = [news_data]
            
            for item in news_data:
                st.markdown('<div class="news-card">', unsafe_allow_html=True)
                st.subheader(item.get("title", "无标题"))
                st.write(f"📰 来源: {item.get('source','未知')} | 📅 时间: {item.get('published_at','未知')}")
                st.write(f"[阅读原文]({item.get('url','#')})")
                
                sentiment = item.get("sentiment", {})
                if sentiment:
                    df = pd.DataFrame([sentiment])
                    st.dataframe(df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if debug_mode:
                st.write("调试信息:", news_data)
            
        except Exception as e:
            st.error(f"请求新闻失败: {str(e)}")

# -------------------- 页脚 --------------------
st.markdown("---")
st.markdown('<p class="footer">CTC Smart Cryptocurrency Recommendation Assistant © 2023 | 新闻数据由 Cryptopanic 提供</p>', unsafe_allow_html=True)
