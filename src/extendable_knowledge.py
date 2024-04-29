from document import Document
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
import os

#putting pinecone api key as a en variable, u may do it ur way
os.environ["PINECONE_API_KEY"] = "fc8b9c53-c32b-45d8-8441-b320d56acaff"

def generate_response(openai_api_key, query_text , chat_history , api_data):
    gds_data_split = [Document(page_content='', metadata={'source': 'zendesk_response'})]

    # Iterate through the list and update page_content
    for document in gds_data_split:
        document.page_content = api_data

    print(gds_data_split)
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # Create a vectorstore from documents
    #index i created on pinecone
    index_name = "zendesk-ai"

    # new  vector store
    db = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

    # db = Chroma.from_documents(gds_data_split, embeddings)
    # Create retriever interface
    from langchain.chains import ConversationalRetrievalChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

    # prompt example for reference
    #     general_system_template = f""" 
    # You are examining a document. Use only the heading and piece of context to answer the questions at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Do not add any observations or comments. Answer only in English.
    # ----
    # HEADING: ({document_description})
    # CONTEXT: {{context}}
    # ----
    # """
    # general_user_template = "Here is the next question, remember to only answer if you can from the provided context. Only respond in English. QUESTION:```{question}```"


    general_system_template = f""" 
    You are examining a resume.
    ----
    HEADING: ({"resume of abubakar"})
    CONTEXT: {{context}}
    ----
    """
    general_user_template = "Here is the next question. QUESTION:```{question}```"

    messages = [
                SystemMessagePromptTemplate.from_template(general_system_template),
                HumanMessagePromptTemplate.from_template(general_user_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages( messages )


    # retriever = db.as_retriever()
    retriever = db.as_retriever( # now the vs can return documents
    search_type='similarity', search_kwargs={'k': 1})



    chat_history_tuples = []
    for message in chat_history:
        print(message)
        chat_history_tuples.append((message['role'], message['content']))
        # previous
    # crc = ConversationalRetrievalChain.from_llm(OpenAI(openai_api_key=openai_api_key), retriever, combine_docs_chain_kwargs={'prompt': qa_prompt})
    #new
    crc = ConversationalRetrievalChain.from_llm(OpenAI(openai_api_key=openai_api_key, model="gpt-4-turbo"), retriever, combine_docs_chain_kwargs={'prompt': qa_prompt})
    
    result = crc({'question': query_text, 'chat_history': chat_history_tuples})

    print(result) # {'question': 'please give another one', 'chat_history': [('system', 'give abubakr contact'), ('user', 'abubakrchan555@gmail.com')], 'answer': "\n\nSystem:\nSure, Abubakr's LinkedIn profile is also available for you to contact him. Here is the link: https://www.linkedin.com/in/abubakrchan/"}
    return result['answer'] # System: Sure, Abubakr's LinkedIn profile is also available for you to contact him. Here is the link: https://www.linkedin.com/in/abubakrchan/

# replace with  the api key
chat_history = [
{"role": "system", "content": "give abubakr contact"},
{"role": "user", "content": "abubakrchan555@gmail.com"}
    ]

#make sure to refine the DATA content so that it does not have extra lashes like "\" and other elements so that gpt can better understand it and query it
# u can remove it like
# Remove backslashes
# cleaned_data = DATA.replace("\\", "")

# print(cleaned_data)
DATA = "[{\"id\": 8, \"assignee_id\": 22872142677139, \"subject\": \"this is shite\", \"description\": \"I'm entering the correct 2FA code, but it keeps saying it's invalid. What's going on?\", \"created_ati\": \"2023-11-12T23:37:10Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/8.json\", \"status\": \"open\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/8.json\", \"via\": {\"channel\": \"email\", \"source\": {\"from\": {\"address\": \"alviahmed06@gmail.com\", \"name\": \"Alvi Ahmed\"}, \"to\": {\"name\": \"Supportive\", \"address\": \"support@supportive5741.zendesk.com\"}, \"rel\": null}}}, {\"id\": 6, \"assignee_id\": 22872142677139, \"subject\": \"error\", \"description\": \"I keep getting an error saying 'Incorrect username or email.\", \"created_ati\": \"2023-11-12T23:34:05Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/6.json\", \"status\": \"open\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/6.json\", \"via\": {\"channel\": \"email\", \"source\": {\"from\": {\"address\": \"alviahmed06@gmail.com\", \"name\": \"Alvi Ahmed\"}, \"to\": {\"name\": \"Supportive\", \"address\": \"support@supportive5741.zendesk.com\"}, \"rel\": null}}}, {\"id\": 5, \"assignee_id\": 22872142677139, \"subject\": \"Again, I need help\", \"description\": \"My account is locked after I tried logging in with the wrong password several times\", \"created_ati\": \"2023-11-12T23:32:48Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/5.json\", \"status\": \"open\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/5.json\", \"via\": {\"channel\": \"email\", \"source\": {\"from\": {\"address\": \"alviahmed06@gmail.com\", \"name\": \"Alvi Ahmed\"}, \"to\": {\"name\": \"Supportive\", \"address\": \"support@supportive5741.zendesk.com\"}, \"rel\": null}}}, {\"id\": 3, \"assignee_id\": 22872142677139, \"subject\": \"Hey\", \"description\": \"Hi,\\n\\nThis is a test\", \"created_ati\": \"2023-11-12T23:24:27Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/3.json\", \"status\": \"open\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/3.json\", \"via\": {\"channel\": \"email\", \"source\": {\"from\": {\"address\": \"alviahmed06@gmail.com\", \"name\": \"Alvi Ahmed\"}, \"to\": {\"name\": \"Supportive\", \"address\": \"support@supportive5741.zendesk.com\"}, \"rel\": null}}}, {\"id\": 7, \"assignee_id\": 22872142677139, \"subject\": \"2 factor broken\", \"description\": \"I'm not receiving the two-factor authentication code on my phone.\", \"created_ati\": \"2023-11-12T23:35:03Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/7.json\", \"status\": \"pending\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/7.json\", \"via\": {\"channel\": \"email\", \"source\": {\"from\": {\"address\": \"alviahmed06@gmail.com\", \"name\": \"Alvi Ahmed\"}, \"to\": {\"name\": \"Supportive\", \"address\": \"support@supportive5741.zendesk.com\"}, \"rel\": null}}}, {\"id\": 4, \"assignee_id\": 22872142677139, \"subject\": \"I need help\", \"description\": \"I can't log in because I've forgotten my password.\", \"created_ati\": \"2023-11-12T23:30:22Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/4.json\", \"status\": \"closed\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/4.json\", \"via\": {\"channel\": \"email\", \"source\": {\"from\": {\"address\": \"alviahmed06@gmail.com\", \"name\": \"Alvi Ahmed\"}, \"to\": {\"name\": \"Supportive\", \"address\": \"support@supportive5741.zendesk.com\"}, \"rel\": null}}}, {\"id\": 2, \"assignee_id\": 22872142677139, \"subject\": \"Test ticket\", \"description\": \"Hey! This is a test\", \"created_ati\": \"2023-11-12T23:22:31Z\", \"type\": \"https://supportive5741.zendesk.com/api/v2/requests/2.json\", \"status\": \"closed\", \"url\": \"https://supportive5741.zendesk.com/api/v2/requests/2.json\", \"via\": {\"channel\": \"web\", \"source\": {\"from\": {}, \"to\": {}, \"rel\": null}}}]"
api_data = DATA


results = generate_response("sk-xxxxxxxxxxxxxxxxxxxxxx", "please give another one" , chat_history, api_data)
print(results)  # answer i got: System: Sure, Abubakr's LinkedIn profile is also available for you to contact him. Here is the link: https://www.linkedin.com/in/abubakrchan/