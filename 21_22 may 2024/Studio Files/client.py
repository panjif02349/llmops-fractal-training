import os
import requests

from PIL import Image
from io import BytesIO
from jsonargparse import CLI


# server_url = "http://127.0.0.1:8000/predict"
server_url = "https://8000-01hy7ksszs01eppcc804p9yjrh.cloudspaces.litng.ai/predict"


def send_image_to_server(prompt: str, image_path:str):
    """
    Sends an image to the server and prints the server's response.

    Args:
    prompt (str): Prompt for the model
    image_path (str): The file path of the image to send.
    """
    # Open the image, convert it to RGB (in case it's not in that mode)
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

    # Print the response from the server
    if response.status_code == 200:
        print("Server response:", response.json())
    else:
        print(
            "Failed to get response from the server, status code:", response.status_code
        )


if __name__ == "__main__":
    image_path = "dog.jpg"
    prompt = "what is in this image?"

    send_image_to_server(image_path=image_path, prompt=prompt)
