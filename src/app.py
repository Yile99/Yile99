import streamlit as st
import datetime
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import html  # 用于解码HTML实体

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
.sentiment-positive {
    color: green;
    font-weight: bold;
}
.sentiment-negative {
    color: red;
    font-weight: bold;
}
.sentiment-important {
    color: orange;
    font-weight: bold;
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
                if isinstance(data, list):
                    raw_news_data = None
                    processed_news_data = None
                    
                    # 分离原始新闻数据和处理后的新闻数据
                    for item in data:
                        if isinstance(item, dict):
                            item_data = item.get("json", item)
                            
                            # 查找原始新闻数据（包含results字段）
                            if isinstance(item_data, dict) and "results" in item_data:
                                raw_news_data = item_data.get("results", [])
                            
                            # 查找处理后的新闻数据（包含title和votes字段）
                            elif isinstance(item_data, dict) and "title" in item_data and "votes" in item_data:
                                processed_news_data = item_data
                            elif isinstance(item_data, list) and len(item_data) > 0:
                                first_item = item_data[0] if isinstance(item_data[0], dict) else {}
                                if "title" in first_item and "votes" in first_item:
                                    processed_news_data = item_data
                    
                    # 合并新闻数据
                    if raw_news_data and processed_news_data:
                        # 确保processed_news_data是列表
                        if not isinstance(processed_news_data, list):
                            processed_news_data = [processed_news_data]
                        
                        # 创建标题到处理数据的映射
                        processed_news_map = {}
                        for p_news in processed_news_data:
                            if isinstance(p_news, dict):
                                title = p_news.get("title", "")
                                if title:
                                    processed_news_map[title] = p_news
                        
                        # 合并数据
                        for r_news in raw_news_data[:5]:  # 只取前5条
                            if isinstance(r_news, dict):
                                title = r_news.get("title", "")
                                processed_info = processed_news_map.get(title, {})
                                
                                # 合并两个数据源
                                merged_news = {
                                    "title": title,
                                    "description": r_news.get("description", ""),
                                    "url": r_news.get("url", "#"),
                                    "published_at": r_news.get("published_at", "未知时间"),
                                    "source": r_news.get("source", {}).get("title", "未知来源") if isinstance(r_news.get("source"), dict) else "未知来源",
                                    "kind": r_news.get("kind", "未知类型"),
                                    "votes": processed_info.get("votes", {"positive": 0, "negative": 0, "important": 0})
                                }
                                news_list.append(merged_news)
                    
                    # 如果合并失败，使用原始新闻数据
                    elif raw_news_data:
                        for r_news in raw_news_data[:5]:
                            if isinstance(r_news, dict):
                                news_list.append({
                                    "title": r_news.get("title", ""),
                                    "description": r_news.get("description", ""),
                                    "url": r_news.get("url", "#"),
                                    "published_at": r_news.get("published_at", "未知时间"),
                                    "source": r_news.get("source", {}).get("title", "未知来源") if isinstance(r_news.get("source"), dict) else "未知来源",
                                    "kind": r_news.get("kind", "未知类型"),
                                    "votes": {"positive": 0, "negative": 0, "important": 0}
                                })
                    
                    # 如果只有处理后的数据
                    elif processed_news_data:
                        if not isinstance(processed_news_data, list):
                            processed_news_data = [processed_news_data]
                        
                        for p_news in processed_news_data[:5]:
                            if isinstance(p_news, dict):
                                news_list.append({
                                    "title": p_news.get("title", ""),
                                    "description": "",
                                    "url": p_news.get("url", "#"),
                                    "published_at": p_news.get("published_at", "未知时间"),
                                    "source": p_news.get("source", "未知来源"),
                                    "kind": "未知类型",
                                    "votes": p_news.get("votes", {"positive": 0, "negative": 0, "important": 0})
                                })
                
                else:
                    # 如果是对象格式
                    price = data.get("price")
                    change_24h = data.get("change_24h", "0%")
                    message = data.get("message", "")
                    news_list = data.get("news", [])
                    if not news_list:
                        news_list = data.get("results", [])
                
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
                            st.markdown('<div class="news-card">', unsafe_allow_html=True)
                            
                            # 标题
                            title = news_item.get('title', '无标题')
                            st.markdown(f'<div class="news-title">{i+1}. {title}</div>', unsafe_allow_html=True)
                            
                            # 描述（解码HTML实体）
                            description = news_item.get('description', '')
                            if description:
                                # 解码HTML实体
                                description = html.unescape(description)
                                # 移除HTML标签
                                import re
                                description = re.sub(r'<[^>]+>', '', description)
                                st.write(f"**摘要:** {description}")
                            
                            # 来源、时间和类型
                            source = news_item.get('source', '未知来源')
                            published_at = news_item.get('published_at', '未知时间')
                            kind = news_item.get('kind', '未知类型')
                            
                            # 格式化时间
                            try:
                                if 'T' in published_at:
                                    dt = datetime.datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                                    published_at = dt.strftime("%Y-%m-%d %H:%M:%S")
                            except:
                                pass
                            
                            st.write(f"**来源:** {source} | **时间:** {published_at} | **类型:** {kind}")
                            
                            # 链接
                            url = news_item.get('url', '#')
                            if url and url != '#':
                                st.markdown(f"[阅读原文 ↗]({url})")
                            
                            # 情绪分析
                            votes = news_item.get('votes', {})
                            if votes:
                                st.write("**市场情绪分析:**")
                                
                                # 创建列来显示情绪指标
                                cols = st.columns(3)
                                
                                with cols[0]:
                                    positive = votes.get('positive', 0)
                                    st.metric("👍 积极", positive, 
                                             delta=f"+{positive}" if positive > 0 else None,
                                             delta_color="normal")
                                
                                with cols[1]:
                                    negative = votes.get('negative', 0)
                                    st.metric("👎 消极", negative,
                                             delta=f"+{negative}" if negative > 0 else None,
                                             delta_color="inverse")
                                
                                with cols[2]:
                                    important = votes.get('important', 0)
                                    st.metric("⭐ 重要度", important,
                                             delta=f"+{important}" if important > 0 else None,
                                             delta_color="off")
                            
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
