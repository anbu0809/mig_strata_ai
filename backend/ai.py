import os
import openai
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def translate_schema(source_dialect: str, target_dialect: str, input_ddl_json: dict) -> dict:
    """
    Translate schema from source dialect to target dialect using OpenAI
    """
    # Check if API key is available
    if not openai.api_key or openai.api_key == "":
        return {
            "translated_ddl": "-- Translation skipped (no API key)",
            "notes": "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment variables."
        }
    
    try:
        prompt = f"""
        Translate the following database schema from {source_dialect} to {target_dialect}.
        Provide the translated DDL and any notes about compatibility issues or manual adjustments needed.
        
        Input DDL:
        {input_ddl_json}
        
        IMPORTANT: Please format your response as JSON with the following structure:
        {{
            "translated_ddl": "Translated DDL statements",
            "notes": "Any compatibility notes or manual adjustments needed"
        }}
        """
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a database schema translation expert. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Check if response content exists
        content = response.choices[0].message.content
        if content is None:
            return {
                "translated_ddl": "-- Translation failed",
                "notes": "AI returned empty response"
            }
        
        # Try to parse as JSON, if that fails return the raw content
        try:
            # Handle code block wrapper if present
            cleaned_content = content.strip()
            if cleaned_content.startswith('```json'):
                # Extract JSON from code block
                cleaned_content = cleaned_content[7:]  # Remove ```json
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]  # Remove ```
                cleaned_content = cleaned_content.strip()
            elif cleaned_content.startswith('```'):
                # Extract content from generic code block
                cleaned_content = cleaned_content[3:]  # Remove ```
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]  # Remove ```
                cleaned_content = cleaned_content.strip()
            
            result = json.loads(cleaned_content)
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, return the content as notes
            return {
                "translated_ddl": "-- Translation completed (see notes)",
                "notes": content
            }
    except Exception as e:
        return {
            "translated_ddl": "-- Translation failed",
            "notes": f"AI translation failed: {str(e)}"
        }

def suggest_fixes(validation_failures_json: dict) -> dict:
    """
    Suggest fixes for validation failures using OpenAI
    """
    # Check if API key is available
    if not openai.api_key or openai.api_key == "":
        return {
            "fixes": [{
                "category": "Error",
                "issue": "OpenAI API key not configured",
                "solution": "Please set OPENAI_API_KEY in your environment variables to enable AI features.",
                "precautions": "None"
            }]
        }
    
    try:
        prompt = f"""
        Based on the following validation failures, suggest fixes for each issue:
        
        Validation Failures:
        {validation_failures_json}
        
        For each failure, provide:
        1. A detailed explanation of the issue
        2. Step-by-step instructions to fix it
        3. Any precautions or considerations
        
        IMPORTANT: Please format your response as JSON with the following structure:
        {{
            "fixes": [
                {{
                    "category": "Category name",
                    "issue": "Detailed explanation",
                    "solution": "Step-by-step fix",
                    "precautions": "Any precautions"
                }}
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a database migration expert. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Check if response content exists
        content = response.choices[0].message.content
        if content is None:
            return {
                "fixes": [{
                    "category": "Error",
                    "issue": "AI returned empty response",
                    "solution": "No suggestions available",
                    "precautions": "None"
                }]
            }
        
        # Try to parse as JSON, if that fails return the raw content
        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a default structure with the content as an issue
            return {
                "fixes": [{
                    "category": "AI Response",
                    "issue": content,
                    "solution": "See issue description",
                    "precautions": "None"
                }]
            }
    except Exception as e:
        return {
            "fixes": [{
                "category": "Error",
                "issue": "Failed to generate suggestions",
                "solution": f"AI suggestion generation failed: {str(e)}",
                "precautions": "None"
            }]
        }