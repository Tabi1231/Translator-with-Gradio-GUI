import gradio as gr
import re
from googletrans import Translator

# Function to divide text into smaller segments, each up to 4500 characters, ensuring lines are not split
def divide_text(input_text, max_length=4500):
    # Break the text into lines
    text_lines = input_text.split("\n")
    # Initialize a list to hold text segments
    segments = []
    # Temporary buffer for the current segment
    current_segment = ""

    # Iterate through each line
    for line in text_lines:
        # Check if adding the line exceeds the max length, if so, store the segment and reset the buffer
        if len(current_segment + line) > max_length:
            segments.append(current_segment)
            current_segment = ""
        # Append the line to the current segment
        current_segment += line + "\n"

    # Add any remaining text as the last segment
    if current_segment:
        segments.append(current_segment)

    # Return the list of text segments
    return segments

# Function to translate text from a source language to a target language
def perform_translation(input_text, target_lang):
    translator = Translator()
    text_segments = divide_text(input_text)

    final_translation = ''
    for segment in text_segments:
        translation = translator.translate(segment, src='auto', dest=target_lang).text
        final_translation += translation + "\n"

    # Clean up extra new lines from the translated text
    final_translation = re.sub(r'[\n]{3,}', '\n\n', final_translation.strip())
    final_translation = final_translation.strip()

    return final_translation

def translate_text(input_text, file, target_lang):
    # Get text from input
    combined_text = input_text
    if file:
        combined_text += '\n' + file.decode('utf-8')
    
    # Perform translation
    if combined_text.strip():
        try:
            translated_text = perform_translation(combined_text, target_lang)
            return translated_text
        except Exception as e:
            return f"Translation Error: {str(e)}"
    else:
        return "Please enter text or upload a file to translate."

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Text Translator")
    
    with gr.Row():
        input_text = gr.Textbox(label="Enter Text", placeholder="Type your text here...", lines=10)
    
    with gr.Row():
        file = gr.File(label="Upload File")
    
    with gr.Row():
        language_dropdown = gr.Dropdown(["en", "es", "fr", "de", "it", "pt", "zh-cn", "ja", "ko"], label="Target Language", value="en")
    
    translate_button = gr.Button("Translate")
    output_text = gr.Textbox(label="Translated Text", lines=10)
    
    translate_button.click(fn=translate_text, inputs=[input_text, file, language_dropdown], outputs=output_text)

# Launch the Gradio interface
demo.launch()
