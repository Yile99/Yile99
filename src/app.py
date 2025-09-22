import streamlit as st
import datetime  # 需要导入datetime模块
import requests

# 设置页面标题
st.title("🚀 CTC Smart Cryptocurrency Recommendation Assistant")
st.markdown("---")  # 修正了拼写错误

# 显示当前时间（一个简单的动态功能）
st.write("Sydney:", datetime.datetime.now())  # 修正了函数调用

# 创建一个输入框
token_symbol = st.text_input("Enter the cryptocurrency code (eg. BTC, ETH):", "BTC")  # 修正了引号和文本

# 创建一个按钮
if st.button("开始分析"):
    with st.spinner('AI正在努力分析中...'):
        
        # 1. 这是你的 n8n Webhook URL - 直接从你的 n8n 界面复制过来！
        n8n_webhook_url = "https://ct012.app.n8n.cloud/webhook/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
        
        # 2. 准备要发送的数据
        payload = {
            "token": token_symbol  # 这个 token_symbol 是用户输入的代币符号
        }
        
        try:
            # 3. 向 n8n 发送 POST 请求（“按门铃”）
            response = requests.post(n8n_webhook_url, json=payload)
            
            # 4. 检查请求是否成功
            if response.status_code == 200:
                data = response.json()  # 获取 n8n 返回的 JSON 数据
                st.success("分析完成！")
                st.write(f"n8n 回复: {data['message']}")
                st.write(f"收到的代币: {data['received_token']}")
            else:
                st.error(f"n8n 似乎出了问题，错误代码: {response.status_code}")
                
        except Exception as e:
            st.error(f"连接失败: {e}")
