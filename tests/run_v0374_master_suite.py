import subprocess
import sys

def main():
    test_files = [
        "tests/test_checkpoint_a_v0374.py",
        "tests/test_submit_v0374.py",
        "tests/test_navigation_v0374.py",
        "tests/test_shortcuts_v0374.py"
    ]
    
    print("===============================================================")
    print("SOCIAL R v0.3.7.4 MASTER TEST SUITE")
    print("===============================================================\n")
    
    for tf in test_files:
        print(f"--> RUNNING: {tf} ...", flush=True)
        res = subprocess.run([sys.executable, tf], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(res.stderr)
            print(f"FAILED: {tf}")
            sys.exit(1)
            
    print("\n===============================================================")
    print("ALL 4 CHECKPOINTS (A, B, C, D) PASSED PERFECTLY!")
    print("===============================================================\n")

if __name__ == "__main__":
    main()
