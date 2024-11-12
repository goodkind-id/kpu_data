from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, LLMRequestsChain, APIChain
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

@app.route('/', strict_slashes=False)
def summarize_candidate_query_endpoint():
    question = request.args.get('q', '')
    path = request.args.get('path', '')

    if question == "" or path == "":
        return jsonify({"result": "Please provide a query and the leader path"})

    template = """Between >>> and <<< are the raw object from the API request.
    Important: 
        - Answer the question only using Bahasa Indonesia.
        - Extract the answer to the question '{question}' or say "Tidak ditemukan" if the information is not contained.
        - Answer only using plain text avoid using html or markdown format

    >>> {requests_result} <<<"""

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

    # print(response)

    # output = response.output

@app.route('/search-with-path', strict_slashes=False)
def path_candidate_query_endpoint():
    question = request.args.get('q', '')
    path = request.args.get('path', '')

    if question == "" or path == "":
        return jsonify({"result": "Please provide a query and the leader path"})

    GOODKIND_API_DOCS =  """BASE URL: https://goodkind.id/api/

        API Documentation
        The API endpoint /public/leaders/[leader-path] provides detailed information about political leaders. This endpoint responds with a JSON object containing relevant information about the specified leader. The URL path parameter `[leader-path]` should be replaced by the leader's unique identifier.

        ### URL Path Parameter:
        - `leader-path`: String. Required. This is the unique path identifier for the leader (e.g., `khofifah-indar-parawansa`).

        ### Example API Call:
        URL: https://goodkind.id/api/public/leaders/khofifah-indar-parawansa

        ### Response Structure:
        The response is returned as a JSON object with the following fields:

        - `data`: An object containing detailed information about the leader:
        - `path`: String. The unique identifier for the leader.
        - `name`: String. The full name of the leader.
        - `gender`: String. The gender of the leader (e.g., "female").
        - `info`: Object containing additional details about the leader:
            - `summary`: String. A brief summary of the leader’s background, potentially including a link to a more detailed document.
            - `pendidikan`: Array. A list of education history items.
            - `organisasi`: Array. A list of organizations the leader has been involved with.
            - `pekerjaan`: Array. A list of job positions the leader holds or has held.
            - `calon_id`: String. The unique identifier for the candidate.
            - `status_hukum`: Array of Strings. Legal status information (e.g., "Tidak memiliki status hukum").
            - `vision`: String. The leader’s vision statement, typically with a link to a more detailed document.
            - `mission`: String. The leader’s mission statement, formatted as a numbered list.
            - `no_urut`: Integer. The order number of the leader in the election.
            - `parties`: String. The list of political parties associated with the leader, separated by commas.
            - `pair_id`: String. The unique identifier for the leader’s pair candidate.
        - `title`: String. The leader’s title (e.g., "Calon Gubernur").
        - `community`: Object containing information about the leader’s community:
            - `level`: String. The administrative level of the community (e.g., "Provinsi").
            - `population`: Integer. The population of the community.
            - `name`: String. The name of the community.
            - `parents`: Object containing nested location information:
            - `province`: Object with `name`: String (e.g., "Provinsi DKI Jakarta").
            - `regency`: Object with `name`: String (e.g., "Kota Administrasi Jakarta Selatan").
            - `kecamatan`: Object with `name`: String (e.g., "Kecamatan Setiabudi").
            - `kelurahan`: Object with `name`: String (e.g., "Kelurahan Karet Kuningan").
        - `leaderIssues`: Array of objects with issues or concerns identified by the leader:
            - `value`: String. A description of an issue or concern (e.g., "Polusi Udara, Sampah, dlsb.").
        - `party`: Object with the political party details:
            - `code`: String. The party short-name (e.g., "PKB").
            - `name`: String. The name of the political party (e.g., "Partai Kebangkitan Bangsa").
    
    Disclaimer:
     - Please answer only the core candidate details based on the given question if available, without including URLs, code blocks, or extra explanations. 
     - Answer only using Bahasa Indonesia.
     - If the answer not available, return "Pencarian tidak ditemukan".
    """

    try:
        chain = APIChain.from_llm_and_api_docs(
            llm,
            GOODKIND_API_DOCS,
            verbose=True,
            limit_to_domains=["https://goodkind.id/"],
        )

        response = chain.run(question)
        clean_response = response.replace("```", "").strip()

        return jsonify({
            "result": clean_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search-candidate', strict_slashes=False)
def search_candidate_query_endpoint():
    question = request.args.get('q', '')

    if question == "" or path == "":
        return jsonify({"result": "Please provide a query"})

    GOODKIND_API_DOCS =  """BASE URL: https://goodkind.id/api/

    API Documentation
    The API endpoint /search/pilkada allows for searching candidates based on various parameters like name, party, and mission. The endpoint responds with a JSON containing relevant candidate data based on specified filters. All URL parameters are listed below:

    Parameter         Format         Required     Default     Description
    q                 String         No           None        A search term to filter candidates by name.
    size              Integer        No           10          The number of results to return per page.
    mission           String         No           None        A filter to select candidates based on their campaign mission. Use '+' to separate multiple words (e.g., 'makan+gratis').
    page              Integer        No           1           The page number for paginated results.
    party             String         No           None        A filter to select candidates by their party affiliation.
    gender            String         No           None        A filter to select candidates by gender. Acceptable values are 'male' and 'female'.

    Example API Call
    URL: https://goodkind.id/api/search/pilkada?q=budi&size=30&mission=makan+gratis&page=1&party=PASA&gender=female

    Response Structure
    The response is returned as JSON array of object with the following fields:

    - `data`: An array of candidate information matching the search criteria. Each object in the `data` array contains the following fields:
        - `id`: String. Unique identifier for the candidate.
        - `communityID`: String. Identifier for the candidate's region.
        - `communityName`: String. Region associated with the candidate.
        - `gender`: String. Gender of the candidate (e.g., "male" or "female").
        - `info`: Object. Additional details about the candidate.
            - `no_urut`: String. Candidate's number in the election.
            - `status_hukum`: Array of Strings. Legal status information (e.g., ["Tidak memiliki status hukum"]).
            - `parties`: String. List of political parties that support the candidacy, separated by commas (e.g., "GOLKAR,PKS,HANURA").
        - `location`: String. Region associated with the candidate.
        - `locationLevel`: String. Administrative level of the location (e.g., "Kabupaten", "Kota", "Provinsi").
        - `name`: String. Name of the candidate.
        - `mission`: String. Mission statement of the candidate.
        - `vision`: String. Vision statement of the candidate.
        - `parties`: String. List of political parties that support the candidacy, listed as comma-separated values.
        - `path`: String. URL path for the candidate's profile.
        - `picUrl`: String. URL of the candidate's profile picture.
        - `status`: String. Status code of the candidate in the context.
        - `title`: String. Title of the candidate (e.g., "Calon Bupati", "Calon Wakil Gubernur").
    
    Disclaimer:
     - Please answer only the core candidate details based on the given question if available, without including URLs, code blocks, or extra explanations. 
     - Answer only using Bahasa Indonesia.
     - If the answer not available, return "Pencarian tidak ditemukan".
    """

    try:
        chain = APIChain.from_llm_and_api_docs(
            llm,
            GOODKIND_API_DOCS,
            verbose=True,
            limit_to_domains=["https://goodkind.id/"],
        )

        response = chain.run(question)
        clean_response = response.replace("```", "").strip()

        return jsonify({
            "result": clean_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/google-search', strict_slashes=False)
def gogole_query_endpoint():
    question = request.args.get('q', '')

    if question == "":
        return jsonify({"result": "Please provide a query"})

    template = """Between >>> and <<< are the raw search result text from google.
    Important: Answer the question using Bahasa Indonesia.
    Extract the answer to the question '{query}' or say "not found" if the information is not contained.
    Use the format
    Extracted:<answer or "not found">
    >>> {requests_result} <<<
    Extracted:"""

    prompt = PromptTemplate(
        input_variables=["query", "requests_result"],
        template=template,
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    chain = LLMRequestsChain(llm_chain=llm_chain)

    # question = "Visi dan misi viananda pramesti calon wali kota kediri"
    inputs = {
        "query": question,
        "url": "https://goodkind.id/api/search/pilkada?q=" + question.replace(" ", "+")
        # "url": "https://www.google.com/search?q=" + question.replace(" ", "+"),
    }

    response = chain.invoke(inputs)
    # print(response)

    # output = response.output

    # print(output)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5500)

