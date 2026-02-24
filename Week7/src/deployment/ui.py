import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Enterprise Multimodal RAG",
    layout="centered",
)

st.title("Enterprise Multimodal RAG Assistant")

mode = st.radio(
    "Select Mode",
    ["Text RAG", "Image RAG", "SQL RAG"],
    horizontal=True,
)

st.divider()

# TEXT RAG

if mode == "Text RAG":

    question = st.text_area("Ask something")

    if st.button("Ask"):
        if not question.strip():
            st.warning("Enter a question")
        else:
            with st.spinner("Thinking..."):
                resp = requests.post(
                    f"{API_BASE}/ask",
                    json={"question": question},
                    timeout=600,
                )

                data = resp.json()

                st.success("Answer")
                st.write(data.get("answer", ""))

                if data.get("image"):
                    st.image(data["image"], caption="Retrieved Image")

                st.caption(
                    f"Confidence: {data.get('confidence')} | "
                    f"Hallucination: {data.get('hallucination')}"
                )

# IMAGE RAG

elif mode == "Image RAG":

    question = st.text_area("Optional question about image")
    image = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

    if st.button("Ask with Image"):

        if not image:
            st.warning("Upload an image first")
        else:
            with st.spinner("Processing image..."):

                files = {
                    "file": (
                        image.name,
                        image.getvalue(),
                        image.type,
                    )
                }

                resp = requests.post(
                    f"{API_BASE}/ask-image",
                    files=files,
                    timeout=1000,
                )

                result = resp.json()

                st.success("Answer")
                st.write(result.get("answer", ""))

                if result.get("image"):
                    st.image(result["image"], caption="Top Retrieved Image")

                st.caption(
                    f"Confidence: {result.get('confidence')} | "
                    f"Hallucination: {result.get('hallucination')}"
                )

# SQL RAG

else:

    question = st.text_area("Ask database question")

    if st.button("Run SQL Query"):

        with st.spinner("Running SQL..."):

            resp = requests.post(
                f"{API_BASE}/ask-sql",
                json={"question": question},
                timeout=600,
            )

        if resp.status_code == 200:
            data = resp.json()

            st.subheader("Answer")
            st.write(data.get("answer"))

            st.caption(
                f"Confidence: {data.get('confidence')} | "
                f"Hallucination: {data.get('hallucination')}"
            )
        else:
            st.error(resp.text)