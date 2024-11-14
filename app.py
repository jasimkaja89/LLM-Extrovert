import os
import requests
import gradio as gr
import random

# Define the Hugging Face API URL for Falcon-7B-Instruct and your API key
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")


extrovert_prompts = [
    "Create a lively and energetic ad addressing the storrowing problem.",
    "Offer a bold, exciting solution to the storrowing problem.",
    # Add remaining 98 unique prompts here...
] * 4  # Repeats each unique prompt 4 times to make 400 prompts

# Function to query the Hugging Face API
def query_huggingface(personality):
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Select a unique prompt variation based on personality type
    if personality == "Introvert":
        prompt = random.choice(introvert_prompts)
    elif personality == "Extrovert":
        prompt = random.choice(extrovert_prompts)

    # Make a request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # Check if the response is successful
    if response.status_code == 200:
        # Return only the generated text
        try:
            return response.json()[0]['generated_text']
        except (KeyError, IndexError):
            return "Error: Unexpected response format. Please try again."
    elif response.status_code == 401:
        return "Error: Unauthorized. Please check your API key."
    elif response.status_code == 429:
        return "Error: Rate limit exceeded. Please wait and try again later."
    else:
        # General error message with specific status code
        return f"Error {response.status_code}: {response.text}"


def create_extrovert_interface():
    with gr.Blocks() as extrovert_interface:
        gr.Markdown("# Extrovert Profile")

        # Display instructions and question
        gr.Markdown("""
        **Instructions for Respondents**

        Write your response to the following question or problem based on your interaction with the Large Language Model.
        Once you have completed your response, copy and paste the content into the Qualtrics survey and then submit the survey.

        """ + QUESTION)

        with gr.Row():
            # Input box at the top
            user_definition = gr.Textbox(label="Input", lines=5, placeholder="Type your own response here based on the generated advertisement.")
        with gr.Row():
            # Output box below Input
            generated_advertisement = gr.Textbox(label="Output", lines=5)
        with gr.Row():
            # Generate button at the bottom
            generate_button = gr.Button("Generate")

        # Connect generate button to the function to get model response
        generate_button.click(lambda: query_huggingface("Extrovert"), None, generated_advertisement)
    return extrovert_interface


# Launch the interface for Extrovert Profile
print("Launching Extrovert Interface...")
extrovert_interface = create_extrovert_interface()
extrovert_interface.launch(server_name="0.0.0.0", server_port=7881)