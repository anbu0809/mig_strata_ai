"""
Test script for Strata CLI tool
"""
import subprocess
import sys

def test_cli_help():
    """Test that the CLI tool shows help"""
    print("Testing CLI help command...")
    result = subprocess.run([sys.executable, "strata.py", "--help"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0 and "usage:" in result.stdout:
        print("✓ CLI help command works")
        return True
    else:
        print("✗ CLI help command failed")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        return False

def test_cli_commands():
    """Test that CLI commands are recognized"""
    print("Testing CLI commands...")
    
    commands = ["setup", "start", "status", "test", "deploy", "reset"]
    
    for command in commands:
        result = subprocess.run([sys.executable, "strata.py", command, "--help"], 
                              capture_output=True, text=True)
        
        # We expect these to show help rather than execute
        if "usage:" in result.stdout or "help" in result.stdout:
            print(f"✓ CLI command '{command}' recognized")
        else:
            print(f"✗ CLI command '{command}' not recognized")
            return False
    
    return True

def main():
    print("Testing Strata CLI tool")
    print("=" * 30)
    
    success = True
    success &= test_cli_help()
    success &= test_cli_commands()
    
    print("\n" + "=" * 30)
    if success:
        print("🎉 All CLI tests passed!")
    else:
        print("❌ Some CLI tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)