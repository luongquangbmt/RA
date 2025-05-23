import streamlit as st
from langgraph_flow import research_graph, ResearchState


# === Display user email and logout/reset ===
if "user_email" not in st.session_state or not st.session_state.user_email:
    st.warning("Please return to the homepage and enter your email to start.")
    st.stop()

with st.sidebar:
    st.markdown(f"👤 **Logged in as:** `{st.session_state.user_email}`")
    if st.button("🔁 Log out / Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
st.title("🔁 LangGraph Research Flow Runner")
st.markdown("This runs the full agent workflow: Idea → LitReview → Structure → Writing → Refine → Export")

# Step 1: Topic input
topic = st.text_input("Enter your research topic:")
run = st.button("🚀 Run Full Pipeline")

if run and topic:
    with st.spinner("Running LangGraph agent pipeline..."):
        # Create initial state
        initial_state = ResearchState(topic=topic)
        final_state = research_graph.invoke(initial_state)

        # Save to session state for other agents to access
        st.session_state.research_idea = {
            "topic": topic,
            "output": final_state.get("idea", "")
        }
        st.session_state.structure_plan = final_state.get("structure", "")
        st.session_state.drafts = final_state.get("drafts", {})

        # Display results
        st.success("✅ Research flow completed!")
        st.markdown("### 📄 Final Output")
        st.text_area("Complete Document: ", value=final_state.get("final", ""), height=300)

        st.markdown("---")
        st.markdown("### 📃 Section Drafts")
        for section, content in final_state.get("drafts", {}).items():
            st.markdown(f"**{section}**")
            st.text_area(label="", value=content, height=200, key=section)
