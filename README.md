Different areas of the project have been split into their respective folders:
    - Explanation includes all code required to generate explanations for detected hallucinations
    - QAGS-C, SummEval, and Wikibio contain the code, data, and results required to reproduce the corresponding experiments from the paper

An OpenAI API key for the LLM will need to be provided to run the code. This can be done by setting the 'OPENAI_API_KEY' environment variable. LLM models are also easily interchangable by editing the prompt's 'model' parameter.

A 'Test' folder has been supplied, so that you can run the code for a custom piece of text (just edit the code at the bottom of main.py)
