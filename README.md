# Codenames Clue Generator
This project uses semantic word embeddings to generate effective clues for the board game Codenames. The embeddings are used to calculate similarity between words, and then choose optimal clues based on the given board and team.

### Installation
1. Clone the repository: `git clone https://github.com/jasonjewelljason/codenames-clue-generator`
2. Install the requirements: `pip install -r requirements.txt`

### Usage
1. Run `get_embeddings.py` to download the word embeddings. This will take ~5 minutes.
2. Run `clue_generator.py`. Follow the prompts to generate a random board, or enter your own board. After each action, you will be prompted to choose the next action:
    * `remove`: Remove words from the board after they have been guessed.
    * `check`: Check the most similar board words to a given clue word (useful to see which words the generated clue is referring to).
    * `clue`: Generate a clue for the current board.
    * `quit`: Quit the program.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgements
* Board generator by Hunter Biede: https://github.com/hbiede/Codenames-Board-Generator
* GloVe word embeddings by Stanford NLP: https://nlp.stanford.edu/projects/glove/
* Common English word list by Keith Vertanen: https://www.keithv.com/software/wlist/
* Functor word list by James O'Shea: https://semanticsimilarity.wordpress.com/function-word-lists/

### Paper
You can find the paper I wrote about this project [here](link).

### Contact
Feel free to reach out with any questions or comments!

Jason Jewell - jewell@u.northwestern.edu
