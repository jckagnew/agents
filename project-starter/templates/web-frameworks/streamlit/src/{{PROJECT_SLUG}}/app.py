"""
{{PROJECT_NAME}} Streamlit Application
{{PROJECT_DESCRIPTION}}
"""

import streamlit as st
import openai
import anthropic
import google.generativeai as genai
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import json
import base64
from io import BytesIO
import requests
from typing import List, Dict, Any
import time

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="{{PROJECT_NAME}}",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure AI APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class {{PROJECT_NAME}}App:
    """Main Streamlit application class"""
    
    def __init__(self):
        self.title = "{{PROJECT_NAME}}"
        self.description = "{{PROJECT_DESCRIPTION}}"
        self.version = "1.0.0"
        
        # Initialize session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'data' not in st.session_state:
            st.session_state.data = None
    
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
    
    def analyze_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze uploaded data"""
        analysis = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'numeric_summary': data.describe().to_dict() if len(data.select_dtypes(include=[np.number]).columns) > 0 else {},
            'categorical_summary': data.select_dtypes(include=['object']).describe().to_dict() if len(data.select_dtypes(include=['object']).columns) > 0 else {}
        }
        return analysis
    
    def create_visualization(self, data: pd.DataFrame, chart_type: str, x_col: str, y_col: str) -> go.Figure:
        """Create visualization based on data and chart type"""
        if chart_type == "Line Plot":
            fig = px.line(data, x=x_col, y=y_col, title=f"Line Plot: {x_col} vs {y_col}")
        elif chart_type == "Bar Chart":
            fig = px.bar(data, x=x_col, y=y_col, title=f"Bar Chart: {x_col} vs {y_col}")
        elif chart_type == "Scatter Plot":
            fig = px.scatter(data, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
        elif chart_type == "Histogram":
            fig = px.histogram(data, x=x_col, title=f"Histogram: {x_col}")
        elif chart_type == "Box Plot":
            fig = px.box(data, x=x_col, y=y_col, title=f"Box Plot: {x_col} vs {y_col}")
        else:
            fig = px.scatter(data, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
        
        return fig
    
    def run(self):
        """Run the Streamlit app"""
        # Header
        st.title(f"🚀 {self.title}")
        st.markdown(f"**{self.description}**")
        st.markdown("---")
        
        # Sidebar
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # AI Model Selection
            ai_model = st.selectbox(
                "Select AI Model",
                ["OpenAI", "Anthropic", "Google AI"],
                index=0
            )
            
            # Theme Selection
            theme = st.selectbox(
                "Select Theme",
                ["Light", "Dark", "Auto"],
                index=2
            )
            
            st.markdown("---")
            st.markdown(f"**Version:** {self.version}")
            st.markdown("**Built with:** Streamlit, Plotly, Pandas")
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🤖 AI Chat", "📊 Data Analysis", "📈 Visualizations", 
            "📁 File Upload", "ℹ️ About"
        ])
        
        # AI Chat Tab
        with tab1:
            st.header("AI Chat Interface")
            
            # Chat input
            user_input = st.text_area(
                "Your Message",
                placeholder="Enter your message here...",
                height=100
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                send_button = st.button("Send", type="primary")
            with col2:
                clear_button = st.button("Clear Chat")
            
            if clear_button:
                st.session_state.messages = []
                st.rerun()
            
            if send_button and user_input:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("Thinking..."):
                    if ai_model == "OpenAI":
                        response = self.chat_with_openai(user_input)
                    elif ai_model == "Anthropic":
                        response = self.chat_with_anthropic(user_input)
                    elif ai_model == "Google AI":
                        response = self.chat_with_google(user_input)
                    else:
                        response = "Unknown model selected"
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Data Analysis Tab
        with tab2:
            st.header("Data Analysis")
            
            if st.session_state.data is not None:
                st.subheader("Data Overview")
                
                # Basic info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", st.session_state.data.shape[0])
                with col2:
                    st.metric("Columns", st.session_state.data.shape[1])
                with col3:
                    st.metric("Missing Values", st.session_state.data.isnull().sum().sum())
                
                # Data preview
                st.subheader("Data Preview")
                st.dataframe(st.session_state.data.head(10))
                
                # Analysis
                analysis = self.analyze_data(st.session_state.data)
                
                st.subheader("Data Types")
                st.write(analysis['dtypes'])
                
                st.subheader("Missing Values")
                missing_df = pd.DataFrame(list(analysis['missing_values'].items()), 
                                        columns=['Column', 'Missing Count'])
                st.dataframe(missing_df)
                
                if analysis['numeric_summary']:
                    st.subheader("Numeric Summary")
                    st.dataframe(pd.DataFrame(analysis['numeric_summary']))
                
            else:
                st.info("Please upload a file in the 'File Upload' tab to analyze data.")
        
        # Visualizations Tab
        with tab3:
            st.header("Data Visualizations")
            
            if st.session_state.data is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    chart_type = st.selectbox(
                        "Chart Type",
                        ["Line Plot", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot"]
                    )
                
                with col2:
                    numeric_cols = st.session_state.data.select_dtypes(include=[np.number]).columns.tolist()
                    categorical_cols = st.session_state.data.select_dtypes(include=['object']).columns.tolist()
                    
                    if numeric_cols:
                        x_col = st.selectbox("X Column", st.session_state.data.columns)
                        y_col = st.selectbox("Y Column", numeric_cols)
                    else:
                        st.warning("No numeric columns found for visualization")
                        x_col = y_col = None
                
                if x_col and y_col:
                    try:
                        fig = self.create_visualization(st.session_state.data, chart_type, x_col, y_col)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating visualization: {str(e)}")
            else:
                st.info("Please upload a file in the 'File Upload' tab to create visualizations.")
        
        # File Upload Tab
        with tab4:
            st.header("File Upload")
            
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'json', 'txt'],
                help="Upload a CSV, Excel, JSON, or text file"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        st.session_state.data = pd.read_csv(uploaded_file)
                        st.success("CSV file uploaded successfully!")
                    elif uploaded_file.name.endswith('.xlsx'):
                        st.session_state.data = pd.read_excel(uploaded_file)
                        st.success("Excel file uploaded successfully!")
                    elif uploaded_file.name.endswith('.json'):
                        st.session_state.data = pd.read_json(uploaded_file)
                        st.success("JSON file uploaded successfully!")
                    elif uploaded_file.name.endswith('.txt'):
                        content = uploaded_file.read().decode('utf-8')
                        st.session_state.data = pd.DataFrame({'text': content.split('\\n')})
                        st.success("Text file uploaded successfully!")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error uploading file: {str(e)}")
        
        # About Tab
        with tab5:
            st.header("About {{PROJECT_NAME}}")
            
            st.markdown(f"**Version:** {self.version}")
            st.markdown(f"**Description:** {self.description}")
            st.markdown(f"**Author:** {{AUTHOR_NAME}}")
            st.markdown(f"**Email:** {{AUTHOR_EMAIL}}")
            
            st.markdown("### Features")
            features = [
                "🤖 AI Chat with multiple providers (OpenAI, Anthropic, Google AI)",
                "📊 Data analysis and visualization",
                "📈 Interactive charts and plots",
                "📁 File upload and processing",
                "🎨 Modern, responsive UI",
                "⚡ Fast and efficient processing"
            ]
            
            for feature in features:
                st.markdown(f"- {feature}")
            
            st.markdown("### Built With")
            st.markdown("- Streamlit")
            st.markdown("- Plotly")
            st.markdown("- Pandas")
            st.markdown("- OpenAI API")
            st.markdown("- Anthropic API")
            st.markdown("- Google AI API")

def main():
    """Main entry point"""
    app = {{PROJECT_NAME}}App()
    app.run()

if __name__ == "__main__":
    main()
