import streamlit as st
import datetime
import requests

# 设置页面标题
st.title("🚀 CTC Smart Cryptocurrency Recommendation Assistant")
st.markdown("---")

# 显示当前时间
st.write("Sydney:", datetime.datetime.now())

# 创建一个输入框
token_symbol = st.text_input("Enter the cryptocurrency code (eg. BTC, ETH):", "BTC")

# 创建一个按钮
if st.button("开始分析"):
    with st.spinner('AI正在努力分析中...'):
        
        n8n_webhook_url = "https://ct012.app.n8n.cloud/webhook-test/d0c76d63-0bd0-4f67-906b-4aa02157eb2a"
        
        payload = {
            "token": token_symbol
        }
        
        try:
            # 添加超时参数，防止请求无限期挂起
            response = requests.post(n8n_webhook_url, json=payload, timeout=10)
            
            # 打印响应状态和内容，用于调试
            st.write(f"状态码: {response.status_code}")
            st.write(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    st.success("分析完成！")
                    st.write(f"n8n 回复: {data.get('message', '无消息')}")
                    st.write(f"收到的代币: {data.get('received_token', '无代币信息')}")
                except ValueError:
                    st.error("n8n 返回的数据不是有效的 JSON 格式")
            else:
                st.error(f"n8n 返回错误，状态码: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("请求超时，n8n 没有在预期时间内响应")
        except requests.exceptions.ConnectionError:
            st.error("无法连接到 n8n 服务器")
        except Exception as e:
            st.error(f"发生未知错误: {str(e)}")
