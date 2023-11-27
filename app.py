import os
import argparse
import glob
import html
import io
import re
import time
from pypdf import PdfReader, PdfWriter
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import *
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure_openai import *
from config import *

import streamlit as st

st.header('Search Engine - Document')

user_input = st.text_input('Enter your question here:', 
                           'What is Diploblastic and Triploblastic Organisation ?')

if st.button('Submit'):

    service_name = "YOUR-SEARCH-SERVICE-NAME"
    service_name = searchservice
    key = "YOUR-SEARCH-SERVICE-ADMIN-API-KEY"
    key = searchkey

    endpoint = "https://{}.search.windows.net/".format(searchservice)
    index_name = index

    azure_credential =  AzureKeyCredential(key)

    search_client = SearchClient(endpoint=endpoint,
                                        index_name=index_name,
                                        credential=azure_credential)


    KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT") or "content"
    KB_FIELDS_CATEGORY = os.environ.get("KB_FIELDS_CATEGORY") or category
    KB_FIELDS_SOURCEPAGE = os.environ.get("KB_FIELDS_SOURCEPAGE") or "sourcepage"

    exclude_category = None

    print("Searching:", user_input)
    print("-------------------")
    filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None
    r = search_client.search(user_input, 
                            filter=filter,
                            query_type=QueryType.SEMANTIC, 
                            query_language="en-us", 
                            query_speller="lexicon", 
                            semantic_configuration_name="default", 
                            top=3)
    results = [doc[KB_FIELDS_SOURCEPAGE] + ": " + doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    content = "\n".join(results)

    references =[]
    for result in results:
        references.append(result.split(":")[0])
    st.markdown("### References:")
    st.write(" , ".join(set(references)))

    conversation=[{"role": "system", "content": "Assistant is a great language model formed by OpenAI."}]
    prompt = create_prompt(content,user_input)            
    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})
    reply = generate_answer(conversation)

    st.markdown("### Answer is:")
    st.write(reply)

