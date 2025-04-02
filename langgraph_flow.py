from langgraph.graph import StateGraph, END
from typing import TypedDict
from utils.model_utils import call_llm

# === Shared memory for the graph ===
class ResearchState(TypedDict):
    topic: str
    idea: str
    lit_review: str
    structure: str
    drafts: dict
    final: str

# === Step functions representing each agent ===
def idea_agent(state: ResearchState) -> ResearchState:
    topic = state.get("topic", "")
    prompt = f"""You are an academic research assistant helping to define a research project.

Based on the topic: "{topic}", generate the following:
- 2–3 possible research questions
- Suggested theoretical frameworks or perspectives
- Possible hypotheses or relationships
- Key concepts or variables involved
- Potential academic or practical contributions

Use clear, formal language.
"""
    idea = call_llm(prompt).strip()
    return {**state, "idea": idea}

def lit_review_agent(state: ResearchState) -> ResearchState:
    topic = state.get("topic", "")
    prompt = f"""You are an academic assistant. Summarize the current literature relevant to the topic: '{topic}' in 5–7 sentences."""
    lit_review = call_llm(prompt).strip()
    return {**state, "lit_review": lit_review}

def structure_agent(state: ResearchState) -> ResearchState:
    idea = state.get("idea", "")
    lit_review = state.get("lit_review", "")
    prompt = f"""Based on the following research idea and literature review, develop a detailed outline for a research paper.

Research Idea:
{idea}

Literature Review:
{lit_review}

The outline should include:
1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion
6. Conclusion

For each section, provide key points or subheadings that should be addressed.

Use clear, formal language.
"""
    structure = call_llm(prompt).strip()
    return {**state, "structure": structure}

def writing_agent(state: ResearchState) -> ResearchState:
    structure = state.get("structure", "")
    lit_review = state.get("lit_review", "")
    drafts = {}
    sections = ["Introduction", "Literature Review", "Methodology", "Results", "Discussion", "Conclusion"]
    for section in sections:
        prompt = f"""You are an academic research assistant tasked with drafting the '{section}' section of a research paper.

Based on the following structure and literature review:

Structure:
{structure}

Literature Review:
{lit_review}

Draft the '{section}' section with appropriate content and depth.

Use formal academic language.
"""
        draft = call_llm(prompt).strip()
        drafts[section] = draft
    return {**state, "drafts": drafts}

def refine_agent(state: ResearchState) -> ResearchState:
    drafts = state.get("drafts", {})
    refined_drafts = {}
    for section, content in drafts.items():
        prompt = f"""You are an academic editor. Please refine the following draft of the '{section}' section to improve clarity, coherence, and academic rigor.

Draft:
{content}

Provide the refined version below:
"""
        refined_draft = call_llm(prompt).strip()
        refined_drafts[section] = refined_draft
    return {**state, "drafts": refined_drafts}

def export_agent(state: ResearchState) -> ResearchState:
    final_text = "\n\n".join([f"{section}\n{content}" for section, content in state["drafts"].items()])
    return {**state, "final": final_text}

# === Build LangGraph ===
workflow = StateGraph(ResearchState)

workflow.add_node("IdeaAgent", idea_agent)
workflow.add_node("LitReviewAgent", lit_review_agent)
workflow.add_node("StructureAgent", structure_agent)
workflow.add_node("WritingAgent", writing_agent)
workflow.add_node("RefineAgent", refine_agent)
workflow.add_node("ExportAgent", export_agent)

workflow.set_entry_point("IdeaAgent")
workflow.add_edge("IdeaAgent", "LitReviewAgent")
workflow.add_edge("LitReviewAgent", "StructureAgent")
workflow.add_edge("StructureAgent", "WritingAgent")
workflow.add_edge("WritingAgent", "RefineAgent")
workflow.add_edge("RefineAgent", "ExportAgent")
workflow.add_edge("ExportAgent", END)

# === Compile the flow ===
research_graph = workflow.compile()

if __name__ == "__main__":
    initial_state = ResearchState(topic="Social Media and Consumer Trust")
    final_state = research_graph.invoke(initial_state)
    print("\n=== Final Output ===")
    print(final_state["final"])
