"""
{{PROJECT_NAME}} Gradio Application
{{PROJECT_DESCRIPTION}}
"""

import os
import gradio as gr
import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Tuple, Optional
import json
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure AI APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class {{PROJECT_NAME}}App:
    """Main Gradio application class"""
    
    def __init__(self):
        self.title = "{{PROJECT_NAME}}"
        self.description = "{{PROJECT_DESCRIPTION}}"
        self.version = "1.0.0"
        
    def chat_with_openai(self, message: str, model: str = "gpt-4o-mini") -> str:
        """Chat with OpenAI model"""
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat_with_anthropic(self, message: str, model: str = "claude-3-sonnet-20240229") -> str:
        """Chat with Anthropic model"""
        try:
            response = anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": message}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat_with_google(self, message: str, model: str = "gemini-pro") -> str:
        """Chat with Google AI model"""
        try:
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_text(self, text: str, analysis_type: str) -> str:
        """Analyze text with different methods"""
        if analysis_type == "Sentiment":
            # Simple sentiment analysis (replace with actual model)
            positive_words = ["good", "great", "excellent", "amazing", "wonderful"]
            negative_words = ["bad", "terrible", "awful", "horrible", "disappointing"]
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                return "Positive sentiment detected"
            elif negative_count > positive_count:
                return "Negative sentiment detected"
            else:
                return "Neutral sentiment detected"
        
        elif analysis_type == "Word Count":
            words = text.split()
            return f"Word count: {len(words)}"
        
        elif analysis_type == "Character Count":
            return f"Character count: {len(text)}"
        
        else:
            return "Unknown analysis type"
    
    def generate_plot(self, data_type: str, x_values: str, y_values: str) -> str:
        """Generate a plot based on input data"""
        try:
            # Parse input data
            x_data = [float(x.strip()) for x in x_values.split(",")]
            y_data = [float(y.strip()) for y in y_values.split(",")]
            
            if data_type == "Line Plot":
                fig = px.line(x=x_data, y=y_data, title="Line Plot")
            elif data_type == "Bar Chart":
                fig = px.bar(x=x_data, y=y_data, title="Bar Chart")
            elif data_type == "Scatter Plot":
                fig = px.scatter(x=x_data, y=y_data, title="Scatter Plot")
            else:
                return "Unknown plot type"
            
            # Convert to base64 for display
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            return f"data:image/png;base64,{img_base64}"
        
        except Exception as e:
            return f"Error generating plot: {str(e)}"
    
    def process_file(self, file) -> str:
        """Process uploaded file"""
        if file is None:
            return "No file uploaded"
        
        try:
            # Read file based on type
            if file.name.endswith('.csv'):
                df = pd.read_csv(file.name)
                return f"CSV file processed. Shape: {df.shape}\\nColumns: {list(df.columns)}"
            elif file.name.endswith('.txt'):
                with open(file.name, 'r') as f:
                    content = f.read()
                return f"Text file processed. Length: {len(content)} characters"
            else:
                return f"File type not supported: {file.name}"
        
        except Exception as e:
            return f"Error processing file: {str(e)}"
    
    def create_interface(self):
        """Create the Gradio interface"""
        with gr.Blocks(
            title=self.title,
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {
                max-width: 1200px !important;
                margin: 0 auto !important;
            }
            """
        ) as interface:
            
            gr.Markdown(f"# {self.title}")
            gr.Markdown(f"**{self.description}**")
            
            with gr.Tabs():
                # AI Chat Tab
                with gr.Tab("🤖 AI Chat"):
                    with gr.Row():
                        with gr.Column():
                            chat_input = gr.Textbox(
                                label="Your Message",
                                placeholder="Enter your message here...",
                                lines=3
                            )
                            model_choice = gr.Dropdown(
                                choices=["OpenAI", "Anthropic", "Google AI"],
                                value="OpenAI",
                                label="AI Model"
                            )
                            chat_button = gr.Button("Send", variant="primary")
                        
                        with gr.Column():
                            chat_output = gr.Textbox(
                                label="AI Response",
                                lines=10,
                                interactive=False
                            )
                    
                    chat_button.click(
                        fn=self._route_chat,
                        inputs=[chat_input, model_choice],
                        outputs=chat_output
                    )
                
                # Text Analysis Tab
                with gr.Tab("📝 Text Analysis"):
                    with gr.Row():
                        with gr.Column():
                            text_input = gr.Textbox(
                                label="Text to Analyze",
                                placeholder="Enter text here...",
                                lines=5
                            )
                            analysis_type = gr.Dropdown(
                                choices=["Sentiment", "Word Count", "Character Count"],
                                value="Sentiment",
                                label="Analysis Type"
                            )
                            analyze_button = gr.Button("Analyze", variant="primary")
                        
                        with gr.Column():
                            analysis_output = gr.Textbox(
                                label="Analysis Result",
                                lines=5,
                                interactive=False
                            )
                    
                    analyze_button.click(
                        fn=self.analyze_text,
                        inputs=[text_input, analysis_type],
                        outputs=analysis_output
                    )
                
                # Data Visualization Tab
                with gr.Tab("📊 Data Visualization"):
                    with gr.Row():
                        with gr.Column():
                            plot_type = gr.Dropdown(
                                choices=["Line Plot", "Bar Chart", "Scatter Plot"],
                                value="Line Plot",
                                label="Plot Type"
                            )
                            x_values = gr.Textbox(
                                label="X Values (comma-separated)",
                                placeholder="1,2,3,4,5",
                                value="1,2,3,4,5"
                            )
                            y_values = gr.Textbox(
                                label="Y Values (comma-separated)",
                                placeholder="2,4,6,8,10",
                                value="2,4,6,8,10"
                            )
                            plot_button = gr.Button("Generate Plot", variant="primary")
                        
                        with gr.Column():
                            plot_output = gr.Image(label="Generated Plot")
                    
                    plot_button.click(
                        fn=self.generate_plot,
                        inputs=[plot_type, x_values, y_values],
                        outputs=plot_output
                    )
                
                # File Processing Tab
                with gr.Tab("📁 File Processing"):
                    with gr.Row():
                        with gr.Column():
                            file_input = gr.File(
                                label="Upload File",
                                file_types=[".csv", ".txt", ".json"]
                            )
                            process_button = gr.Button("Process File", variant="primary")
                        
                        with gr.Column():
                            file_output = gr.Textbox(
                                label="Processing Result",
                                lines=10,
                                interactive=False
                            )
                    
                    process_button.click(
                        fn=self.process_file,
                        inputs=file_input,
                        outputs=file_output
                    )
            
            # Footer
            gr.Markdown("---")
            gr.Markdown(f"**{{PROJECT_NAME}}** v{self.version} | Built with Gradio")
        
        return interface
    
    def _route_chat(self, message: str, model: str) -> str:
        """Route chat to appropriate model"""
        if model == "OpenAI":
            return self.chat_with_openai(message)
        elif model == "Anthropic":
            return self.chat_with_anthropic(message)
        elif model == "Google AI":
            return self.chat_with_google(message)
        else:
            return "Unknown model selected"
    
    def launch(self, **kwargs):
        """Launch the Gradio app"""
        interface = self.create_interface()
        interface.launch(**kwargs)

def main():
    """Main entry point"""
    app = {{PROJECT_NAME}}App()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )

if __name__ == "__main__":
    main()
