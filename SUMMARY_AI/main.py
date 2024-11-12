from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import AgentType, Tool, initialize_agent
# from langchain_openai import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from openai import OpenAI as OpenAiConfig

app = Flask(__name__)
CORS(app)

@app.route('/summary', strict_slashes=False)
def query_endpoint():
    os.environ["SERPER_API_KEY"] = ""
    os.environ["OPENAI_API_KEY"] = ""

    llm = OpenAI(temperature=0)
    search = GoogleSerperAPIWrapper()

    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]

    name = request.args.get('name', '')
    issue = request.args.get('issue', '')
    if issue == "undefined":
        issue = "polusi"
    if name == "" or issue == "":
        return jsonify({"result": "Please provide a name and issue"}) 

    file_name = (name + "_" + issue + ".json").lower().replace(" ", "_")
    file_path = os.path.join("results", file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            result = json.loads(f.read())
    else:
        self_ask_with_search = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
        )
        
        result = self_ask_with_search.run("Bagaimana pandangan " + name + " tentang isu " 
+ issue + "?" + " Jawab dalam bahasa Indonesia.")
        result = { "result": result }

        with open(file_path, "a+") as f:
            f.write(json.dumps(result))

    is_secure_request = request.is_secure
    redirect_url = request.url.replace("http://", "https://")

    response = jsonify(result)
    response.headers['Location'] = redirect_url
    response.status_code = 200
                        
    return response
    #:return jsonify({"result": result})

@app.route('/search-ai', strict_slashes=False)
def query_search_endpoint():
    q = request.args.get('q', '')

    if q == "":
        return jsonify({"result": "Please provide a query"})

@app.route('/summary-ai', strict_slashes=False)
def query_visi_endpoint():
    q = request.args.get('q', '')

    if q == "":
        return jsonify({"result": "Please provide a query"})

    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key="",
        model_name="google/gemma-2-9b-it:free",
        temperature=0,
    )

    search = GoogleSerperAPIWrapper(
        serper_api_key="",
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

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    result = agent.run(f"Answer this question in Bahasa Indonesia: {q}")
    result = { "result": result }

    is_secure_request = request.is_secure
    redirect_url = request.url.replace("http://", "https://")

    response = jsonify(result)
    response.headers['Location'] = redirect_url
    response.status_code = 200
                        
    return response
if __name__ == '__main__':
    app.run(debug=True, port=5500)