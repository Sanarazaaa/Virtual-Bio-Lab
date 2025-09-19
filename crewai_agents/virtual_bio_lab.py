from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileReadTool
import json
import pandas as pd
from datetime import datetime
#from langchain_google_genai import ChatGoogleGenerativeAI
import os  # Add this import
from crewai import LLM

# Define the agents for your virtual biology lab

# 1. Protocol Reader Agent - Understands experiment procedures
protocol_reader = Agent(
    role='Protocol Reader',
    goal='Read and understand experimental protocols, extract key parameters and steps',
    backstory="""You are an experienced lab technician who specializes in reading and 
    interpreting biological experiment protocols. You can break down complex procedures 
    into clear, actionable steps and identify all necessary materials and conditions.""",
    verbose=True,
    allow_delegation=False,
    tools=[FileReadTool()],  # Can read protocol files
    # Change from default (OpenAI) to Gemini
    llm=LLM(model="gemini/gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
)

# 2. Virtual Experimenter Agent - Simulates running experiments
virtual_experimenter = Agent(
    role='Virtual Experimenter',
    goal='Simulate biological experiments using historical data and established patterns',
    backstory="""You are a skilled researcher who can predict experimental outcomes 
    based on existing scientific literature and data. You understand how different 
    variables affect biological systems and can generate realistic experimental results.""",
    verbose=True,
    allow_delegation=False,
    tools=[SerperDevTool()],  # Can search for relevant biological data
    # Change from default (OpenAI) to Gemini
    llm=LLM(model="gemini/gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
)

# 3. Data Collector Agent - Organizes experimental data
data_collector = Agent(
    role='Data Collector',
    goal='Collect, organize, and structure experimental data in a systematic way',
    backstory="""You are a meticulous data manager who ensures all experimental 
    observations are properly recorded, organized, and formatted for analysis. 
    You maintain data integrity and follow scientific data management standards.""",
    verbose=True,
    allow_delegation=False,
    # Change from default (OpenAI) to Gemini
    llm=LLM(model="gemini/gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
)

# 4. Data Analyst Agent - Analyzes results and creates visualizations
data_analyst = Agent(
    role='Data Analyst',
    goal='Analyze experimental data, perform statistical tests, and create meaningful visualizations',
    backstory="""You are a bioinformatician with expertise in statistical analysis 
    and data visualization. You can identify patterns, calculate significance, 
    and present findings through clear graphs and charts.""",
    verbose=True,
    allow_delegation=False,
    # Change from default (OpenAI) to Gemini
    llm=LLM(model="gemini/gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
)

# 5. Report Writer Agent - Creates reports and suggests next steps
report_writer = Agent(
    role='Report Writer',
    goal='Write comprehensive experiment reports and suggest future research directions',
    backstory="""You are a scientific writer who can synthesize experimental results 
    into clear, professional reports. You understand scientific methodology and 
    can suggest logical next steps based on current findings.""",
    verbose=True,
    allow_delegation=False,
    # Change from default (OpenAI) to Gemini
    llm=LLM(model="gemini/gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
)

# Define tasks for each agent
def create_experiment_tasks(experiment_description, protocol_file=None):
    
    # Task 1: Read and understand protocol
    protocol_task = Task(
        description=f"""
        Read and analyze the following experiment: {experiment_description}
        
        Extract and organize:
        - Objective of the experiment
        - Required materials and reagents
        - Step-by-step procedure
        - Expected timeline
        - Critical parameters (temperature, pH, concentrations, etc.)
        - Safety considerations
        
        Present this information in a structured format that other agents can easily follow.
        """,
        agent=protocol_reader,
        expected_output="A structured breakdown of the experimental protocol with all key details organized"
    )
    
    # Task 2: Simulate experiment execution
    experiment_task = Task(
        description="""
        Based on the protocol analysis, simulate running this biological experiment:
        
        - Generate realistic data points based on the experimental conditions
        - Consider biological variability and potential experimental errors
        - Include appropriate controls and replicates
        - Account for time-dependent changes if applicable
        - Generate raw data in a format suitable for analysis
        
        Use your knowledge of biological systems to create plausible results.
        """,
        agent=virtual_experimenter,
        expected_output="Simulated experimental data with realistic biological measurements and observations"
    )
    
    # Task 3: Collect and organize data
    collection_task = Task(
        description="""
        Take the simulated experimental data and organize it systematically:
        
        - Structure data in appropriate formats (tables, matrices)
        - Add metadata (timestamps, conditions, sample IDs)
        - Ensure data quality and consistency
        - Create data dictionaries explaining variables
        - Organize files in a logical directory structure
        
        Prepare the data for statistical analysis.
        """,
        agent=data_collector,
        expected_output="Well-organized dataset with proper structure, labels, and metadata"
    )
    
    # Task 4: Analyze data and create visualizations
    analysis_task = Task(
        description="""
        Perform comprehensive analysis of the experimental data:
        
        - Calculate descriptive statistics
        - Perform appropriate statistical tests
        - Identify significant patterns or differences
        - Create informative visualizations (bar charts, line graphs, heatmaps)
        - Generate figures with proper labels and legends
        - Assess data quality and potential outliers
        
        Present findings in a clear, scientific manner.
        """,
        agent=data_analyst,
        expected_output="Statistical analysis results with publication-quality figures and interpretation"
    )
    
    # Task 5: Write report and suggest next steps
    report_task = Task(
        description="""
        Create a comprehensive experiment report including:
        
        - Executive summary of findings
        - Methods section (based on protocol)
        - Results section (incorporating analysis and figures)
        - Discussion of biological significance
        - Limitations of the virtual experiment
        - Specific recommendations for next experiments
        - Suggestions for protocol improvements
        
        Write in standard scientific report format.
        """,
        agent=report_writer,
        expected_output="Complete scientific report with conclusions and actionable next steps"
    )
    
    return [protocol_task, experiment_task, collection_task, analysis_task, report_task]

# Create the crew (your virtual lab team)
def create_virtual_lab_crew(experiment_description, protocol_file=None):
    tasks = create_experiment_tasks(experiment_description, protocol_file)
    
    crew = Crew(
        agents=[protocol_reader, virtual_experimenter, data_collector, data_analyst, report_writer],
        tasks=tasks,
        process=Process.sequential,  # Tasks run in order
    )
    
    return crew

# Example usage function
def run_virtual_experiment(experiment_description):
    """
    Run a complete virtual biology experiment
    
    Args:
        experiment_description (str): Description of the experiment to run
    
    Returns:
        dict: Complete results including all agent outputs
    """
    
    print("🧪 Starting Virtual Biology Lab Experiment...")
    print(f"Experiment: {experiment_description}")
    print("-" * 50)
    
    # Create the crew
    lab_crew = create_virtual_lab_crew(experiment_description)
    
    # Run the experiment
    try:
        result = lab_crew.kickoff()
        
        print("✅ Virtual experiment completed successfully!")
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "experiment": experiment_description,
            "results": result
        }
        
    except Exception as e:
        print(f"❌ Experiment failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Example experiment scenarios
EXAMPLE_EXPERIMENTS = {
    "protein_expression": """
    Test the effect of different IPTG concentrations (0.1mM, 0.5mM, 1.0mM) on 
    recombinant protein expression in E. coli BL21(DE3) cells over 4 hours at 37°C.
    Measure protein levels using SDS-PAGE and Western blot.
    """,
    
    "cell_viability": """
    Evaluate the cytotoxicity of a new compound on HeLa cells using MTT assay.
    Test concentrations: 1µM, 10µM, 50µM, 100µM, 500µM over 24 and 48 hours.
    Include DMSO vehicle control.
    """,
    
    "enzyme_kinetics": """
    Determine Km and Vmax values for β-galactosidase using ONPG as substrate.
    Test substrate concentrations from 0.1 to 10 mM. Measure absorbance at 420nm 
    every 30 seconds for 10 minutes at 37°C, pH 7.0.
    """
}

# Main execution
if __name__ == "__main__":
    # Example: Run a protein expression experiment
    experiment = EXAMPLE_EXPERIMENTS["protein_expression"]
    results = run_virtual_experiment(experiment)
    
    # Save results
    with open(f"virtual_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n📊 Results saved to file!")