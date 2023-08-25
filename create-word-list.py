import openai
import json
import random

# Initialize OpenAI API
openai.api_key = 'YOUR_API_KEY'

sru_json = 'sru-word-list.json'
common_words_txt = 'common-words.txt'
output_filename = 'generated-list.json'
sru_words_count = 10
common_words_count = 20


def get_clue(word):
  # This function will request a definition or a clue for the word from OpenAI API
  response = openai.Completion.create(
    prompt=f"Provide a clue for the word: {word}",
    max_tokens=50
  )
  return response.choices[0].text.strip()

def get_sru_words_and_hints(num_entries):
  with open(sru_json, 'r') as json_file:
    data = json.load(json_file)
    
  word_entries = data["words"]
  sru_words = random.sample(word_entries, min(num_entries, len(word_entries)))

  return sru_words

def get_commmon_words(num_words):
  with open(common_words_txt, 'r') as txt_file:
    words = txt_file.read().splitlines()

  random_words = random.sample(words, min(num_words, len(words)))

  return random_words

word_dict = {'words' : []}
sru_words_and_hints = get_sru_words_and_hints(sru_words_count)
common_words = get_commmon_words(common_words_count)

#append common words and clues to full list
for word in common_words:
  #clue = get_clue(word)
  clue = 'lorum ipsum'
  word_dict['words'].append({'word': word.upper(), 'clue': clue})

#append sru words and clue to full list
for entry in sru_words_and_hints:
  word_dict['words'].append({'word': entry['word'].upper(), 'clue': entry['hint']})

#shuffle full dictionary
random.shuffle(word_dict['words'])

for x in word_dict['words']:
  print(f"{x['word']} - {x['clue']}")

with open(output_filename, 'w') as json_file:
    json.dump(word_dict, json_file, indent=4)

print(f"Saved word_dict to {output_filename}")