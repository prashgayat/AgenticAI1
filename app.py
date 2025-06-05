# app.py

import streamlit as st
from tools import search_jobs, evaluate_jobs, write_proposal, get_past_memory

st.set_page_config(page_title="Freelance AI Assistant", layout="wide")

st.title("🤖 Freelance Project Finder (Powered by CrewAI)")

# Input field for keywords
keywords = st.text_input("Enter search keywords (e.g., AI, chatbot, automation):", value="AI, chatbot")

# Start button
if st.button("🔍 Search Jobs"):
    with st.spinner("Searching and evaluating jobs..."):

        # Step 1: Search
        jobs = search_jobs(keywords)
        st.success(f"Found {len(jobs)} jobs.")

        # Step 2: Evaluate
        shortlisted = evaluate_jobs(jobs)
        st.info(f"{len(shortlisted)} jobs passed evaluation.")

        # Step 3: Show results
        for job in shortlisted:
            st.subheader(f"📌 {job['title']}")
            st.markdown(f"**Client:** {job['client']}  \n**Budget:** ${job['budget']}  \n**[View Job]({job['url']})**")

            # Step 4: Generate proposal
            with st.expander("✍️ View Auto-Generated Proposal"):
                proposal = write_proposal(job["title"])
                st.code(proposal, language="markdown")

    # Step 5: Memory (Optional)
    st.divider()
    st.subheader("🧠 Memory Summary (based on keyword 'AI')")
    st.markdown(get_past_memory("AI"))
