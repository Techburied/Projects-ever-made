document.getElementById('wordInput').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        search();
    }
});

async function search() {
    const word = document.getElementById('wordInput').value;
    const meaningElement = document.getElementById('meaning');

    try {
        const response = await fetch(`https://www.dictionaryapi.com/api/v3/references/collegiate/json/${word}?key=2adae326-dd8e-4839-8a28-d8b1ef583e5b`);

        if (!response.ok) {
            throw new Error('Word not found');
        }

        const data = await response.json();
        const meaning = data[0].shortdef[0];
        meaningElement.textContent =  data[0].shortdef[0] + " ," + data[0].shortdef[1]+ " , "  + data[0].shortdef[2];
    } catch (error) {
        console.error('Error:', error);
        meaningElement.textContent = 'Word not found';
    }
}
