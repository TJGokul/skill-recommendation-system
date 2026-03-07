import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {bool(api_key)}")
if api_key:
    print(f"API Key starts with: {api_key[:10]}...")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    try:
        # Test simple generation
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in one word")
        print(f"✅ Success! Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ No API key found in .env file")