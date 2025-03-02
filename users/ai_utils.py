import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_ai_suggestion(extracted_text, user_info):
    try:
        prompt = f"""
        Given the extracted food ingredients: {extracted_text}
        and the user's health data: {user_info},
        determine if the user can eat this food.
        Consider age, gender, BMI, and health conditions.
        Answer these three questions in one point:
        1. Can the user eat this food?
        2. How much can they consume safely?
        3. If they overconsume, what are the consequences and remedies?
        Provide a simple yes/no answer with a brief explanation.
        """

        model_name = "gemini-1.5-pro"  # Use the latest available model
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        return response.text if response else "No response from AI."

    except Exception as e:
        return f"Error fetching AI suggestion: {str(e)}"
