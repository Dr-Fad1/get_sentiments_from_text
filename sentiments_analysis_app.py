import streamlit as st
import pandas as pd
import ollama
from io import BytesIO
import time  # Import time module to track time taken

# Set the model for sentiment analysis
llm = "llama3.2:3b"
#llm = "llama3.2-vision:11b"

# Function to get sentiment for each text
def get_sentiment(text):
    sentiment_question = f"Sentiment analysis: {text}. After analysing the message, return only either Positive, Negative or Neutral and nothing else"
    
    response = ollama.chat(model=llm, messages=[
        {
            'role': 'user',
            'content': sentiment_question,
        },
    ])
    return response['message']['content']

# Streamlit App
def main():
    st.title("Sentiment Analysis App")
    
    st.write("Upload an Excel file with a column containing text. The app will analyze the sentiment of each text.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        # Read the uploaded Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Show the first few rows of the uploaded file for preview
        st.write("Data Preview:", df.head())
        
        # Get the column name that contains the text to analyze
        column_name = st.text_input("Enter the column name containing text:", "Text")
        
        # Ensure the specified column exists in the dataframe
        if column_name in df.columns:
            # Start the timer to track the time taken for sentiment analysis
            start_time = time.time()

            # Apply the sentiment analysis to the specified column
            df['Sentiment'] = df[column_name].apply(get_sentiment)
            
            # Calculate the time taken for sentiment analysis
            end_time = time.time()
            time_taken = end_time - start_time

            st.write(f"Sentiment Analysis completed in {time_taken:.2f} seconds.")
            st.write(df.head())  # Show the result

            # Provide download link for the output file
            output_file = BytesIO()
            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sentiment Analysis')
            output_file.seek(0)

            st.download_button(
                label="Download the output with sentiments",
                data=output_file,
                file_name="output_with_sentiment.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error(f"Column '{column_name}' not found in the file.")

if __name__ == "__main__":
    main()
