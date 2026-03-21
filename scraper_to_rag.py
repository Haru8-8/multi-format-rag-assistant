import os
import requests
from bs4 import BeautifulSoup
from google import genai
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# --- 設定 ---
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
# 今回はITニュースサイト「Publickey」のトップページを対象にします
NEWS_URL = "https://www.publickey1.jp/"

# --- Step 1: スクレイピング関数 ---
def scrape_latest_news():
    print(f"🌐 {NEWS_URL} から最新ニュースを取得中...")
    try:
        response = requests.get(NEWS_URL, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # 記事のタイトルと概要が含まれる要素を抽出（サイトの構造に合わせます）
        # ※サイト構造が変わるとここを修正する必要があります
        items = soup.select('div.newentries ul li.clearfix a')

        for entry in items:
            title = entry.get_text(strip=True)
            if title and len(title) > 5: # 短すぎる行は除外
                articles.append(title)
        
        # 上位15件程度に絞る（多すぎるとEmbeddingの時間がかかります）
        unique_articles = list(dict.fromkeys(articles))[:15]
        return unique_articles
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []

# --- Step 2: Embedding関数 ---
def get_embedding(text, task_type):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={'task_type': task_type}
    )
    return response.embeddings[0].values

# --- メイン処理 ---
def run_news_rag():
    # ニュースの取得
    raw_docs = scrape_latest_news()
    if not raw_docs:
        print("記事が取得できませんでした。")
        return

    print(f"📑 {len(raw_docs)} 件のテキストをベクトル化しています...")
    documents = raw_docs
    doc_embeddings = [get_embedding(doc, 'RETRIEVAL_DOCUMENT') for doc in documents]

    while True:
        user_query = input("\n最新ニュースについて聞いてください (終了は 'q'): ")
        if user_query.lower() == 'q': break
        
        # 検索
        query_emb = get_embedding(user_query, 'RETRIEVAL_QUERY')
        similarities = [np.dot(query_emb, d_emb) for d_emb in doc_embeddings]
        
        # Top-3を取得
        k = min(3, len(documents))
        top_indices = np.argsort(similarities)[-k:][::-1]
        retrieved_contexts = [documents[i] for i in top_indices]

        # Geminiによる回答生成
        context_text = "\n".join(retrieved_contexts)
        prompt = f"""
        あなたは最新ITニュースに詳しいアシスタントです。
        以下の「取得した最新ニュース」に基づいて、ユーザーの質問に答えてください。
        
        【取得した最新ニュース】
        {context_text}
        
        【ユーザーの質問】
        {user_query}
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        print("\n--- 💡 AIの回答 ---")
        print(response.text)

if __name__ == "__main__":
    run_news_rag()