from google import genai
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

# 1. クライアントの初期化
# APIキーを直接渡すか、環境変数 GEMINI_API_KEY に設定してください
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. 知識ベース
documents = [
    "株式会社テックサンプルの営業時間は平日10:00〜18:00です。",
    "サポート窓口はメールのみで、返信には最大2営業日かかります。",
    "2024年の夏季休暇は8月10日から8月15日までです。",
    "当社の所在地は東京都渋谷区のテックビル4階です。",
    "代表取締役は山田太郎、設立は2015年4月1日です。"
]

# 3. テキストをベクトル化する関数 (最新版 API 形式)
def get_embedding(text):
    # client.models.embed_content を使用します
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            'task_type': 'RETRIEVAL_DOCUMENT',
            'title': 'Knowledge Base'
        }
    )
    # response.embeddings[0].values に数値リストが入っています
    return response.embeddings[0].values

# 4. 知識ベースを事前ベクトル化
print("知識ベースをベクトル化しています...")
doc_embeddings = [get_embedding(doc) for doc in documents]

def vector_rag_chat():
    user_query = input("\n質問を入力してください: ")
    
    # 5. ユーザーの質問をベクトル化 (task_typeをQUERYに変更)
    query_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=user_query,
        config={'task_type': 'RETRIEVAL_QUERY'}
    )
    query_embedding = query_response.embeddings[0].values
    
    # 6. コサイン類似度で最も近い文章を特定
    similarities = [np.dot(query_embedding, doc_emb) for doc_emb in doc_embeddings]
    best_doc_index = np.argmax(similarities)
    
    retrieved_knowledge = documents[best_doc_index]
    print(f"--- 検索された知識: {retrieved_knowledge} ---")

    # 7. Gemini-2.0-Flash (最新) などで回答生成
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        以下の「提供された知識」のみに基づいて回答してください。
        
        【提供された知識】
        {retrieved_knowledge}
        
        【ユーザーの質問】
        {user_query}
        """
    )
    
    print("\n--- AIの回答 ---")
    print(response.text)

if __name__ == "__main__":
    vector_rag_chat()