import streamlit as st
import spacy

@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_md")

nlp = load_nlp()

# FAQs Dataset
FAQ_DATA = [
    {"question": "What is your return policy?", "answer": "You can return any product within 30 days of purchase for a full refund."},
    {"question": "How long does shipping take?", "answer": "Standard shipping takes 3-5 business days. Express takes 1-2 days."},
    {"question": "Do you ship internationally?", "answer": "Yes, we ship to over 50 countries worldwide."},
    {"question": "How can I track my order?", "answer": "We will send you an email with a tracking link once your order has shipped."},
    {"question": "What payment methods do you accept?", "answer": "We accept all major Credit cards, PayPal, and Apple Pay."}
]

def get_best_faq_response(user_query, faq_list, threshold=0.6):
    text_clean = user_query.lower().strip()
    
    # --- GREETINGS HANDLE KARNE KE LIYE ---
    if text_clean in ["hi", "hello", "hey", "asalaam alaikum", "yo"]:
        return "Hello! I am your FAQ assistant. How can I help you today? You can ask me about returns, shipping, or tracking."
        
    user_doc = nlp(text_clean)
    best_match = None
    highest_score = 0.0
    
    for faq in faq_list:
        faq_doc = nlp(faq["question"].lower().strip())
        similarity = user_doc.similarity(faq_doc)
        
        if similarity > highest_score:
            highest_score = similarity
            best_match = faq
            
    # Threshold thoda kam (0.6) kiya hai taaki match aaram se ho sake
    if highest_score >= threshold:
        return best_match["answer"]
    else:
        return "I'm sorry, I couldn't find a matching answer for that. Can you please ask about shipping, returns, tracking, or payments?"

# Streamlit UI
st.set_page_config(page_title="FAQ Bot", page_icon="🤖")
st.title("🤖 FAQ Customer Support Bot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Type your question here..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        bot_response = get_best_faq_response(user_input, FAQ_DATA)
        
    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})