import os
import sys

def main():
    print("Starting BharatCodeMix...")
    print("Ensuring environment variables are loaded...")
    
    # Check if dependencies are installed
    try:
        import gradio
        import transformers
    except ImportError:
        print("Error: Missing dependencies. Please run: pip install -r requirements.txt")
        sys.exit(1)
        
    print("Launching Application...")
    os.system("python app.py")

if __name__ == "__main__":
    main()
