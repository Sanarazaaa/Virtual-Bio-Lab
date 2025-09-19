from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# This should run without errors if everything is installed correctly
llm = ChatGoogleGenerativeAI(model="gemini-pro")
print("Installation successful!")