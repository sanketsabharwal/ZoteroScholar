import os
import streamlit as st
from utils.zotero_downloader import ZoteroDownloader
from utils.pdf_loader import PDFLoader
from utils.text_processor import TextProcessor
from utils.query_processor import QueryProcessor

# Function to reset the application's state
def reset_application_state():
    # Example: Clearing session variables
    keys_to_clear = ["last_data_source", "papers", "full_text", "paper_chunks"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    print("Application state has been reset.")

# Main UI title
st.title('Zotero Scholar')
st.subheader('Simplify your research with easy document handling and querying with your Zotero files.')

base_dir = "data/zotero_papers"

# User inputs for Zotero credentials and library options
zotero_user_id = st.text_input("Enter Zotero User ID")
zotero_api_key = st.text_input("Enter Zotero API Key", type="password")
download_option = st.selectbox("Choose your Zotero library:", ["Personal Library", "Groups"])
group_limit = None

# Group download limit input field
if download_option == "Groups":
    group_limit = st.number_input("Limit Group Downloads", min_value=1, max_value=10, value=2)

# Button to initiate document sync from Zotero
if st.button('Sync Documents'):
    zotero_downloader = ZoteroDownloader(zotero_user_id, zotero_api_key, base_dir)
    zotero_downloader.download_pdfs(group_limit=group_limit if download_option == "Groups" else None)
    st.success('Your documents have been successfully synced.')

# Input field for the user's query
question_text = st.text_area("Ask a question about your collection of documents.", help="Type here.")

# Button to process the query
if st.button('Get Answer'):
    loader = PDFLoader(base_dir)
    papers, success = loader.load_pdfs()
    if not success:
        st.write("Failed to load papers.")
    else:
        full_text, success = TextProcessor.process_text(papers)
        if not success:
            st.write("Failed to process text.")
        else:
            paper_chunks, success = TextProcessor.split_text(full_text)
            if not success:
                st.write("Failed to split text.")
            else:
                processor = QueryProcessor(paper_chunks, question_text)
                result = processor.process_query()
                st.write(result)

# Button to reset the application state
if st.button('Reset Application'):
    reset_application_state()
    st.experimental_rerun()
