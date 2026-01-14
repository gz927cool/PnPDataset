import argparse
from src.pipeline.runner import PipelineRunner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", nargs="+", type=int, help="Steps to run (0-6)")
    parser.add_argument("--limit", type=int, help="Limit number of records to process")
    args = parser.parse_args()

    PipelineRunner().run(steps=args.steps, limit=args.limit)

if __name__ == "__main__":
    main()
