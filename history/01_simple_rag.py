from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def simple_rag_chat():
    # 1. APIの設定 (取得したAPIキーを入力してください)
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    # 2. 外部知識（カンニングペーパー）の定義
    # 本来はここをスクレイピングしたデータやPDFから読み込みます
    knowledge_base = """
    【ポートフォリオ用サンプル知識】
    - このAIは、株式会社テックサンプルの公式ガイドに基づいています。
    - 営業時間は平日10:00〜18:00です。
    - サポート窓口はメールのみで、返信には最大2営業日かかります。
    - 2024年の夏季休暇は8月10日から8月15日までです。
    """

    print("--- RAGチャットボット起動中 ---")
    user_query = input("質問を入力してください: ")

    # 3. RAG用プロンプトの作成
    # 知識(Context)と質問(Question)を組み合わせてAIに渡します
    prompt = f"""
    以下の「提供された知識」のみに基づいて回答してください。
    知識の中に答えがない場合は「分かりかねます」と答えてください。

    【提供された知識】
    {knowledge_base}

    【ユーザーの質問】
    {user_query}
    """

    # 4. 回答の生成
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    print("\n--- AIの回答 ---")
    print(response.text)

if __name__ == "__main__":
    simple_rag_chat()