from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import re
import json
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
import pandas as pd
from portfolio import Portfolio

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
        return jason_res


    def eliminate_think_tags(text):
            
            """
            Removes the <think>...</think> block from a given string.

            Args:
                text (str): The input string containing the <think> tags.

            Returns:
                str: The string with the <think> block removed.
            """
            # The regex pattern matches the <think> tag, any characters (including newlines)
            # in between, and the </think> tag. The re.DOTALL flag ensures that '.'
            # matches newline characters.
            pattern = re.compile(r'<think>.*?</think>', re.DOTALL)
            
            # Use re.sub() to replace the matched pattern with an empty string.
            cleaned_text = pattern.sub('', text)
            
            # Strip any leading/trailing whitespace left after the removal.
            return cleaned_text.strip()
        
    def generateEmail(self,job,links):
                
                
                prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION:
                {job_description}
                
                ### INSTRUCTION:
                You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
                the seamless integration of business processes through automated tools. 
                Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                process optimization, cost reduction, and heightened overall efficiency. 
                Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
                Remember you are Mohan, BDE at AtliQ. 
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
                
                """
                )

                chain_email = prompt_email | self.llm
                res = chain_email.invoke({"job_description": str(job), "link_list": links})
                return res.content


""" myObj = Chain()
pf = Portfolio()

j = myObj.extractJobs("https://jobs.apple.com/en-us/details/200615383/software-engineer?team=SFTWR")



k = pf.query_links(str(j))


res = myObj.generateEmail(j,k)
print(res) """





