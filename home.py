import streamlit as st
import ML

def main(user_id, pdf_texts):
    st.sidebar.title("Upload your Reports")
    pdf_docs = st.sidebar.file_uploader("Upload PDF documents", accept_multiple_files=True, type=["pdf", "jpeg", "png"])
    
    submit = st.sidebar.button("Submit")

    if submit and pdf_docs:
        # Clear previous chat history before processing new documents
        st.session_state["chat_history"] = []
        st.session_state["pdf_texts"] = []

        for doc in pdf_docs:
            if doc.type == 'application/pdf':
                pdf_text = ML.extract_text_from_pdf(doc)
            else:
                pdf_text = ML.extract_text_from_image(doc)
            if "no such file" not in pdf_text.lower():
                st.session_state["pdf_texts"].append(pdf_text)
                st.session_state["chat_history"].append({"user_health_history": pdf_text})
            else:
                st.error(f"Error extracting text from file: {pdf_text}")

    user_input = st.text_input("Your message")

    st.markdown("<p style='font-size: small;'>Find the medicine advice, Diet Plan and fitness Plan based on uploaded report</p>", unsafe_allow_html=True)

    if user_input:
        # Combine all extracted texts
        combined_texts = " ".join(st.session_state["pdf_texts"])
        
        combined_input = combined_texts + " " + user_input

        if "medicine" in user_input.lower():
            ai_response = ML.generate_medicine_advice(combined_input)
        elif "diet" in user_input.lower():
            ai_response = ML.generate_diet_plan(combined_input)
        elif "fitness" in user_input.lower():
            ai_response = ML.generate_fitness_plan(combined_input)
        else:
            ai_response = ML.extract_health_info(combined_input)
        
        st.session_state["chat_history"].append({"user": user_input})
        st.session_state["chat_history"].append({"ai": ai_response})

    for chat in st.session_state.get("chat_history", []):
        if "user" in chat:
            st.markdown(f"<div style='text-align: right; font-weight: bold;'>User: {chat['user']}</div>", unsafe_allow_html=True)
        if "ai" in chat:
            st.markdown(f"<div style='text-align: left;'>AICopilotX: {chat['ai']}</div>", unsafe_allow_html=True)
