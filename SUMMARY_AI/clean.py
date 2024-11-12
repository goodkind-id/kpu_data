from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, LLMRequestsChain
from langchain_core.prompts import PromptTemplate

app = Flask(__name__)
CORS(app)

API_BASE = "https://openrouter.ai/api/v1"
AI_MODEL = "google/gemma-2-9b-it"
SERPER_API_KEY = ""
OPENROUTER_API_KEY = ""
OPENAI_API_KEY = ""

llm = ChatOpenAI(
    openai_api_base=API_BASE,
    openai_api_key=OPENROUTER_API_KEY,
    model_name=AI_MODEL,
    temperature=0,
)

@app.route('/summary', strict_slashes=False)
def summarize_candidate_query_endpoint():
    question = request.args.get('q', '')
    path = request.args.get('path', '')

    if question == "" or path == "":
        return jsonify({"result": "Please provide a query and the leader path"})

    template = """Between >>> and <<< are the raw object from the API request.

    >>> {requests_result} <<<

    Important: 
        - Answer the question only using Bahasa Indonesia.
        - Extract the answer to the question '{question}' or say "Tidak ditemukan" if the information is not contained.
        - Answer only using plain text avoid using html or markdown format
    """

    prompt = PromptTemplate(
        input_variables=["question", "requests_result"],
        template=template,
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    chain = LLMRequestsChain(llm_chain=llm_chain)

    inputs = {
        "question": question,
        "url": "https://goodkind.id/api/public/leaders/" + path,
    }

    response = chain.invoke(inputs)

    try:
        output = response.get('output', '')
        return jsonify({
            "result": output
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5500)