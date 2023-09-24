import os

import requests

import gradio as gr

from model import GLMModel, OpenAIModel
from translator import PDFTranslator
from utils import LOG


def main():
    with gr.Blocks() as demo:
        input_file = gr.File(label="PDF file to translate", type="file")

        target_language = gr.Textbox(label="Target language")

        target_file_format = gr.Radio(
            [
                "PDF",
                "Markdown",
            ],
            label="Target file format",
        )

        translate_pages = gr.Slider(
            minimum=1,
            maximum=10,
            step=1,
            default=1,
            label="Pages to translate",
            type="int",
        )

        output_file = gr.File(label="Download translated file")

        submit = gr.Button("Translate")

        submit.click(
            translate,
            inputs=[input_file, target_language, target_file_format, translate_pages],
            outputs=[output_file],
        )

        demo.launch(share=True)

        return


def translate(input_file, target_language, target_file_format, translate_pages):
    model_name = "gpt-3.5-turbo"
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    file_format = "PDF"

    model = OpenAIModel(model=model_name, api_key=openai_api_key)

    translator = PDFTranslator(model)
    return translator.translate_pdf(
        pdf_file_path=input_file.name,
        file_format=target_file_format,
        target_language=target_language,
        pages=translate_pages,
    )


if __name__ == "__main__":
    main()
