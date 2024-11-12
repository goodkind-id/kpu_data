from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.tracers import ConsoleCallbackHandler

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

search = GoogleSerperAPIWrapper(
    serper_api_key=SERPER_API_KEY,
    gl="id",
    hl="id",
    k=2,
    type="search"
)

tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]


@app.route('/summary', strict_slashes=False)
def query_endpoint():
    name = request.args.get('name', '')
    issue = request.args.get('issue', '')
    q = request.args.get('q', '')

    if (name == "" or issue == "") and q == "":
        return jsonify({"result": "Please provide a query"})

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors = True,
    )

    if q != "":
        result = agent.run(f"Answer this question in plain text using Bahasa Indonesia: {q}")
        result = { "result": result }

    else:
        if issue == "undefined":
            issue = "polusi"

        file_name = (name + "_" + issue + ".json").lower().replace(" ", "_")
        file_path = os.path.join("results", file_name)

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                result = json.loads(f.read())
        else:
            result = agent.run("Bagaimana pandangan " + name + " tentang isu " + issue + "?" + " Jawab dalam bahasa Indonesia.")
            result = { "result": result }

            with open(file_path, "a+") as f:
                f.write(json.dumps(result))

    redirect_url = request.url.replace("http://", "https://")

    response = jsonify(result)
    response.headers['Location'] = redirect_url
    response.status_code = 200
                        
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5500)