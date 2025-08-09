from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import re
import json
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()
k = os.getenv("GROQ_API_KEY")


class Chain:
    def __init__(self):

        self.llm = ChatGroq(
        model="deepseek-r1-distill-llama-70b",
        temperature=0,
        # other params...
    )
        
    def extract_json_from_string(self,text):

        # Regex to find text between ```json and ```, using re.DOTALL to match newlines
        match = re.search(r'```json\n(.*?)```', text, re.DOTALL)
        if match:
            json_string = match.group(1).strip()
            try:
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        return None
    

    def extractJobs(self,url):

        loader = WebBaseLoader(url)
        content1 = loader.load().pop().page_content

        prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON NO PREAMBLE :    
        """
)
        

        chain_extract = prompt_extract | self.llm 
        res = chain_extract.invoke(input={'page_data':content1})
        jason_res = self.extract_json_from_string(res.content)
        print(jason_res)


myObj = Chain()
myObj.extractJobs("https://amazon.jobs/en/jobs/3055226/software-engineer-i")