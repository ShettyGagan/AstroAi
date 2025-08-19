# llm_chain.py
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import os

# Import the knowledge base
from knowledge import VEDIC_KNOWLEDGE_BASE

class AstroChain:
    def __init__(self, chart_data, aspects, api_key=None):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0.7,
            api_key=api_key or os.getenv("GROQ_API_KEY")
        )
        self.memory = ConversationBufferMemory()
        
        # Build the structured context for the LLM
        self.chart_context = self.build_chart_context(chart_data, aspects)

    def build_chart_context(self, placements, aspects):
        
        
        # 1. Retrieving relevant knowledge from the knowledge base
        knowledge_snippets = "--- Relevant Vedic Interpretations ---\n"
        for body in ["Ascendant", "Sun", "Moon"]:
            if body in placements:
                sign = placements[body]['sign']
                try:
                    snippet = VEDIC_KNOWLEDGE_BASE[body][sign]
                    knowledge_snippets += f"*{body} in {sign}:* {snippet}\n\n"
                except KeyError:
                    # Handle cases where a planet-sign combo might not be in the KB
                    knowledge_snippets += f"*{body} in {sign}:* No specific interpretation found in knowledge base.\n\n"

        placement_summary = "--- Natal Chart Placements (Sidereal Lahiri) ---\n"
        for name, data in placements.items():
            placement_summary += f"- {name}: {data['degree_str']} {data['sign']} (in House {data['house']})\n"

       
        aspect_summary = "--- Major Planetary Aspects ---\n"
        if aspects:
            for aspect in aspects:
                p1, p2 = aspect['planets']
                aspect_summary += f"- {p1} {aspect['type']} {p2} (Orb: {aspect['orb']}°)\n"
        else:
            aspect_summary += "No major aspects found.\n"

        return f"{knowledge_snippets}\n{placement_summary}\n{aspect_summary}"

    def predict(self, user_input):
        
        prompt = f"""
You are 'AstroGuide AI', a profound, wise, and empathetic astrologer specializing in Vedic (Sidereal/Lahiri) astrology.
Your task is to synthesize the user's chart data into a holistic and insightful narrative.

**Your Guiding Principles:**
1.  **Ground in Data:** Base your interpretation on the "Relevant Vedic Interpretations".
2.  **Synthesize, Don't List:** Weave the placements, houses, and aspects together.
3.  **BE EXTREMELY CONCISE:** This is the most important instruction. Provide a summary in **no more than three short paragraphs.** Focus only on the most critical information about the person's core nature, strengths, and challenges.
4.  **Be Compassionate and Empowering:** Frame challenges as opportunities for growth.

**USER'S CHART CONTEXT:**
{self.chart_context}

**CONVERSATION HISTORY:**
{self.memory.load_memory_variables({})['history']}

**USER'S QUESTION:**
Human: {user_input}

**Your Astrological Synthesis:**
AI:"""
        
        response = self.llm.invoke(prompt).content
        self.memory.save_context({"input": user_input}, {"output": response})
        return response