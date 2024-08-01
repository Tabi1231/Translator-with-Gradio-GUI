**TRANS_GUI**
This is a simple text translator application built using Gradio and Googletrans. It allows users to input text manually or upload a text file, select a target language, and get the translated text.

**Features**
Translate text from a textbox or a file
Supports multiple target languages
Easy-to-use web interface built with Gradio
Requirements
Python 3.6+
Gradio
Googletrans
Installation
Clone the repository:




**Create a virtual environment (optional but recommended):
**
sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

sh
Copy code
pip install -r requirements.txt
If you encounter dependency conflicts, you can install the packages individually as follows:

sh
Copy code
pip install gradio
pip install googletrans==4.0.0-rc1
pip install httpx==0.13.3
Usage
Run the application:

sh
Copy code
python app.py
Open your web browser and go to the URL provided by Gradio (usually http://127.0.0.1:7860/).

Enter text in the textbox or upload a file containing the text you want to translate.

Select the target language from the dropdown menu.

Click the "Translate" button to see the translated text.

**Code Explanation**
divide_text
This function divides the input text into smaller segments, each up to 4500 characters, ensuring lines are not split.

python
Copy code
def divide_text(input_text, max_length=4500):
    text_lines = input_text.split("\n")
    segments = []
    current_segment = ""
    for line in text_lines:
        if len(current_segment + line) > max_length:
            segments.append(current_segment)
            current_segment = ""
        current_segment += line + "\n"
    if current_segment:
        segments.append(current_segment)
    return segments
perform_translation
This function translates text from a source language to a target language using Googletrans.

python
Copy code
def perform_translation(input_text, target_lang):
    translator = Translator()
    text_segments = divide_text(input_text)
    final_translation = ''
    for segment in text_segments:
        translation = translator.translate(segment, src='auto', dest=target_lang).text
        final_translation += translation + "\n"
    final_translation = re.sub(r'[\n]{3,}', '\n\n', final_translation.strip())
    final_translation = final_translation.strip()
    return final_translation
translate_text
This function takes input from the text box and the uploaded file, combines the text, and performs the translation.

python
Copy code
def translate_text(input_text, file, target_lang):
    combined_text = input_text
    if file:
        combined_text += '\n' + file.decode('utf-8')
    if combined_text.strip():
        try:
            translated_text = perform_translation(combined_text, target_lang)
            return translated_text
        except Exception as e:
            return f"Translation Error: {str(e)}"
    else:
        return "Please enter text or upload a file to translate."
Gradio Interface
This part sets up the Gradio interface.

python
Copy code
with gr.Blocks() as demo:
    gr.Markdown("## Text Translator")
    input_text = gr.Textbox(label="Enter Text", placeholder="Type your text here...", lines=10)
    file = gr.File(label="Upload File")
    language_dropdown = gr.Dropdown(["en", "es", "fr", "de", "it", "pt", "zh-cn", "ja", "ko"], label="Target Language", value="en")
    translate_button = gr.Button("Translate")
    output_text = gr.Textbox(label="Translated Text", lines=10)
    translate_button.click(fn=translate_text, inputs=[input_text, file, language_dropdown], outputs=output_text)
demo.launch()
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.
