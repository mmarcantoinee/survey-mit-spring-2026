import os
import shutil
import csv
import hashlib

github_username = "mmarcantoinee" 
repo_name = "survey-mit-spring-2026"

base_original = r"./images/original"
base_renamed = r"./images/renamed"

conditions = ["visual_complex", "visual_scrambled"]

csv_data = [["Original_Filename", "Anonymized_Filename", "Condition", "GitHub_URL"]]

print("Starting idempotent anonymization and copy process...")

for condition in conditions:
    orig_path = os.path.join(base_original, condition)
    renamed_path = os.path.join(base_renamed, condition)
    
    os.makedirs(renamed_path, exist_ok=True)
    
    if not os.path.exists(orig_path):
        print(f"Warning: Could not find folder {orig_path}")
        continue

    for filename in os.listdir(orig_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            ext = os.path.splitext(filename)[1]
            
            # Generate a deterministic hash based on the original filename
            # Adding the condition to the encode ensures files with the same name 
            # in different folders get unique hashes
            unique_string = f"{condition}_{filename}"
            anon_id = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:8]
            anon_filename = f"{anon_id}{ext}"
            
            src_file = os.path.join(orig_path, filename)
            dst_file = os.path.join(renamed_path, anon_filename)
            
            # Copy the file (will safely overwrite if it already exists)
            shutil.copy2(src_file, dst_file)
            
            github_url = f"https://{github_username}.github.io/{repo_name}/images/renamed/{condition}/{anon_filename}"
            csv_data.append([filename, anon_filename, condition, github_url])

csv_filename = "survey_image_mapping.csv"
with open(csv_filename, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print(f"Success! Operation complete. Data saved to {csv_filename}")