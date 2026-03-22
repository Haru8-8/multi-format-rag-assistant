# 業務文書検索AI（RAG × マルチフォーマット × チャット）

PDF・PowerPoint・Wordなどの社内文書を横断的に検索し、AIが文脈を理解して回答するRAGアシスタントです。

👉 **社内ドキュメントの検索・ナレッジ共有・問い合わせ対応を効率化できます。**

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![RAG](https://img.shields.io/badge/Technology-RAG-blue)
![Gemini](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-orange?logo=google-gemini)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 解決できる課題

- 社内ドキュメントの検索に時間がかかる
- PDFや資料が分散しており活用しづらい
- 必要な情報を見つけるのに全文を読む必要がある
- 社内ナレッジが属人化している

---

## 想定ユースケース

- 社内ナレッジ検索システム
- マニュアル・仕様書のQAボット
- 営業資料・提案書の横断検索
- カスタマーサポートの問い合わせ支援

---

## 主な機能

- **マルチフォーマット対応**: PDF / PPTX / DOCX から自動でテキスト抽出
- **RAGによる高精度回答**: 関連チャンクを検索し、文脈に基づいた回答を生成
- **コンテキスト理解（Query Refinement）**: 会話履歴をもとに曖昧な質問を補完・再構成
- **全体把握（Summary Indexing）**: 文書全体の要約を保持し、広範な質問にも対応
- **出典表示**: 回答に使用した資料と該当箇所をStreamlit expanderで確認可能

---

## デモ

### アプリ画面
![アプリ画面](docs/screenshots/app_screenshot.png)

### デモURL

Streamlit Cloud でインタラクティブデモを公開しています。  
→ **https://multi-format-rag-assistant-stpsybemmcd4fxjizgc6rg.streamlit.app/**

> **API利用制限について**  
> 本アプリはGemini APIの無料枠を利用しているため、リクエストが集中した場合や時間あたりの制限（RPM/TPM）に達した場合、一時的に回答が生成されないことがあります。その場合は、しばらく時間を置いてから再度お試しください。

---

## 技術スタック

| 分類 | 技術 |
|------|------|
| 言語モデル | Gemini 2.5 Flash / 2.5 Flash Lite |
| Embedding | gemini-embedding-001 |
| フレームワーク | Streamlit |
| 文書解析 | PyMuPDF・python-pptx・python-docx |
| その他 | NumPy・BeautifulSoup・python-dotenv |

---

## 技術的な工夫

- **ハイブリッド検索構造**: チャンク検索 + 文書全体要約を組み合わせ、局所・全体の両方に対応
- **クエリ再構成（Query Refinement）**: 会話履歴から検索クエリを動的生成し、検索精度を向上
- **マルチソース対応**: 複数ファイル・複数形式を横断的に処理

---

## 📂 学習の軌跡

このプロジェクトはRAGの基礎から応用まで段階的に実装・進化させた学習プロジェクトでもあります。各プロトタイプは `history/` フォルダに格納されており、ルートの `app.py` がその集大成です。

### 🏗️ 発展のプロセス

1. **`history/01_simple_rag.py`**: 基礎的なRAGの仕組み（単一テキストからの回答生成）
2. **`history/02_embedding_rag.py`**: Embeddingを用いたベクトル検索による精度向上
3. **`history/03_topk_rag.py`**: Top-K検索の導入による関連チャンクの取得精度向上
4. **`history/04_streamlit_rag.py`**: Streamlitによる対話型Web UIの実装
5. **`history/05_pdf_rag.py`**: PyMuPDFを用いたPDF文書の解析対応
6. **`history/06_multi_format_rag.py`**: PowerPoint（.pptx）形式への対応拡大

### 🏆 最終形態（ルートディレクトリ）

- **`app.py`**: 本プロジェクトのメインアプリ。これまでの全機能に加え、以下の高度な機能を統合しています。
  - **Word（.docx）対応**: ビジネス文書の主要3形式（PDF / PPTX / DOCX）をフルカバー
  - **Query Refinement**: 会話履歴を考慮した文脈に沿ったクエリの自動再構成
  - **Summary Indexing**: 各資料の全体要約を自動生成し、広範囲な質問にも対応

- **`scraper_to_rag.py`**: Webニュースサイトからリアルタイムに情報をスクレイピングし、RAGのナレッジベースとして活用する応用実装。最新情報を取り込んだ回答生成が可能です。

---

## 🛠️ セットアップ

### 1. ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example` を参考に `.env` ファイルを作成し、Gemini APIキーを設定してください。

```plaintext
GOOGLE_API_KEY=あなたのAPIキー
```

### 3. 実行

```bash
# メインアプリ（マルチフォーマットRAG）
streamlit run app.py

# スクレイピングRAG
streamlit run scraper_to_rag.py
```

---

## 拡張例

- 社内システムとの連携
- Slack / LINE連携
- DB・ベクトルDBへの保存
- 権限管理付きナレッジ検索

---

## 備考

👉 業務内容に応じてカスタマイズ（検索ロジック・UI・連携機能など）も可能です。

---

## ライセンス

[MIT License](LICENSE)