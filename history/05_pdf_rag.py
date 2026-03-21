import streamlit as st
from google import genai
import numpy as np
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import time

load_dotenv()

# --- 設定 ---
st.set_page_config(page_title="ドキュメントAIアシスタント", layout="wide")
st.title("📄 資料読み込み型 AIチャット")

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- 関数定義 ---

def get_emb(text):
    res = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={'task_type': 'RETRIEVAL_DOCUMENT'}
    )
    return res.embeddings[0].values

def extract_and_chunk(pdf_file, chunk_size=600, overlap=100):
    """PDFからテキストを抽出し、オーバーラップを持たせて分割する"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i : i + chunk_size]
        if len(chunk) > 20: # 短すぎるゴミデータを除外
            chunks.append(chunk)
    return chunks

# --- サイドバー：ファイルアップロード ---
with st.sidebar:
    st.header("設定")
    uploaded_file = st.file_uploader("PDFファイルをアップロード", type="pdf")
    
    if uploaded_file:
        if "file_id" not in st.session_state or st.session_state.file_id != uploaded_file.name:
            with st.spinner("資料を解析・ベクトル化中..."):
                # 1. テキスト抽出 & 分割
                chunks = extract_and_chunk(uploaded_file)
                # 2. 全チャンクのベクトル化
                embeddings = []
                for c in chunks:
                    try:
                        embeddings.append(get_emb(c))
                        # 1回のリクエストごとに0.5秒〜1秒待機
                        time.sleep(1.0) 
                    except Exception as e:
                        st.error(f"APIエラーが発生しました: {e}")
                        break # エラーが出たら停止
                
                # セッションに保存
                st.session_state.chunks = chunks
                st.session_state.embs = embeddings
                st.session_state.file_id = uploaded_file.name
                st.success("解析完了！")

# --- メインチャット画面 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("資料の内容について質問してください"):
    if "chunks" not in st.session_state:
        st.warning("先にPDFファイルをアップロードしてください。")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 1. 質問のベクトル化
        q_emb = get_emb(prompt)
        
        # 2. 類似度計算 (Top-3)
        sims = [np.dot(q_emb, d_emb) for d_emb in st.session_state.embs]
        top_idx = np.argsort(sims)[-3:][::-1]
        relevant_chunks = [st.session_state.chunks[i] for i in top_idx]
        
        # 3. 回答生成
        context = "\n---\n".join(relevant_chunks)
        final_prompt = f"""以下の資料の一部を参考にして、質問に答えてください。
        資料に答えがない場合は、無理に答えず「資料には記載がありません」と伝えてください。

        【資料の内容】
        {context}

        【質問】
        {prompt}
        """
        
        response = client.models.generate_content(model="gemini-2.5-flash", contents=final_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            with st.expander("参照した箇所を確認"):
                for c in relevant_chunks:
                    st.info(c)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})