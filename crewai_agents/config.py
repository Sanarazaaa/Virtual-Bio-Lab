# config.py - Configuration for Virtual Biology Lab

import os
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class LabConfig:
    """Configuration settings for the virtual biology lab"""
    
    # API Keys (set these as environment variables)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")  # For web searches
    
    # Lab settings
    LAB_NAME: str = "Virtual BioLab AI"
    MAX_EXPERIMENT_TIME: int = 3600  # Maximum time in seconds
    DEFAULT_TEMPERATURE: float = 25.0  # Default lab temperature in Celsius
    
    # Data storage
    DATA_DIR: str = "./experiment_data"
    RESULTS_DIR: str = "./results"
    PROTOCOLS_DIR: str = "./protocols"
    
    # Agent behavior settings
    AGENT_VERBOSE: bool = True
    USE_MEMORY: bool = True
    MAX_ITERATIONS: int = 5

# Equipment database for realistic simulation
VIRTUAL_EQUIPMENT = {
    "spectrophotometer": {
        "wavelength_range": "200-800nm",
        "accuracy": "±1nm",
        "capabilities": ["absorbance", "transmittance", "kinetics"]
    },
    "pcr_machine": {
        "temp_range": "4-100°C",
        "accuracy": "±0.1°C",
        "capabilities": ["pcr", "qpcr", "melting_curves"]
    },
    "centrifuge": {
        "max_speed": "15000rpm",
        "temp_range": "4-40°C",
        "capabilities": ["cell_pelleting", "protein_purification"]
    },
    "incubator": {
        "temp_range": "15-70°C",
        "humidity_control": True,
        "co2_control": True,
        "capabilities": ["cell_culture", "bacterial_growth"]
    },
    "microscope": {
        "magnification": "40x-1000x",
        "illumination": ["brightfield", "fluorescence"],
        "capabilities": ["cell_counting", "morphology", "live_imaging"]
    }
}

# Common reagent database with properties
REAGENT_DATABASE = {
    "IPTG": {
        "molecular_weight": 238.3,
        "solubility": "water",
        "storage_temp": -20,
        "function": "protein_expression_inducer"
    },
    "DMSO": {
        "molecular_weight": 78.13,
        "solubility": "universal",
        "storage_temp": 25,
        "function": "solvent"
    },
    "MTT": {
        "molecular_weight": 414.32,
        "solubility": "water",
        "storage_temp": -20,
        "function": "viability_dye"
    },
    "ONPG": {
        "molecular_weight": 301.25,
        "solubility": "water",
        "storage_temp": -20,
        "function": "enzyme_substrate"
    }
}

# Biological data templates for realistic simulation
BIOLOGICAL_TEMPLATES = {
    "protein_expression": {
        "baseline_expression": 0.1,
        "max_expression": 10.0,
        "ec50_iptg": 0.5,  # mM
        "hill_coefficient": 2.0,
        "variability": 0.15
    },
    "cell_viability": {
        "control_viability": 100.0,
        "max_kill": 95.0,
        "ic50_range": [10, 100],  # μM
        "hill_coefficient": 1.5,
        "variability": 0.1
    },
    "enzyme_kinetics": {
        "km_range": [0.5, 5.0],  # mM
        "vmax_range": [1.0, 10.0],  # μmol/min/mg
        "variability": 0.08
    }
}

# Installation and setup instructions
SETUP_INSTRUCTIONS = """
🧬 Virtual Biology Lab Setup Instructions

1. Install Required Packages:
   pip install crewai crewai-tools pandas matplotlib seaborn numpy scipy

2. Set Environment Variables:
   export GOOGLE_API_KEY="https://aistudio.google.com/app/apikey"
   export SERPER_API_KEY=""  # Optional for web search

3. Create Directory Structure:
   mkdir experiment_data results protocols

4. API Key Setup:
   - Get Gemini API key from 
   - Get Serper API key from https://serper.dev/ (for web searches)

5. Test Installation:
   python virtual_bio_lab.py

6. Customize Your Lab:
   - Modify BIOLOGICAL_TEMPLATES for your specific experiments
   - Add new equipment to VIRTUAL_EQUIPMENT
   - Update REAGENT_DATABASE with your compounds

🔬 Usage Examples:

# Quick test
from virtual_bio_lab import run_virtual_experiment
results = run_virtual_experiment("Test antibiotic resistance in E. coli")

# Custom experiment
experiment = '''
Test the effect of caffeine on yeast cell growth.
Use concentrations: 0, 1, 5, 10, 50 mM caffeine.
Measure OD600 every hour for 12 hours at 30°C.
'''
results = run_virtual_experiment(experiment)
"""

# Validation functions
def validate_setup():
    """Check if the virtual lab is properly configured"""
    issues = []
    
    if not os.getenv("GOOGLE_API_KEY"):
        issues.append("❌ GOOGLE_API_KEY not set")
    else:
        issues.append("✅ Google API key configured")
    
    # Check directories
    for directory in ["experiment_data", "results", "protocols"]:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                issues.append(f"✅ Created directory: {directory}")
            except Exception as e:
                issues.append(f"❌ Could not create {directory}: {e}")
        else:
            issues.append(f"✅ Directory exists: {directory}")
    
    # Check Python packages
    required_packages = ["crewai", "pandas", "matplotlib"]
    for package in required_packages:
        try:
            __import__(package)
            issues.append(f"✅ {package} installed")
        except ImportError:
            issues.append(f"❌ {package} not installed")
    
    print("🔍 Virtual Lab Setup Check:")
    print("-" * 40)
    for issue in issues:
        print(issue)
    
    return "❌" not in str(issues)

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
    print("\n" + "="*50)
    validate_setup()