import streamlit as st
from google import genai
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

# --- ページ設定 ---
st.set_page_config(page_title="最新ITニュースRAGチャット", layout="centered")
st.title("🌐 最新ITニュース AIアシスタント")

# --- 初期設定 ---
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# ニュース取得 (キャッシュを利用して何度もサイトを叩かないようにします)
@st.cache_data
def get_latest_news():
    url = "https://www.publickey1.jp/"
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('div.newentries ul li.clearfix a')
    articles = [a_text for a in items if len(a_text :=a.get_text(strip=True)) > 5]
    return list(dict.fromkeys(articles))[:15]

def get_emb(text, task_type):
    res = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={'task_type': task_type}
    )
    return res.embeddings[0].values

# --- アプリ本体 ---
news_list = get_latest_news()

if "doc_embs" not in st.session_state:
    st.info("ニュースをインデックス化しています...")
    st.session_state.doc_embs = [get_emb(doc, 'RETRIEVAL_DOCUMENT') for doc in news_list]
    st.success("準備完了！")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 履歴の表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ユーザー入力
if prompt := st.chat_input("最新のIT動向について聞いてください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAGロジック
    q_emb = get_emb(prompt, 'RETRIEVAL_QUERY')
    sims = [np.dot(q_emb, d_emb) for d_emb in st.session_state.doc_embs]
    top_idx = np.argsort(sims)[-3:][::-1]
    contexts = [news_list[i] for i in top_idx]
    
    # 回答生成
    full_prompt = f"以下のニュースを参考に答えて:\n{chr(10).join(contexts)}\n質問: {prompt}"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=full_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.caption(f"参照したニュース: {', '.join(contexts)}")
    st.session_state.messages.append({"role": "assistant", "content": response.text})