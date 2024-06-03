import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from jsonargparse import CLI
from io import StringIO
import tempfile
import os

st.set_page_config(layout="wide")

# server_url = "https://8000-01hy7ksszs01eppcc804p9yjrh.cloudspaces.litng.ai/predict"
server_url = "http://0.0.0.0:8000/predict"


def send_image_to_server(prompt: str, image_path: str):
   
    image = Image.open(image_path).convert("RGB")

    # Convert the image to bytes
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()

    # Send a POST request to the server with the image
    response = requests.post(
        server_url,
        json={
            "image_bytes": image_bytes.hex(),  # Convert bytes to hex string for JSON serialization
            "prompt": prompt,
        },
    )

    # Return the response from the server
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get response from the server, status code: " + str(response.status_code))
        return None

def main():
    st.title("PaliGemma Multimodal LLM Demo")

    col1,_, col2 = st.columns([1,0.3,1])

    with col1:
        st.header("Upload Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        prompt = st.text_area("Enter a prompt")

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.text(" ")
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Save the image to a temporary file
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # st.write(f"Image saved to: {temp_file_path}")

            if prompt and image :              
                
                # Display the result in the second column
                with col2:   
                    st.text(" ")                 
                    check=st.button("Process Image with PaliGemma")
                    if check:
                        response = send_image_to_server(prompt, temp_file_path)
                        st.text(" ")
                        st.text(" ")
                        st.subheader(response["output"])
                    

if __name__ == "__main__":
    main()
