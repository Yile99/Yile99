import streamlit as st
import datetime
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# -------------------------------
# 页面配置与样式
# -------------------------------
st.set_page_config(page_title="CTC Crypto Assistant", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
body {
    background: linear-gradient(to right, #e0f7fa, #ffffff);
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
    box-shadow: 0 6px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    text-align: center;
}
.positive-change {
    color: green;
    font-weight: bold;
    font-size: 1.2rem;
}
.negative-change {
    color: red;
    font-weight: bold;
    font-size: 1.2rem;
}
.news-card {
    background-color: #ffffffcc;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 CTC Smart Cryptocurrency Recommendation Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# 侧边栏输入
# -------------------------------
st.sidebar.header("设置")
token_symbol = st.sidebar.text_input("请输入加密货币代码 (如 BTC, ETH):", "BTC").upper()
debug_mode = st.sidebar.checkbox("启用调试模式", value=True)

# -------------------------------
# 主布局
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.write("当前时间 (Sydney):", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if st.button("获取实时分析"):
        with st.spinner("获取数据中..."):
            # -------------------------------
            # n8n webhook 配置
            # -------------------------------
            WEBHOOK_URL = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
            auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')
            payload = {"token": token_symbol}
            
            try:
                response = requests.post(WEBHOOK_URL, json=payload, auth=auth, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if debug_mode:
                    st.markdown("### 调试信息")
                    st.write("请求 URL:", WEBHOOK_URL)
                    st.write("请求 payload:", payload)
                    st.write("响应内容:", data)
                
                # -------------------------------
                # 解析价格信息
                # -------------------------------
                if isinstance(data, list) and len(data) > 0:
                    data = data[0].get("json", data[0])
                
                price = data.get("price")
                change_24h = data.get("change_24h", "0%")
                message = data.get("message", "")
                
                # -------------------------------
                # 右侧显示
                # -------------------------------
                with col2:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.subheader(f"{token_symbol} 实时分析")
                    if message:
                        st.write(f"状态信息: {message}")
                    if price is not None:
                        st.write(f"价格: ${price:,.2f}")
                        change_value = float(change_24h.strip('%'))
                        trend = "上涨 📈" if change_value >=0 else "下跌 📉"
                        trend_class = "positive-change" if change_value >=0 else "negative-change"
                        st.markdown(f"<p class='{trend_class}'>过去24小时: {trend} ({change_24h})</p>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # -------------------------------
                    # 新闻展示
                    # -------------------------------
                    news_list = data.get("news", [])
                    if news_list:
                        st.subheader("最新新闻与情绪")
                        for item in news_list:
                            st.markdown('<div class="news-card">', unsafe_allow_html=True)
                            st.write(f"**标题:** {item.get('title','无标题')}")
                            st.write(f"📰 来源: {item.get('source','未知')} | 📅 {item.get('published_at','未知')}")
                            st.write(f"[阅读原文]({item.get('url','#')})")
                            sentiment = item.get("sentiment", {})
                            if sentiment:
                                df = pd.DataFrame([sentiment])
                                st.dataframe(df, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("暂无新闻数据")
            
            except requests.exceptions.RequestException as e:
                st.error(f"请求失败: {str(e)}")

# -------------------------------
# 页脚
# -------------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>CTC Smart Cryptocurrency Recommendation Assistant © 2023</p>", unsafe_allow_html=True)
