import argparse
from src.pipeline.step0_preprocess import Step0Preprocessor
from src.pipeline.step2_candidates import Step2CandidateGenerator
from src.pipeline.step3_relations import Step3RelationMapper
from src.pipeline.step4_disambiguation import Step4Aligner
from src.pipeline.step5_facts import Step5FactGenerator
from src.pipeline.step6_graph import Step6GraphBuilder

class PipelineRunner:
    def run(self, steps=None, limit=None):
        if steps is None:
            steps = [0, 2, 3, 4, 5, 6]
            
        print(f"Starting Knowledge Graph Construction Pipeline... (Steps: {steps}, Limit: {limit})")
        
        if 0 in steps:
            Step0Preprocessor().run(limit=limit)
        if 2 in steps:
            Step2CandidateGenerator().run()
        if 3 in steps:
            Step3RelationMapper().run()
        if 4 in steps:
            Step4Aligner().run()
        if 5 in steps:
            Step5FactGenerator().run()
        if 6 in steps:
            Step6GraphBuilder().run()
            
        print("Pipeline completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", nargs="+", type=int, help="Steps to run (0-6)")
    parser.add_argument("--limit", type=int, help="Limit number of records to process in Step 0")
    args = parser.parse_args()
    
    PipelineRunner().run(steps=args.steps, limit=args.limit)
