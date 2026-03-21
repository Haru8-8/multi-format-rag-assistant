import os
from google import genai
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# 1. クライアントの初期化 (環境変数または直接入力)
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 2. 知識ベース（少し情報を増やしました）
documents = [
    "株式会社テックサンプルの営業時間は平日10:00〜18:00です。",
    "定休日は土日祝日および年末年始となります。",
    "サポート窓口はメールのみで、返信には最大2営業日かかります。",
    "2024年の夏季休暇は8月10日から8月15日までです。",
    "当社の所在地は東京都渋谷区のテックビル4階です。",
    "代表取締役は山田太郎、設立は2015年4月1日です。",
    "最寄り駅は渋谷駅で、徒歩5分の場所にあります。"
]

def get_embedding(text, task_type):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={'task_type': task_type}
    )
    return response.embeddings[0].values

# 知識ベースの事前ベクトル化
print("知識ベースをインデックス化しています...")
doc_embeddings = [get_embedding(doc, 'RETRIEVAL_DOCUMENT') for doc in documents]

def top_k_rag_chat(k=3):
    user_query = input("\n質問を入力してください: ")
    query_embedding = get_embedding(user_query, 'RETRIEVAL_QUERY')
    
    # 3. 全ドキュメントとの類似度を計算
    similarities = [np.dot(query_embedding, doc_emb) for doc_emb in doc_embeddings]
    
    # 4. 【Top-K抽出】類似度が高い順にインデックスを並び替え、上位k件を取得
    top_indices = np.argsort(similarities)[-k:][::-1] 
    
    retrieved_contexts = [documents[i] for i in top_indices]
    
    print(f"\n--- 検索された上位{k}件の知識 ---")
    for i, context in enumerate(retrieved_contexts, 1):
        print(f"{i}: {context}")

    # 5. 複数の知識を統合してプロンプトを作成
    context_text = "\n".join(retrieved_contexts)
    prompt = f"""
    以下の「提供された複数の知識」を参考にして、ユーザーの質問に正確に答えてください。
    
    【提供された複数の知識】
    {context_text}
    
    【ユーザーの質問】
    {user_query}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    print("\n--- AIの回答 ---")
    print(response.text)

if __name__ == "__main__":
    top_k_rag_chat(k=3) # 上位3件を使用