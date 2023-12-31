import streamlit as st

from financial_analyst import FinancialAssistantManager
from utils import financial_tools, INSTRUCTIONS
import os
import requests

if "message" not in st.session_state:
    st.session_state.message = []

st.set_page_config(
    page_title="Financial Analyst",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.sidebar.header("Have a look at the internal working")
st.sidebar.write("What's happeing in the background")
st.header("💰 : Financial Analyst")

fmp_analyst: FinancialAssistantManager = FinancialAssistantManager()

assistant = fmp_analyst.create_assistant(
    name="Financial Analyst",
    instructions=INSTRUCTIONS,
    tools=financial_tools,
)

thread = fmp_analyst.create_thread()

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input(
    "compare last year financial health of Microsoft and Apple focusing on their balance sheets and key financial ratios"
):
    st.session_state.message.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    try:
        fmp_analyst.add_message_to_thread(role="user", content=prompt)
    except Exception:
        st.sidebar.error(
            "Error in processing your request. Please refresh and try again later."
        )
        st.stop()

    run = fmp_analyst.run_assistant(instructions=INSTRUCTIONS)

    final_res = fmp_analyst.wait_for_completion(run=run, thread=thread)

    assistant_message_in_run = [
        message
        for message in final_res
        if message.run_id == run.id and message.role == "assistant"
    ]

    for message in assistant_message_in_run:
        role_label = "User" if message.role == "user" else "Assistant"

        for content in message.content:
            if content.type == "text":
                message_content = content.text.value
                st.session_state.message.append(
                    {"role": role_label, "content": message_content}
                )
                with st.chat_message(role_label):
                    st.markdown(message_content, unsafe_allow_html=True)

            elif content.type == "image_file":
                image_file_id = content.image_file.file_id
                image_url = f"https://api.openai.com/v1/files/{image_file_id}/content"
                headers = {
                    "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
                }

                response = requests.get(image_url, headers=headers)

                if response.status_code == 200:
                    st.image(
                        response.content,
                        caption=f"{role_label}: Image File ID: {image_file_id}",
                        use_column_width=True,
                    )
                else:
                    st.warning(
                        f"Failed to download image: HTTP Status Code {response.status_code}"
                    )
