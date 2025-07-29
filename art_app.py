import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mandala Art Creator", layout="centered")

# Step 1: API key input
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

if not st.session_state["api_key"]:
    st.title("🎨 Mandala Art Creator")
    st.markdown("Enter your OpenAI API key to get started.")
    api_key_input = st.text_input("🔐 OpenAI API Key", type="password")
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.rerun()
    st.stop()

# Instantiate OpenAI client
client = OpenAI(api_key=st.session_state["api_key"])

# Step 2: UI
st.title("🎨 Mandala Art Creator")
st.markdown("Enter a single inspirational word and we’ll create a stunning mandala based on it.")

user_word = st.text_input("✨ Your inspiration word:", max_chars=50)

# Step 3: Generate
if st.button("Generate Mandala") and user_word:
    with st.spinner("🎨 Generating your mandala..."):

        # Step 3.1: Generate prompt
        try:
            chat_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a creative prompt generator. Given a word, respond ONLY with a vivid prompt "
                            "to generate a DALL·E image of a mandala inspired by that word. Do not explain anything."
                        )
                    },
                    {"role": "user", "content": user_word.strip()}
                ],
                temperature=0.8,
                max_tokens=100
            )
            refined_prompt = chat_response.choices[0].message.content.strip()

        except Exception as e:
            st.error("❌ Failed to generate prompt.")
            st.exception(e)
            st.stop()

        # Step 3.2: Generate image
        try:
            image_response = client.images.generate(
                prompt=refined_prompt,
                n=1,
                size="1024x1024",
                model="dall-e-2"  # You can try "dall-e-3" if available on your plan
            )
            image_url = image_response.data[0].url
            st.image(image_url, caption=f"🧘 Mandala inspired by '{user_word}'", use_column_width=True)

        except Exception as e:
            st.error("❌ Failed to generate image.")
            st.exception(e)
