import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient(model="http://127.0.0.1:8080")

def inference(message, history):
    try:
        # Flatten the history and concatenate with the new message
        flattened_history = [item for sublist in history for item in sublist]
        full_message = " ".join(flattened_history + [message])
        
        partial_message = ""
        for token in client.text_generation(
            full_message,
            max_new_tokens=512,
            temperature=.1, 
            top_k=40, 
            top_p=.9, 
            repetition_penalty=1.18, 
            stream=True):
            partial_message += token
            yield partial_message
    except Exception as e:
        # Print the exception to the console for debugging
        print("Exception encountered:", str(e))
        # Optionally, you can yield a message to the user
        yield f"An Error occured please 'Clear' the error and try your question again"

# Create and modify the theme to use Teal
theme = gr.themes.Default(primary_hue="teal").set(
    loader_color="#008080",  # Teal color for loader
)

gr.ChatInterface(
    inference,
    chatbot=gr.Chatbot(height=475),
    textbox=gr.Textbox(placeholder="Please ask me a Question...", container=False, scale=7),
    description="I am demonstration of applied technology.  I and a general knowledge Chatbot that uses a local LLaMA 7B-Chat model.",
    title="Company Chat:  How can I help you today...",
    examples=["What is the link to AWS for product FAQs?"],
    retry_btn="Retry",
    undo_btn="Undo",
    clear_btn="Clear",
    theme=theme,  # Apply the theme here
).queue().launch()
