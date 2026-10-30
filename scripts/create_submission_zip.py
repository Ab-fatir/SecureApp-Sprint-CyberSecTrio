import os
import zipfile

def create_zip(zip_filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    exclude_dirs = {".git", "__pycache__", ".pytest_cache", "demo_build", "instance"}
    exclude_extensions = {".pyc", ".pyo"}
    exclude_files = {zip_filename, "SecureApp-Sprint-CyberSecTrio.zip"}

    print(f"[*] Packaging submission archive: {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in exclude_extensions):
                    continue
                if file in exclude_files:
                    continue
                if file == "cloudvault.db":
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zipf.write(full_path, rel_path)

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"[+] Archive created successfully: {zip_filename} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    primary_zip = "CYC386_Midterm_Sprint_FA23-BCT-029_FA23-BCT-034_FA23-BCT-054.zip"
    create_zip(primary_zip)
    
    alias_zip = "SecureApp-Sprint-CyberSecTrio.zip"
    import shutil
    shutil.copyfile(primary_zip, alias_zip)
    print(f"[+] Created copy: {alias_zip}")

