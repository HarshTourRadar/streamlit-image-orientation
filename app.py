import streamlit as st
import base64
import requests

# OpenAI API Key
api_key = st.secrets["openai_api_key"]


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Function to send request to OpenAI API
def send_openai_request(base64_image):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                            You are an expert image analyser and you have to do below task for give image.
                            is this image correctly oriented ?
                            just answer in True or False if False then just rotation side and angle to make it correct.
                            Output format:
                            {
                            is_image_orientation_is_correct: Result of True or false,
                            correction: Correction data of angle and side
                            }
                        """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    return response.json()


# Streamlit app
def main():
    st.title("OpenAI Image Orientation Analysis")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Convert the file to base64
        base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")

        # Display the image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Button to analyze the image
        if st.button("Click to Analyze the Orientation of an Image"):
            # Send request to OpenAI API
            st.write("Analyzing...")
            response = send_openai_request(base64_image)
            st.write("Analysis Result:")
            st.json(response.get("choices", [])[0])


if __name__ == "__main__":
    main()
