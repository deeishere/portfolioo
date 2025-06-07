

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GitHub Models configuration
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400

        # Formulate the prompt
        prompt_content = (
            "Please create a recipe for children using the following ingredients: "
            f"{', '.join(ingredients)}. "
            "The approximate time to do it 'Approximate Time:'"
            "Include a creative name with 'Recipe Title:', "
            "an introduction with 'Introduction:', "
            "ingredients with 'Ingredients:', and "
            "cooking steps with 'Cooking Steps:'."
        )

        # Make API request
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert chef."},
                {"role": "user", "content": prompt_content},
            ],
            temperature=1.0,
            max_tokens=1000,
            model=model_name,
        )
        
        generated_text = response.choices[0].message.content.strip()
        return jsonify({'recipe': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    


