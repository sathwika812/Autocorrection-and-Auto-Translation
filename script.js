async function autoCorrect(text) {
    try {
        const response = await fetch('http://localhost:5000/autocorrect', {
            method: 'POST',
            body: JSON.stringify({ text: text }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        return data.corrected_text;
    } catch (error) {
        console.error('Error:', error);
        return text; // Return the original text if there's an error
    }
}

async function translate(text, targetLanguages) {
    try {
        const response = await fetch('http://localhost:5000/translate', {
            method: 'POST',
            body: JSON.stringify({ text: text, target_languages: targetLanguages }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        if (data.error) {
            console.error('Error:', data.error);
            return 'Translation error';
        }
        return data.translations;
    } catch (error) {
        console.error('Error:', error);
        return 'Translation error';
    }
}

function autoCorrectText() {
    const textInput = document.getElementById('textInput').value;
    autoCorrect(textInput).then(correctedText => {
        document.getElementById('output').innerText = correctedText;
    });
}

function showLanguageSelect() {
    document.getElementById('languageSelectContainer').style.display = 'block';
}

function translateText() {
    const textInput = document.getElementById('textInput').value;
    const languageSelect = document.getElementById('languageSelect');
    const selectedLanguages = Array.from(languageSelect.selectedOptions).map(option => option.value);

    translate(textInput, selectedLanguages).then(translations => {
        let outputHtml = '';
        for (const [language, translation] of Object.entries(translations)) {
            outputHtml += `<p><strong>${language}:</strong> ${translation}</p>`;
        }
        document.getElementById('output').innerHTML = outputHtml;
    });
}

