
import streamlit as st
import whisper
import os
import tempfile

st.set_page_config(page_title="逐字神器", layout="centered")
st.title("📣 逐字神器｜AI逐字稿 + 話術整理工具")

st.markdown("請上傳音檔（支援 mp3、m4a、wav），系統將：\n1️⃣ 自動辨識語音為逐字稿\n2️⃣ 自動優化話術內容\n3️⃣ 提供逐字稿與話術稿下載")

uploaded_file = st.file_uploader("🔺 上傳錄音檔：", type=["mp3", "m4a", "wav"])
language = st.selectbox("🗣️ 語音語言：", ["中文 (Chinese)", "英文 (English)"])

if uploaded_file is not None:
    with st.spinner("🤖 AI 正在轉換中，請稍候..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        model = whisper.load_model("base")
        result = model.transcribe(tmp_path, language="chinese" if language.startswith("中") else "english")
        transcript = result["text"]

        optimized = transcript.replace("我跟你說", "我這邊說明") \
                                .replace("就是", "也就是說") \
                                .replace("你知道嗎", "讓我補充一下")

        st.subheader("📝 原始逐字稿")
        st.text_area("以下是辨識出來的逐字稿內容：", transcript, height=250)

        st.subheader("🪄 話術優化建議")
        st.text_area("以下是經過 AI 整理後的話術內容：", optimized, height=250)

        st.download_button("📥 下載逐字稿.txt", data=transcript, file_name="逐字稿.txt")
        st.download_button("📥 下載話術優化稿.txt", data=optimized, file_name="話術稿.txt")

        os.remove(tmp_path)
