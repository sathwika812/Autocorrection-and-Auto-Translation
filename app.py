from flask import Flask, request, jsonify # type: ignore
from transformers import MarianMTModel, MarianTokenizer # type: ignore

app = Flask(__name__)

# Define a dictionary mapping language codes to model names
model_names = {
    'hi': 'Helsinki-NLP/opus-mt-en-hi',
    'ta': 'Helsinki-NLP/opus-mt-en-ta',
    'te': 'Helsinki-NLP/opus-mt-en-te',
    'kn': 'Helsinki-NLP/opus-mt-en-kn',
    'ml': 'Helsinki-NLP/opus-mt-en-ml',
    'gu': 'Helsinki-NLP/opus-mt-en-gu',
    # Add more languages and their corresponding model names here
}

@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    data = request.get_json()
    text = data.get('text', '')
    # Add your auto-correct logic here
    corrected_text = text  # For now, return the original text
    return jsonify({'corrected_text': corrected_text})

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_languages = data.get('target_languages', ['hi'])

    translations = {}
    for target_language in target_languages:
        if target_language not in model_names:
            translations[target_language] = 'Unsupported language'
            continue

        model_name = model_names[target_language]
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
        translated_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        translations[target_language] = translated_text[0]

    return jsonify({'translations': translations})

if __name__ == '__main__':
    app.run(debug=True)
