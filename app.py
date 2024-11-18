import os
import requests
import gradio as gr
import random

# Define the Hugging Face API URL for Falcon-7B-Instruct and your API key
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Extensive lists of nuanced prompts for introverts and extroverts with added context
introvert_prompts = [
    "Provide a thoughtful and serene advertisement for addressing the 'storrowing problem,' a metaphorical challenge representing creative blockages in generating ideas.",
    "Develop an introspective solution to the 'storrowing problem,' which symbolizes overcoming mental barriers in creativity.",
    "Share an introspective, reflective storyboard for addressing the 'storrowing problem' as a creative challenge.",
    "Propose a calm and subtle advertisement concept to solve the 'storrowing problem,' a representation of creative roadblocks.",
    "Craft a gentle and insightful promotional idea for resolving the 'storrowing problem,' representing creative stagnation."
] * 50  # Repeat for a larger pool of options

extrovert_prompts = [
    "Design an energetic and engaging storyboard for tackling the 'storrowing problem,' a creative challenge requiring innovative thinking.",
    "Propose a high-energy promotional idea to resolve the 'storrowing problem,' symbolizing breaking through creative barriers.",
    "Create a bold and exciting advertisement to address the 'storrowing problem,' representing a need for fresh ideas.",
    "Share a dynamic and thrilling storyboard for combating the 'storrowing problem,' a metaphorical challenge in creativity.",
    "Present a vibrant and enthusiastic promotional concept to overcome the 'storrowing problem' and foster innovation."
] * 50  # Repeat for a larger pool of options

# Function to query the Hugging Face API with contextual prompts
def query_huggingface(personality):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    context = "The 'storrowing problem' is a metaphorical challenge representing creative blocks in advertising."
    prompt = random.choice(introvert_prompts if personality == "Introvert" else extrovert_prompts)
    full_prompt = f"{context}\n\n{prompt}"

    try:
        # Make the API request
        response = requests.post(API_URL, headers=headers, json={"inputs": full_prompt})
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Extract and return the generated text
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            output_text = result[0]['generated_text']

            # Remove the original prompt from the generated text if present
            clean_output = output_text.replace(full_prompt, "").strip()
            return clean_output
        else:
            return "Error: Unexpected response format from the model. Please try again."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request error: {req_err}"
    except Exception as err:
        return f"An unexpected error occurred: {err}"

# Function to create the Gradio interface
def create_interface(profile_title, personality):
    with gr.Blocks() as interface:
        gr.Markdown(f"## {profile_title}")

        # Instructions for users
        gr.Markdown("""
        There is a problem called **"Storrowing Problem"**. Use the AI tool below to understand the problem and find a solution for a creative advertisement to solve this.

        ### Instructions:
        The AI tool cannot create a full advertisement. A broad storyboard of how the advertisement would look would be sufficient. You would have to interact with the AI tool below to understand the problem and ask the right questions and give appropriate prompts to generate the outline/storyboard of an effective advertisement.

        Whenever you are ready, start giving the inputs in the input box and click on "Generate". The AI tool will generate answers to your question. When you are happy with the solution, paste the solution in the Qualtrics link.
        """)

        # Input and output components
        with gr.Row():
            user_input = gr.Textbox(label="INPUT", placeholder="Type your question or prompt here.", lines=4)
        with gr.Row():
            generate_button = gr.Button("Generate")
        with gr.Row():
            generated_advertisement = gr.Textbox(label="OUTPUT", lines=5)

        # Button functionality to query the API
        generate_button.click(
            lambda question: query_huggingface(personality) if question.strip() else "Please enter a valid prompt.",
            inputs=user_input,
            outputs=generated_advertisement
        )

    return interface

print("Launching Profile 2 Interface...")
profile_2_interface = create_interface("Profile 2", "Extrovert")
profile_2_interface.launch(server_name="0.0.0.0", server_port=7881)







