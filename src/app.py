import streamlit as st
import datetime
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# ---------------- 页面配置 ----------------
st.set_page_config(
    page_title="CTC Crypto Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS 样式 ----------------
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
.metric-card, .advice-card {
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

# ---------------- 标题 ----------------
st.markdown('<h1 class="main-header">🚀 CTC Smart Cryptocurrency Assistant</h1>', unsafe_allow_html=True)

# ---------------- 侧边栏 ----------------
st.sidebar.header("用户设置")
token_symbol = st.sidebar.text_input("请输入加密货币代码 (如 BTC, ETH):", "BTC", key="sidebar_token").upper()
debug_mode = st.sidebar.checkbox("启用调试模式", value=True, key="sidebar_debug")
st.sidebar.write("🕒 当前时间（Sydney）:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ---------------- 主体布局 ----------------
col1, col2 = st.columns([1,2])

with col1:
    st.markdown("### 输入设置")
    st.write(f"代币: **{token_symbol}**")
    if st.button("获取价格与新闻", key="btn_fetch"):
        # ----------- 请求价格 -----------
        n8n_price_url = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
        payload = {"token": token_symbol}
        auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')
        
        try:
            response = requests.post(n8n_price_url, json=payload, auth=auth, timeout=10)
            response.raise_for_status()
            price_data = response.json()
            if isinstance(price_data, list) and len(price_data)>0 and 'json' in price_data[0]:
                price_data = price_data[0]['json']
            elif isinstance(price_data, list) and len(price_data)>0:
                price_data = price_data[0]
        except Exception as e:
            st.error(f"请求价格失败: {e}")
            price_data = {}
        
        # ----------- 请求新闻 -----------
        try:
            response = requests.post(n8n_price_url, json=payload, auth=auth, timeout=10)
            response.raise_for_status()
            news_data = response.json()
            if isinstance(news_data, dict):
                news_data = [news_data]
        except Exception as e:
            st.error(f"请求新闻失败: {e}")
            news_data = []

        # ----------- 显示价格与建议 -----------
        price = price_data.get("price")
        change_24h = price_data.get("change_24h","0%")
        token_name = price_data.get("token", token_symbol)

        if price:
            col2.markdown('<div class="metric-card">', unsafe_allow_html=True)
            col2.metric(label=f"{token_name} 当前价格", value=f"${price:,.2f}", delta=f"{change_24h}")
            col2.markdown('</div>', unsafe_allow_html=True)
            
            change_value = float(change_24h.strip('%'))
            # ----------- 实时建议框 -----------
            advice_text = "📈 建议：看涨" if change_value >=0 else "📉 建议：看跌"
            col2.markdown('<div class="advice-card">', unsafe_allow_html=True)
            col2.markdown(f"### {advice_text}")
            col2.markdown('</div>', unsafe_allow_html=True)
        else:
            col2.error("无法获取价格信息")

        # ----------- 展示新闻 -----------
        col2.markdown("### 📰 最新新闻与情绪分析")
        for item in news_data:
            col2.markdown('<div class="news-card">', unsafe_allow_html=True)
            col2.subheader(item.get("title","无标题"))
            col2.write(f"📰 来源: {item.get('source','未知')} | 📅 时间: {item.get('published_at','未知')}")
            col2.write(f"[阅读原文]({item.get('url','#')})")
            sentiment = item.get("sentiment",{})
            if sentiment:
                df = pd.DataFrame([sentiment])
                col2.dataframe(df, use_container_width=True)
            col2.markdown('</div>', unsafe_allow_html=True)

        if debug_mode:
            st.write("调试信息: 价格数据", price_data)
            st.write("调试信息: 新闻数据", news_data)

# ---------------- 页脚 ----------------
st.markdown("---")
st.markdown('<p class="footer">CTC Smart Cryptocurrency Assistant © 2023 | 新闻数据由 Cryptopanic 提供</p>', unsafe_allow_html=True)
