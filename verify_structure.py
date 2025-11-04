"""
Script to verify the Strata project structure
"""
import os

def verify_file_exists(filepath):
    """Verify that a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {filepath}")
        return True
    else:
        print(f"✗ {filepath} (MISSING)")
        return False

def main():
    print("Verifying Strata project structure...")
    print("=" * 50)
    
    # Required files and directories
    required_paths = [
        # Root files
        "README.md",
        "requirements.txt",
        "main.py",
        "strata.py",
        ".gitignore",
        "start.sh",
        "start.bat",
        "replit.nix",
        ".replit",
        
        # Backend files
        "backend/__init__.py",
        "backend/main.py",
        "backend/database.py",
        "backend/models.py",
        "backend/ai.py",
        "backend/requirements.txt",
        
        # Backend routes
        "backend/routes/__init__.py",
        "backend/routes/connections.py",
        "backend/routes/session.py",
        "backend/routes/analyze.py",
        "backend/routes/extract.py",
        "backend/routes/migrate.py",
        "backend/routes/validate.py",
        "backend/routes/export_routes.py",
        "backend/routes/reset.py",
        
        # Frontend files
        "frontend/package.json",
        "frontend/index.html",
        "frontend/tsconfig.json",
        "frontend/tsconfig.node.json",
        "frontend/vite.config.ts",
        "frontend/tailwind.config.js",
        "frontend/postcss.config.js",
        
        # Frontend source files
        "frontend/src/main.tsx",
        "frontend/src/App.tsx",
        "frontend/src/index.css",
        "frontend/src/types.ts",
        
        # Frontend components
        "frontend/src/components/Sidebar.tsx",
        "frontend/src/components/TopBar.tsx",
        "frontend/src/components/AddConnectionModal.tsx",
        
        # Frontend pages
        "frontend/src/pages/Analyze.tsx",
        "frontend/src/pages/Extract.tsx",
        "frontend/src/pages/Migrate.tsx",
        "frontend/src/pages/Reconcile.tsx",
        
        # Frontend assets
        "frontend/src/assets/logo.svg",
    ]
    
    all_present = True
    for path in required_paths:
        if not verify_file_exists(path):
            all_present = False
    
    print("\n" + "=" * 50)
    if all_present:
        print("🎉 All required files are present!")
        print("The Strata project structure is complete.")
    else:
        print("⚠️  Some required files are missing!")
        print("Please check the project structure.")
    
    return all_present

if __name__ == "__main__":
    main()