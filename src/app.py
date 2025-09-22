import streamlit as st
import datetime
import requests
import json
from requests.auth import HTTPBasicAuth

import streamlit as st
import datetime
import requests
import json
from requests.auth import HTTPBasicAuth

# 设置页面标题和布局
st.set_page_config(page_title="CTC Cryptocurrency Assistant", layout="wide")

# 自定义CSS样式
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
    .news-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        border-left: 4px solid #1E90FF;
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

# 页面标题
st.markdown('<h1 class="main-header">🚀 CTC Smart Cryptocurrency Recommendation Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# 创建两列布局
col1, col2 = st.columns([1, 2])

# Cryptopanic API密钥
CRYPTOPANIC_API_KEY = "94175c508338f6594ebec52cbe031069b242413f"

# 获取加密货币新闻的函数
def get_crypto_news(currency="BTC", limit=5):
    """从Cryptopanic获取加密货币新闻"""
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&currencies={currency}&kind=news"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            news_data = response.json()
            return news_data.get('results', [])[:limit]
        else:
            st.error(f"获取新闻失败，状态码: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"获取新闻时出错: {str(e)}")
        return []

# 显示新闻的函数
def display_news(news_items):
    """在UI中显示新闻"""
    if not news_items:
        st.info("暂无相关新闻")
        return
    
    st.subheader("📰 最新加密货币新闻")
    
    for i, news in enumerate(news_items):
        # 创建新闻卡片
        st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
        
        # 新闻标题和链接
        st.markdown(f"### [{news.get('title', '无标题')}]({news.get('url', '#')})")
        
        # 新闻来源和时间
        col1, col2 = st.columns([3, 1])
        with col1:
            if news.get('source'):
                st.caption(f"来源: {news['source'].get('title', '未知')}")
        with col2:
            if news.get('published_at'):
                # 转换时间格式
                published_time = datetime.datetime.strptime(
                    news['published_at'], "%Y-%m-%dT%H:%M:%SZ"
                )
                st.caption(f"发布时间: {published_time.strftime('%Y-%m-%d %H:%M')}")
        
        # 新闻预览
        if news.get('preview'):
            st.write(news['preview'])
        
        st.markdown('</div>', unsafe_allow_html=True)

with col1:
    # 显示当前时间
    st.write("Sydney:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # 创建一个输入框
    token_symbol = st.text_input("Enter the cryptocurrency code (eg. BTC, ETH):", "BTC").upper()
    
    # 添加调试模式开关
    debug_mode = st.checkbox("启用调试模式", value=False)
    
    # 创建一个按钮
    analyze_btn = st.button("开始分析", type="primary")
    
    # 添加新闻刷新按钮
    news_btn = st.button("刷新新闻", type="secondary")

with col2:
    # 占位区域用于显示结果
    result_placeholder = st.empty()

# 处理新闻刷新按钮
if news_btn:
    with st.spinner('正在获取最新新闻...'):
        news_items = get_crypto_news(token_symbol)
        display_news(news_items)

# 处理分析按钮点击事件
if analyze_btn:
    with st.spinner('AI正在努力分析中...'):
        n8n_webhook_url = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
        
        payload = {
            "token": token_symbol
        }
        
        # 添加 Basic Auth 认证信息
        auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')
        
        try:
            response = requests.post(n8n_webhook_url, json=payload, auth=auth, timeout=10)
            
            # 显示状态码
            st.write(f"状态码: {response.status_code}")
            
            if debug_mode:
                st.markdown("### 调试信息")
                st.write("请求URL:", n8n_webhook_url)
                st.write("请求负载:", payload)
                st.write("响应内容:", response.text)
            
            if response.status_code == 200:
                try:
                    # 解析响应数据
                    response_data = response.json()
                    
                    if debug_mode:
                        st.write("解析后的JSON:", response_data)
                    
                    # 检查返回的数据结构
                    if isinstance(response_data, list):
                        # 处理列表格式的响应
                        if len(response_data) > 0:
                            data = response_data[0]
                            
                            # 检查是否有json字段
                            if 'json' in data:
                                data = data['json']
                            else:
                                data = data  # 直接使用第一个元素
                        else:
                            st.error("返回的列表为空")
                            data = {}
                    else:
                        # 如果不是列表，直接使用
                        data = response_data
                    
                    # 显示处理后的数据
                    if debug_mode:
                        st.write("处理后的数据:", data)
                    
                    # 检查是否有错误信息
                    if data.get('error'):
                        st.error(f"错误: {data.get('message', '未知错误')}")
                    else:
                        with result_placeholder.container():
                            st.success("分析完成！")
                            
                            # 显示消息
                            if 'message' in data:
                                st.write(f"**状态:** {data.get('message')}")
                            
                            # 显示代币信息
                            token_name = data.get('token', token_symbol)
                            st.write(f"**代币:** {token_name}")
                            
                            # 显示价格信息
                            price = data.get('price')
                            change_24h = data.get('change_24h', '0%')
                            
                            if price is not None:
                                # 确定价格变化样式
                                try:
                                    change_value = float(change_24h.strip('%'))
                                    change_style = "positive-change" if change_value >= 0 else "negative-change"
                                    
                                    # 创建指标卡
                                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                                    st.metric(
                                        label=f"{token_name} 价格",
                                        value=f"${price:,.2f}",
                                        delta=f"{change_24h}"
                                    )
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # 添加价格变化解释
                                    if change_value >= 0:
                                        st.info(f"过去24小时内，{token_name}价格上涨了{change_24h}")
                                    else:
                                        st.warning(f"过去24小时内，{token_name}价格下跌了{change_24h.replace('-', '')}")
                                except ValueError:
                                    st.metric(
                                        label=f"{token_name} 价格",
                                        value=f"${price:,.2f}",
                                        delta=f"{change_24h}"
                                    )
                            else:
                                st.error("无法获取价格信息")
                                if debug_mode:
                                    st.write("可用数据键:", list(data.keys()))
                        
                except ValueError as e:
                    st.error("n8n 返回的数据不是有效的 JSON 格式")
                    st.code(response.text, language="json")
            else:
                st.error(f"n8n 返回错误，状态码: {response.status_code}")
                st.write(f"错误详情: {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("请求超时，n8n 没有在预期时间内响应")
        except requests.exceptions.ConnectionError:
            st.error("无法连接到 n8n 服务器")
        except Exception as e:
            st.error(f"发生未知错误: {str(e)}")
    
    # 分析完成后自动获取相关新闻
    with st.spinner('正在获取相关新闻...'):
        news_items = get_crypto_news(token_symbol)
        display_news(news_items)


# 添加使用说明
with st.expander("使用说明"):
    st.markdown("""
    1. 在输入框中输入加密货币代码（如BTC、ETH）
    2. 点击"开始分析"按钮获取价格信息
    3. 点击"刷新新闻"按钮获取最新相关新闻
    4. 系统将通过n8n工作流从CoinGecko API获取最新价格信息
    5. 新闻来自Cryptopanic API，提供最新的加密货币动态
    
    **支持的加密货币:** BTC, ETH, 以及其他CoinGecko API支持的代币
    
    **调试模式:** 启用后可以查看详细的请求和响应信息，有助于排查问题
    """)

# 添加页脚
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>CTC Smart Cryptocurrency Recommendation Assistant © 2023 | 新闻数据由Cryptopanic提供</p>", unsafe_allow_html=True)
# 设置页面标题和布局
st.set_page_config(page_title="CTC Cryptocurrency Assistant", layout="wide")

# 自定义CSS样式
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

# 页面标题
st.markdown('<h1 class="main-header">🚀 CTC Smart Cryptocurrency Recommendation Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# 创建两列布局
col1, col2 = st.columns([1, 2])

with col1:
    # 显示当前时间
    st.write("Sydney:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # 创建一个输入框
    token_symbol = st.text_input("Enter the cryptocurrency code (eg. BTC, ETH):", "BTC").upper()
    
    # 添加调试模式开关
    debug_mode = st.checkbox("启用调试模式", value=True)
    
    # 创建一个按钮
    analyze_btn = st.button("开始分析", type="primary")

with col2:
    # 占位区域用于显示结果
    result_placeholder = st.empty()

# 处理按钮点击事件
if analyze_btn:
    with st.spinner('AI正在努力分析中...'):
        n8n_webhook_url = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
        
        payload = {
            "token": token_symbol
        }
        
        # 添加 Basic Auth 认证信息
        auth = HTTPBasicAuth('yile.cai1222@gmail.com', 'Ax112211')
        
        try:
            response = requests.post(n8n_webhook_url, json=payload, auth=auth, timeout=10)
            
            # 显示状态码
            st.write(f"状态码: {response.status_code}")
            
            if debug_mode:
                st.markdown("### 调试信息")
                st.write("请求URL:", n8n_webhook_url)
                st.write("请求负载:", payload)
                st.write("响应内容:", response.text)
            
            if response.status_code == 200:
                try:
                    # 解析响应数据
                    response_data = response.json()
                    
                    if debug_mode:
                        st.write("解析后的JSON:", response_data)
                    
                    # 检查返回的数据结构
                    if isinstance(response_data, list):
                        # 处理列表格式的响应
                        if len(response_data) > 0:
                            data = response_data[0]
                            
                            # 检查是否有json字段
                            if 'json' in data:
                                data = data['json']
                            else:
                                data = data  # 直接使用第一个元素
                        else:
                            st.error("返回的列表为空")
                            data = {}
                    else:
                        # 如果不是列表，直接使用
                        data = response_data
                    
                    # 显示处理后的数据
                    if debug_mode:
                        st.write("处理后的数据:", data)
                    
                    # 检查是否有错误信息
                    if data.get('error'):
                        st.error(f"错误: {data.get('message', '未知错误')}")
                    else:
                        with result_placeholder.container():
                            st.success("分析完成！")
                            
                            # 显示消息
                            if 'message' in data:
                                st.write(f"**状态:** {data.get('message')}")
                            
                            # 显示代币信息
                            token_name = data.get('token', token_symbol)
                            st.write(f"**代币:** {token_name}")
                            
                            # 显示价格信息
                            price = data.get('price')
                            change_24h = data.get('change_24h', '0%')
                            
                            if price is not None:
                                # 确定价格变化样式
                                change_value = float(change_24h.strip('%'))
                                change_style = "positive-change" if change_value >= 0 else "negative-change"
                                
                                # 创建指标卡
                                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                                st.metric(
                                    label=f"{token_name} 价格",
                                    value=f"${price:,.2f}",
                                    delta=f"{change_24h}"
                                )
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # 添加价格变化解释
                                if change_value >= 0:
                                    st.info(f"过去24小时内，{token_name}价格上涨了{change_24h}")
                                else:
                                    st.warning(f"过去24小时内，{token_name}价格下跌了{change_24h.replace('-', '')}")
                            else:
                                st.error("无法获取价格信息")
                                if debug_mode:
                                    st.write("可用数据键:", list(data.keys()))
                        
                except ValueError as e:
                    st.error("n8n 返回的数据不是有效的 JSON 格式")
                    st.code(response.text, language="json")
            else:
                st.error(f"n8n 返回错误，状态码: {response.status_code}")
                st.write(f"错误详情: {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("请求超时，n8n 没有在预期时间内响应")
        except requests.exceptions.ConnectionError:
            st.error("无法连接到 n8n 服务器")
        except Exception as e:
            st.error(f"发生未知错误: {str(e)}")

# 添加使用说明
with st.expander("使用说明"):
    st.markdown("""
    1. 在输入框中输入加密货币代码（如BTC、ETH）
    2. 点击"开始分析"按钮
    3. 系统将通过n8n工作流从CoinGecko API获取最新价格信息
    4. 结果将显示在右侧面板中
    
    **支持的加密货币:** BTC, ETH, 以及其他CoinGecko API支持的代币
    
    **调试模式:** 启用后可以查看详细的请求和响应信息，有助于排查问题
    """)

# 添加页脚
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>CTC Smart Cryptocurrency Recommendation Assistant © 2023</p>", unsafe_allow_html=True)
