import os
import requests
import gradio as gr
import random

# Define the Hugging Face API URL for Falcon-7B-Instruct and your API key
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Define the fixed question with larger font and bold using Markdown for proper rendering
QUESTION = "**Create a creative advertisement about a new solution to the storrowing problem.**"

# Define extrovert prompts
extrovert_prompts = [
    f"{QUESTION} Provide a lively and high-energy message.",
    f"{QUESTION} Create a bold, exciting advertisement.",
    f"{QUESTION} Share an enthusiastic, vibrant ad idea.",
    f"{QUESTION} Develop a high-energy promotional concept.",
    f"{QUESTION} Propose a dynamic and thrilling ad message.",
    f"{QUESTION} Present an engaging, energetic advertisement.",
    f"{QUESTION} Craft an upbeat, extroverted promotional message.",
    f"{QUESTION} Design a compelling, lively advertisement concept."
] * 50  # Replicates to create a pool of 400 options when shuffled

# Function to query the Hugging Face API with randomness for diversity
def query_huggingface(personality):
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Select a unique prompt variation based on personality type
    if personality == "Introvert":
        prompt = random.choice(introvert_prompts)  # Ensure introvert prompts are defined
    elif personality == "Extrovert":
        prompt = random.choice(extrovert_prompts)

    # Make a request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # Check if the response is successful
    if response.status_code == 200:
        # Return only the generated text
        return response.json()[0]['generated_text']
    else:
        return f"Error: {response.status_code}, {response.text}"

def create_extrovert_interface():
    with gr.Blocks() as extrovert_interface:
        # Display the Extrovert Profile heading
        gr.Markdown("# Extrovert Profile")
        
        # Display instructions and question
        gr.Markdown("""
        **Instructions for Respondents**
        
        Write your response to the following question or problem based on your interaction with the Large Language Model.
        Once you have completed your response, copy and paste the content into the Qualtrics survey and then submit the survey.
        
        """ + QUESTION)
        
        with gr.Row():
            # Output area for the model-generated text
            generated_advertisement = gr.Textbox(label="Generated Advertisement", lines=5)
            # Button to generate the output
            generate_button = gr.Button("Generate")
            # Empty textbox for user to input their own definition
            user_definition = gr.Textbox(label="Your Definition", lines=5, placeholder="Type your own response here based on the generated advertisement.")

        # Connect generate button to the model function
        generate_button.click(lambda: query_huggingface("Extrovert"), None, generated_advertisement)
    return extrovert_interface


# Launch the interface for Extrovert Profile
print("Launching Extrovert Interface...")
extrovert_interface = create_extrovert_interface()
extrovert_interface.launch(server_name="0.0.0.0", server_port=7881)
