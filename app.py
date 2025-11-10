import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage 
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# LLMに問い合わせる処理を関数として定義
def get_answer(llm, user_question, expert_role):
    """
    LLMから回答を取得する関数

    引数:
    - llm: 使用するLLMのインスタンス
    - user_question: ユーザーからの質問テキスト
    - expert_role: ラジオボタンで選択された専門家の役割

    戻り値:
    - LLMからの回答テキスト
    """
    
    # 専門家の役割に応じたシステムメッセージを定義
    # ここで専門家の種類と、その振る舞いを定義します
    expert_prompts = {
        "フレンドリーなチャット相手": "あなたはユーザーの親しい友人です。フレンドリーで、少しユーモアを交えながら会話してください。",
        "プロの翻訳家": "あなたはプロの翻訳家です。受け取ったテキストを、文脈を考慮して自然で正確な英語に翻訳してください。",
        "ITエンジニア": "あなたは経験豊富なITエンジニアです。専門用語も使いながら、技術的な質問に対して簡潔かつ正確に回答してください。"
    }
    
    # 選択された専門家に応じてシステムメッセージを取得（見つからない場合はデフォルトのメッセージを使用）
    system_message_content = expert_prompts.get(expert_role, "You are a helpful assistant.")

    # LLMに渡すメッセージを作成
    messages = [
        SystemMessage(content=system_message_content),
        HumanMessage(content=user_question),
    ]
    
    # LLMを実行して結果を取得
    result = llm.invoke(messages)
    return result.content
# --- 関数定義ここまで ---


# 環境変数からOpenAI APIキーを読み込む
api_key = os.getenv("OPENAI_API_KEY")

# APIキーが設定されていない場合のエラーハンドリング
if not api_key:
    st.error("OpenAI APIキーが設定されていません。.envファイルを確認してください。")
else:
    # LLMモデルを初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=api_key)

    # --- ここからが追加・変更部分 (2/3) ---
    # Webアプリの概要や操作方法を表示
    st.title("AIエキスパート チャット")
    st.markdown("""
    このアプリは、AIに様々な専門家の役割を演じさせて質問に答えてもらうチャットアプリです。

    **【操作方法】**
    1. 下のラジオボタンからAIに演じさせたい専門家を選んでください。
    2. 質問を入力してください。
    3. 「送信」ボタンを押すと、AIがその専門家として回答します。
    """)

    # 専門家選択のラジオボタン
    # ここで選択肢となる専門家をリストで定義します
    expert_options = ["フレンドリーなチャット相手", "プロの翻訳家", "ITエンジニア"]
    selected_expert = st.radio(
        "AIに演じさせる専門家を選んでください:",
        expert_options,
        horizontal=True # ラジオボタンを横並びにする
    )
    # --- UIの追加ここまで ---

    # ユーザーがテキストを入力するためのフォーム
    user_input = st.text_input("質問を入力してください:")

    # 送信ボタン
    if st.button("送信"):
        if user_input:
            with st.spinner("AIが回答を生成中です..."):
                # --- ここからが追加・変更部分 (3/3) ---
                # 先ほど定義した関数を呼び出す
                response = get_answer(llm, user_input, selected_expert)
            
            # 回答結果を画面に表示
            st.markdown("### 回答")
            st.write(response)
            # --- 関数呼び出しに変更ここまで ---
        else:
            st.warning("質問を入力してください。")