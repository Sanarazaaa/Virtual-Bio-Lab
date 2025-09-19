# example_experiments.py - Ready-to-run virtual biology experiments

from virtual_bio_lab import run_virtual_experiment
import json
from datetime import datetime

class VirtualLabExperiments:
    """Collection of pre-designed virtual biology experiments"""
    
    def __init__(self):
        self.experiment_library = {
            "drug_screening": self.drug_screening_experiment,
            "protein_purification": self.protein_purification_experiment,
            "pcr_optimization": self.pcr_optimization_experiment,
            "cell_counting": self.cell_counting_experiment,
            "ph_optimization": self.ph_optimization_experiment
        }
    
    def drug_screening_experiment(self):
        """Virtual drug screening on cancer cells"""
        return """
        Screen potential anticancer compound XYZ-123 on HeLa cells:
        
        Experimental Design:
        - Cell line: HeLa (cervical cancer)
        - Compound concentrations: 0.1, 1, 10, 50, 100, 500 μM
        - Controls: DMSO vehicle control, Doxorubicin positive control (10 μM)
        - Assay: MTT viability assay
        - Time points: 24h and 48h treatment
        - Replicates: n=6 per condition
        
        Measurements:
        - Cell viability percentage
        - IC50 calculation
        - Statistical analysis (ANOVA)
        - Dose-response curves
        
        Expected deliverables:
        - IC50 values at both time points
        - Dose-response graphs
        - Statistical significance testing
        - Recommendations for follow-up concentrations
        """
    
    def protein_purification_experiment(self):
        """Virtual protein purification workflow"""
        return """
        Purify His-tagged recombinant protein from E. coli:
        
        Experimental Steps:
        1. Bacterial lysis (sonication buffer: 50mM Tris pH 7.5, 300mM NaCl)
        2. Centrifugation (12,000g, 30min, 4°C)
        3. Ni-NTA column purification
        4. Wash steps (20mM imidazole)
        5. Elution (250mM imidazole)
        6. Buffer exchange (dialysis to PBS)
        
        Analysis:
        - SDS-PAGE at each step
        - Bradford assay for protein concentration
        - Western blot confirmation
        - Activity assay (if enzyme)
        
        Calculate:
        - Protein yield at each step
        - Purification fold
        - Recovery percentage
        - Purity assessment
        """
    
    def pcr_optimization_experiment(self):
        """Virtual PCR optimization experiment"""
        return """
        Optimize PCR conditions for amplifying 1.2 kb gene fragment:
        
        Variables to test:
        - Annealing temperatures: 50°C, 55°C, 60°C, 65°C
        - MgCl2 concentrations: 1.5mM, 2.0mM, 2.5mM, 3.0mM
        - Primer concentrations: 0.2μM, 0.5μM, 1.0μM
        
        PCR Protocol:
        - Initial denaturation: 95°C, 5min
        - 35 cycles: 95°C 30s, variable temp 30s, 72°C 90s
        - Final extension: 72°C, 10min
        
        Analysis:
        - Agarose gel electrophoresis (1% gel)
        - Band intensity measurement
        - Product size verification
        - Optimization matrix analysis
        
        Output: Recommended optimal conditions
        """
    
    def cell_counting_experiment(self):
        """Virtual cell growth and counting experiment"""
        return """
        Monitor bacterial growth under different nutrient conditions:
        
        Media conditions:
        - Rich media (LB broth)
        - Minimal media (M9 + glucose)
        - Minimal media + amino acids
        - Minimal media + vitamins
        - Nutrient-limited media
        
        Measurements:
        - OD600 every 2 hours for 24 hours
        - Viable cell counts (CFU/ml) at 8h, 16h, 24h
        - pH measurements
        
        Calculations:
        - Growth rates (doubling time)
        - Maximum cell density
        - Lag time analysis
        - Statistical comparison between conditions
        
        Deliverables:
        - Growth curves for each condition
        - Growth parameter table
        - Recommendations for optimal medium
        """
    
    def ph_optimization_experiment(self):
        """Virtual enzyme activity pH optimization"""
        return """
        Determine optimal pH for enzyme activity:
        
        Enzyme: β-galactosidase
        pH range: 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0
        
        Buffer systems:
        - pH 5.0-6.0: Acetate buffer (50mM)
        - pH 6.5-7.5: Phosphate buffer (50mM)
        - pH 8.0-9.0: Tris buffer (50mM)
        
        Assay conditions:
        - Substrate: ONPG (2mM)
        - Enzyme concentration: 10 μg/ml
        - Temperature: 37°C
        - Reaction time: 10 minutes
        - Detection: A420nm
        
        Analysis:
        - Activity vs pH curve
        - Optimal pH determination
        - Buffer compatibility assessment
        - Temperature stability at optimal pH
        """
    
    def run_experiment(self, experiment_name, save_results=True):
        """Run a specific experiment from the library"""
        
        if experiment_name not in self.experiment_library:
            print(f"❌ Experiment '{experiment_name}' not found!")
            print(f"Available experiments: {list(self.experiment_library.keys())}")
            return None
        
        print(f"🧪 Running {experiment_name.replace('_', ' ').title()}")
        print("=" * 60)
        
        # Get experiment description
        experiment_description = self.experiment_library[experiment_name]()
        
        # Run the virtual experiment
        results = run_virtual_experiment(experiment_description)
        
        if save_results and results["status"] == "success":
            filename = f"{experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(f"./results/{filename}", "w") as f:
                json.dump(results, f, indent=2)
            print(f"📁 Results saved to: ./results/{filename}")
        
        return results
    
    def list_experiments(self):
        """List all available experiments"""
        print("🔬 Available Virtual Experiments:")
        print("-" * 40)
        for i, (name, func) in enumerate(self.experiment_library.items(), 1):
            title = name.replace('_', ' ').title()
            print(f"{i}. {title}")
            # Get first line of description
            description = func().split('\n')[1].strip()
            print(f"   {description}")
            print()
    
    def run_all_experiments(self):
        """Run all experiments in the library"""
        print("🚀 Running All Virtual Experiments")
        print("=" * 50)
        
        results = {}
        for exp_name in self.experiment_library.keys():
            print(f"\n▶️ Starting {exp_name}...")
            result = self.run_experiment(exp_name, save_results=True)
            results[exp_name] = result
            
            if result["status"] == "success":
                print(f"✅ {exp_name} completed successfully")
            else:
                print(f"❌ {exp_name} failed: {result.get('error', 'Unknown error')}")
        
        return results

# Interactive experiment runner
def interactive_lab():
    """Interactive mode for running virtual experiments"""
    lab = VirtualLabExperiments()
    
    print("🧬 Welcome to the Virtual Biology Lab!")
    print("Type 'help' for commands or 'quit' to exit")
    
    while True:
        command = input("\nVirtual Lab > ").strip().lower()
        
        if command == 'quit' or command == 'exit':
            print("👋 Thanks for using Virtual Biology Lab!")
            break
        elif command == 'help':
            print("\nAvailable commands:")
            print("- 'list': Show all available experiments")
            print("- 'run <experiment_name>': Run specific experiment")
            print("- 'run_all': Run all experiments")
            print("- 'custom': Run a custom experiment")
            print("- 'quit': Exit the lab")
        elif command == 'list':
            lab.list_experiments()
        elif command.startswith('run '):
            exp_name = command[4:].strip()
            lab.run_experiment(exp_name)
        elif command == 'run_all':
            lab.run_all_experiments()
        elif command == 'custom':
            print("Enter your custom experiment description:")
            custom_exp = input("Experiment > ")
            if custom_exp.strip():
                results = run_virtual_experiment(custom_exp)
                print("Custom experiment completed!")
        else:
            print("Unknown command. Type 'help' for available commands.")

# Example usage
if __name__ == "__main__":
    # Create lab instance
    virtual_lab = VirtualLabExperiments()
    
    # Option 1: List all experiments
    virtual_lab.list_experiments()
    
    # Option 2: Run a specific experiment
    results = virtual_lab.run_experiment("drug_screening")
    
    # Option 3: Interactive mode
    # interactive_lab()
    
    # Option 4: Run all experiments
    # all_results = virtual_lab.run_all_experiments()