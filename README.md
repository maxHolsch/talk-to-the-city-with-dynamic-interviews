# Talk to the City With a Twist

Adding onto the work done by the AI objectives institute, this program does the following:
Takes a PDF file (exported from the generated webpage report) as input.
Extracts its text content.
Performs an analysis of topics
Uses the Anthropic API to generate follow-up questions aimed at future interviews, based on these identified topics.



Requirements:
Assumes you have installed pytesseract and have Tesseract installed on your system.


Install instructions:
For Tesseract:
- On macOS (with Homebrew):
- brew install tesseract

On Ubuntu/Debian:
- sudo apt-get install tesseract-ocr

For Python binding:
-pip install pytesseract

## Here's what our tool does (in detail)

Reads an image (screenshot of a report webpage).
Uses Tesseract (OCR) to extract text from the image.
Cleans and processes the text to improve the prompt for the Anthropic API.
sends this to the Anthropic API (Claude model) using a given prompt, requesting:
Identification of commonly discussed topics.
Identification of less mentioned, underexplored topics.
Generation of three sets of interview questions (deep-dive, underexplored, and connecting questions).
returns the resulting questions in a structured JSON format of new question directions to take.

future directions goals: 
- get this directly integrated with talk to the city, such that when deployed this tool is lightning quick to use
- Resolve bugs with more modern versions of Mac and Windows



## Talk to the City Turbo

This is the [graph-based reports application](./turbo). It is JS / TS based, it generates interactive reports, and a very wide variety of LLM apps.

e.g

[Heal Michigan](https://tttc-turbo.web.app/report/heal-michigan-9)  
[Taiwan same-sex marriage](https://tttc-turbo.web.app/report/taiwan-zh)  
[Mina protocol](https://tttc-turbo.web.app/report/mina-protocol)


## Talk to the City Reports

This is the [CLI based reports application](./scatter). It is python and next based, and generates static interactive scatter-plot reports with summaries.

e.g

[Heal Michigan](https://tttc.dev/heal-michigan)  
[Recursive Public](https://tttc.dev/recursive)  
[GenAI Taiwan](https://tttc.dev/genai)
