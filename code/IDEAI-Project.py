import gradio as gr
import os
import plotly.express as px
import pandas as pd
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import AutoModelForSeq2SeqLM

# Authenticate Hugging Face API
access_token = os.getenv("HUGGINGFACE_TOKEN")
if access_token:
    login(access_token)
else:
    print("⚠️ Warning: No Hugging Face token found. Some features may not work.")

# Load the model and tokenizer locally
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create a text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Function to generate responses
def respond(message, history):
    response = generator(message, max_length=100, do_sample=True)[0]["generated_text"]
    return response

# Function to generate a pie chart
def generate_pie_chart():
    data = {
        'Category': ['Wrong Data', 'Integration Issue', 'Application Issue', 'User Entry', 'Design Issue'],
        'Value': [350, 250, 400, 150, 100]
    }
    df = pd.DataFrame(data)
    fig = px.pie(df, names='Category', values='Value', title='Issue Type Wise Distribution')
    return fig

# Function to generate system insights
def get_insights():
    insights = (
        "**Memory on the server is reaching its limit! Take Necessary Action**\n\n"
        "**Application Table space is reaching its limit**\n\n"
        "**The CPU is running at maximum capacity. Can be reduced.**\n\n"
        "**The overall resource cost is high.**"
    )
    return insights

# Function to create the Gradio dashboard
def dashboard():
    with gr.Blocks(fill_height=True) as demo:
        with gr.Row():
            with gr.Column(scale=3):  # Main Content
                gr.Markdown("## 📊 Application Insights Dashboard")
                
                with gr.Tabs():
                    with gr.Tab("Dashboard"):
                        gr.Markdown("## Dashboard Data")
                        gr.Dataframe(
                            [[1, "Total no. of Issues Assigned", 92.3], 
                             [2, "Total No. of Issues in Progress", 75.4]],
                            headers=["ID", "Issue Statuses", "%"]
                        )
                    
                    with gr.Tab("Pie Chart"):
                        gr.Plot(generate_pie_chart())  # Corrected Pie Chart rendering
                    
                    with gr.Tab("Insights"):
                        gr.Markdown("## Key System Insights")
                        gr.Markdown(get_insights(), elem_id="insights-display")
                    
                    with gr.Tab("Chatbot"):
                        gr.Markdown("## Chatbot Integration")
                        button = gr.LoginButton("Sign in")
                        gr.load("models/mistralai/Mistral-7B-Instruct-v0.3", accept_token=button, provider="together",examples=["What are the Jobs failing","List incidents on Job Failure"])
                       # gr.ChatInterface(
                       #     respond, 
                       #     examples=["Jobs are failing on the Nodes", "List all the incidents related to Job Failure"]
                       # )
                    
                    with gr.Tab("Recommendations"):
                        gr.Markdown("## Recommendations")
                        gr.Textbox(value="Suggested action: Optimize prompt for better responses", interactive=False)

    return demo

# Launch the app
demo = dashboard()
print("After Dashboard")
demo.launch()