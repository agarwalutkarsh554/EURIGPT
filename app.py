import os
import streamlit as st
from euriai import EuriaiClient
from dotenv import load_dotenv

load_dotenv()


st.title("🧠 Euriai Text Generator with Code Support")

# Model selector
model_choice = st.selectbox("Choose Model:", ["gpt-4.1-mini", "gpt-4.1-nano","deepseek-r1-distill-llama-70b","qwen-qwq-32b"," mistral-saba-24b","llama-4-scout-17b-16e-instruct","llama-4-maverick-17b-128e-instruct","gemini-2.5-pro-exp-03-25","gemini-2.0-flash-001"])

# Prompt input
prompt = st.text_area("Enter your prompt:", "Write a Python function to reverse a string.")

# Generate button
if st.button("Generate"):
    with st.spinner("Generating response..."):
        try:
            client = EuriaiClient(api_key=os.getenv("API_KEY"), model=model_choice)

            response = client.generate_completion(
                prompt=prompt
            )

            st.success("Response:")
            response=response["choices"][0]["message"]["content"]
            # Auto format if code detected
            if "```" in response or prompt.lower().startswith("write code") or "python" in response.lower():
                # Extract language and code if inside triple backticks
                if "```" in response:
                    parts = response.split("```")
                    language = parts[1].split("\n")[0] if "\n" in parts[1] else "python"
                    code = "\n".join(parts[1].split("\n")[1:]) if "\n" in parts[1] else parts[1]
                else:
                    language = "python"
                    code = response

                st.code(code.strip(), language=language)
                st.download_button("📋 Copy Code", code.strip(), file_name="code_snippet.py")
            else:
                st.text_area("📝 Output", response.strip(), height=200)
                st.download_button("📋 Copy Text", response.strip(), file_name="response.txt")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.text(response)
