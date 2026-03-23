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
- 表記ゆれや曖昧な質問で情報にたどり着けない

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
- **先進的な検索パイプライン**: **Multi-Query**（多角的なクエリ生成）と **HyDE**（仮説回答生成）による高い検索ヒット率
- **AIによる再ランキング（Rerank）**: 会話履歴とファイル名を考慮し、検索結果から最適な回答根拠を厳選
- **全体把握（Summary Indexing）**: 文書全体の要約を保持し、広範な質問にも対応
- **出典引用（Citations）**: 回答の文末に根拠資料の番号（例: [1]）を表示し、該当箇所をシームレスに確認可能

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

- **ハイブリッド検索 & Rerank**: ベクトル検索で候補抽出後、LLMで再ランキングし精度向上
- **文脈依存のクエリ拡張**: 会話履歴から「それ」や「共通点」といった代名詞の意味を解釈し、検索に適したクエリへ自動展開
- **情報の信頼性担保**: AIに引用元を明示させるプロンプトエンジニアリングにより、ハルシネーション（嘘の回答）を抑制
- **マルチソース対応**: 複数ファイル・複数形式を横断的に処理

---

## 📂 学習の軌跡

このプロジェクトはRAGの基礎から応用まで段階的に実装・進化させた学習プロジェクトでもあります。各プロトタイプは `history/` フォルダに格納されており、ルートの `app.py` がその最終版です。

### 🏗️ 発展のプロセス

1. **`history/01_simple_rag.py`**: 基礎的なRAGの仕組み（単一テキストからの回答生成）
2. **`history/02_embedding_rag.py`**: Embeddingを用いたベクトル検索による精度向上
3. **`history/03_topk_rag.py`**: Top-K検索の導入による関連チャンクの取得精度向上
4. **`history/04_streamlit_rag.py`**: Streamlitによる対話型Web UIの実装
5. **`history/05_pdf_rag.py`**: PyMuPDFを用いたPDF文書の解析対応
6. **`history/06_multi_format_rag.py`**: PowerPoint（.pptx）形式への対応拡大
7. **`history/07_summary_and_refine_rag.py`**: Word (.docx) 形式への対応拡大と資料ごとの全体要約の導入、会話履歴を考慮したクエリの再構成の導入
8. **`history/08_multiquery_hyde_rag.py`**: Multi-QueryとHyDEによる検索精度の向上
9. **`history/09_advanced_rerank_rag.py`**: LLMによるRerankの導入

### 🏆 最終形態（ルートディレクトリ）

- **`app.py`**: 本プロジェクトのメインアプリ。これまでの全機能に加え、以下の機能を統合しています。
  - **出典表示 (Citations)** : 各回答に根拠となる出典の番号を明示するように変更。ハルシネーション防止にも

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

また、 `.streamlit/` 内の `secrets.toml.example` を参考に、 `.streamlit/` 内に `secrets.toml` ファイルを作成し、Gemini APIキーを設定してください。

```toml
GOOGLE_API_KEY = "あなたのAPIキー"
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