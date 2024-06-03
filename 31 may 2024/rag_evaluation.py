import os
import sys
from langchain.document_loaders import PyPDFLoader
from langchain.llms import Ollama
from langchain.embeddings import HuggingFaceEmbeddings

pdf_directory = "/home/ec2-user/llama_index/docs/docs/examples/data/10k/"
llm = Ollama(model="llama2:7b", base_url="http://localhost:11434")

def load_embedding_model(model_path, normalize_embedding=True):
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device':'cuda'},
        encode_kwargs = {
            'normalize_embeddings': normalize_embedding  # keep True to compute cosine similarity
        }
    )

model_id = "BAAI/bge-small-en"
ollama_embeddings = load_embedding_model(model_path=model_id)

pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
all_pages = []

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    all_pages.extend(pages)

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=102, add_start_index=True
)

all_splits = text_splitter.split_documents(all_pages)
print(all_splits[0])

from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

vectorstore = Chroma.from_documents(
    documents=all_splits,
    embedding=ollama_embeddings
)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Ask a question
question = "what is uber policy?"
result = qa_chain.invoke(question)
print(result)

from trulens_eval.feedback.provider import LiteLLM
from trulens_eval import Feedback
import numpy as np
from trulens_eval import TruChain, Tru

tru = Tru()
provider = LiteLLM(model_engine="ollama/llama2:7b", api_base='http://localhost:11434')

from trulens_eval.app import App
context = App.select_context(qa_chain)

# Define a groundedness feedback function
f_groundedness = (
    Feedback(provider.groundedness_measure_with_cot_reasons)
    .on(context.collect())  # collect context chunks into a list
    .on_output()
)

# Question/answer relevance between overall question and answer.
f_answer_relevance = (
    Feedback(provider.relevance)
    .on_input_output()
)

# Question/statement relevance between question and each context chunk.
f_context_relevance = (
    Feedback(provider.context_relevance_with_cot_reasons)
    .on_input()
    .on(context)
    .aggregate(np.mean)
)

# instrument with TruChain
tru_recorder = TruChain(qa_chain)
with tru_recorder as recording:
    print(qa_chain.invoke(input="what are uber policies"))

tru_recorder = TruChain(
    qa_chain,
    app_id='Chain1_ChatApplication',
    feedbacks=[f_answer_relevance, f_context_relevance, f_groundedness]
)

response, tru_record = tru_recorder.with_record(qa_chain.invoke, "what are uber policies")
records, feedback = tru.get_records_and_feedback(app_ids=["Chain1_ChatApplication"])
print(records.head())
print(tru.get_leaderboard(app_ids=["Chain1_ChatApplication"]))

tru.run_dashboard()  # open a local streamlit app to explore
# tru.stop_dashboard()  # stop if needed
