import os
import requests
import gradio as gr
import random

# Define the Hugging Face API URL for Falcon-7B-Instruct and your API key
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Extensive lists of nuanced prompts for introverts and extroverts
introvert_prompts = [
    "Offer a quiet, reflective message for a solution to the storrowing problem.",
    "Develop a subtle, insightful advertisement for addressing the storrowing problem.",
    "Provide a calm and thought-provoking promotional angle for solving the storrowing problem.",
    "Share an introspective, thoughtful message to creatively address storrowing.",
    "Present a serene, deep concept for overcoming the storrowing challenge.",
    "Propose a gentle, introspective advertisement idea to tackle the storrowing issue.",
    "Craft a soothing and thoughtful promotional idea for resolving storrowing.",
    "Design an understated, reflective storyboard for combating storrowing."
] * 50  # Creates a pool of 400 options when shuffled

extrovert_prompts = [
    "Provide a lively and high-energy concept for a solution to the storrowing problem.",
    "Create a bold, exciting advertisement to address storrowing.",
    "Share an enthusiastic, vibrant storyboard idea to tackle storrowing.",
    "Develop a high-energy promotional concept for solving storrowing.",
    "Propose a dynamic and thrilling storyboard to combat the storrowing problem.",
    "Present an engaging, energetic advertisement to solve storrowing.",
    "Craft an upbeat, extroverted promotional angle for addressing the storrowing issue.",
    "Design a compelling, lively concept for resolving storrowing."
] * 50  # Creates a pool of 400 options when shuffled

# Function to query the Hugging Face API with improved output handling
def query_huggingface(personality):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    prompt = random.choice(introvert_prompts if personality == "Introvert" else extrovert_prompts)

    try:
        # Make the API request
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Extract and return the generated text
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            output_text = result[0]['generated_text']

            # Remove the original prompt from the generated text if present
            clean_output = output_text.replace(prompt, "").strip()
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
        
        # Add revised instructions
        gr.Markdown("""
        There is a problem called **"Storrowing Problem"**. Use the AI tool below to understand the problem and find a solution for a creative advertisement to solve this. 

        ### Instructions:
        The AI tool cannot create a full advertisement. A broad storyboard of how the advertisement would look would be sufficient. You would have to interact with the AI tool below to understand the problem and ask the right questions and give appropriate prompts to generate the outline/storyboard of an effective advertisement. 

        Whenever you are ready, start giving the inputs in the input box and click on "Generate". The AI tool will generate answers to your question. When you are happy with the solution, paste the solution in the Qualtrics link.
        """)

        # Create input and output boxes
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
