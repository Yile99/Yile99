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
.news-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #1E90FF;
    margin-bottom: 5px;
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
                response = requests.post(WEBHOOK_URL, json=payload, auth=auth, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if debug_mode:
                    st.markdown("### 调试信息")
                    st.write("请求 URL:", WEBHOOK_URL)
                    st.write("请求 payload:", payload)
                    st.write("完整响应:", data)
                    st.write("响应类型:", type(data))
                    if isinstance(data, list):
                        st.write("数组长度:", len(data))
                        for i, item in enumerate(data):
                            st.write(f"第{i}个元素类型:", type(item))
                            st.write(f"第{i}个元素内容:", item)
                
                # 数据解析逻辑
                price = None
                change_24h = "0%"
                message = ""
                news_list = []
                
                # 处理n8n返回的数据结构
                if isinstance(data, list) and len(data) > 0:
                    # 取第一个元素，其中包含合并后的数据
                    item_data = data[0].get("json", data[0])
                    price = item_data.get("price")
                    change_24h = item_data.get("change_24h", "0%")
                    message = item_data.get("message", "")
                    news_list = item_data.get("news", [])
                else:
                    # 如果是对象格式
                    price = data.get("price")
                    change_24h = data.get("change_24h", "0%")
                    message = data.get("message", "")
                    news_list = data.get("news", [])
                
                # 确保news_list是列表
                if not isinstance(news_list, list):
                    news_list = []
                
                # -------------------------------
                # 右侧显示 - 价格信息
                # -------------------------------
                with col2:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.subheader(f"{token_symbol} 实时分析")
                    
                    if message:
                        st.write(f"状态信息: {message}")
                    
                    if price is not None:
                        # 格式化价格显示
                        try:
                            price_float = float(price)
                            st.write(f"价格: ${price_float:,.2f}")
                        except (ValueError, TypeError):
                            st.write(f"价格: {price}")
                        
                        # 显示24小时变化
                        try:
                            change_value = float(str(change_24h).strip('%'))
                            trend = "上涨 📈" if change_value >= 0 else "下跌 📉"
                            trend_class = "positive-change" if change_value >= 0 else "negative-change"
                            st.markdown(f"<p class='{trend_class}'>过去24小时: {trend} ({change_24h})</p>", unsafe_allow_html=True)
                        except ValueError:
                            st.write(f"过去24小时: {change_24h}")
                    else:
                        st.warning("未能获取到价格数据")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # -------------------------------
                    # 新闻展示
                    # -------------------------------
                    if news_list and len(news_list) > 0:
                        st.subheader(f"📰 最新{token_symbol}相关新闻")
                        
                        for i, news_item in enumerate(news_list):
                            if not isinstance(news_item, dict):
                                continue
                                
                            st.markdown('<div class="news-card">', unsafe_allow_html=True)
                            
                            # 标题
                            title = news_item.get('title', '无标题')
                            st.markdown(f'<div class="news-title">{i+1}. {title}</div>', unsafe_allow_html=True)
                            
                            # 来源和时间
                            source = news_item.get('source', '未知来源')
                            published_at = news_item.get('published_at', '未知时间')
                            st.write(f"**来源:** {source} | **时间:** {published_at}")
                            
                            # 链接
                            url = news_item.get('url', '#')
                            if url and url != '#':
                                st.markdown(f"[阅读原文 ↗]({url})")
                            
                            # 情绪分析（如果有）
                            votes = news_item.get('votes', {})
                            if votes:
                                st.write("**市场情绪分析:**")
                                cols = st.columns(3)
                                with cols[0]:
                                    positive = votes.get('positive', 0)
                                    st.metric("积极", positive)
                                with cols[1]:
                                    negative = votes.get('negative', 0)
                                    st.metric("消极", negative)
                                with cols[2]:
                                    important = votes.get('important', 0)
                                    st.metric("重要度", important)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("暂无相关新闻数据")
                        if debug_mode:
                            st.write("新闻列表为空或格式不正确")
            
            except requests.exceptions.RequestException as e:
                st.error(f"请求失败: {str(e)}")
            except Exception as e:
                st.error(f"处理数据时出错: {str(e)}")
                if debug_mode:
                    import traceback
                    st.write("详细错误信息:", traceback.format_exc())

# -------------------------------
# 页脚
# -------------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>CTC Smart Cryptocurrency Recommendation Assistant © 2023</p>", unsafe_allow_html=True)
