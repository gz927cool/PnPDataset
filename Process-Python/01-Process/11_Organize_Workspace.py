import os
import shutil

# Paths
base_dir = r"c:\Users\001\Desktop\list"
enrich_dir = os.path.join(base_dir, "04-Enrich")
python_dir = os.path.join(base_dir, "99-Python")
archive_dir = os.path.join(python_dir, "Archive")

def rename_enrich_files():
    print("--- Renaming 04-Enrich files ---")
    for filename in os.listdir(enrich_dir):
        if filename.endswith(".csv") and not filename.endswith("_refined.csv"):
            old_path = os.path.join(enrich_dir, filename)
            new_name = filename.replace(".csv", "_refined.csv")
            new_path = os.path.join(enrich_dir, new_name)
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")
            except Exception as e:
                print(f"Error renaming {filename}: {e}")

def organize_python_scripts():
    print("\n--- Organizing 99-Python scripts ---")
    
    # Create Archive folder if not exists
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Created Archive directory: {archive_dir}")

    # 1. Move old/exploratory scripts to Archive
    # We'll assume Steps 1-12 are archival
    for filename in os.listdir(python_dir):
        if filename.startswith("Step") and filename.endswith(".py"):
            # Extract step number
            try:
                step_num = int(filename.split('_')[0].replace("Step", ""))
                if step_num < 13:
                    old_path = os.path.join(python_dir, filename)
                    new_path = os.path.join(archive_dir, filename)
                    shutil.move(old_path, new_path)
                    print(f"Archived: {filename}")
            except ValueError:
                pass # Not a standard StepXX file
        elif filename.endswith(".txt"): # Archive text reports too
             old_path = os.path.join(python_dir, filename)
             new_path = os.path.join(archive_dir, filename)
             shutil.move(old_path, new_path)
             print(f"Archived: {filename}")

    # 2. Rename the active revision scripts to a clean sequence
    # Mapping of old names to new descriptive names
    rename_map = {
        "Step13_apply_cidoc_all.py": "01_Apply_Initial_CIDOC.py",
        "Step14_update_enrich_unknowns.py": "02_Update_Specific_Unknowns.py",
        "Step15_finalize_unknowns.py": "03_Finalize_Unknown_Classification.py",
        "Step16_fix_quoted_unknowns.py": "04_Fix_Quoted_Terms.py",
        "Step17_fix_mismatches.py": "05_Fix_Type_Mismatches.py"
    }

    for old_name, new_name in rename_map.items():
        old_path = os.path.join(python_dir, old_name)
        new_path = os.path.join(python_dir, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"Renamed Script: {old_name} -> {new_name}")
        else:
            print(f"Warning: Could not find {old_name}")

if __name__ == "__main__":
    rename_enrich_files()
    organize_python_scripts()
