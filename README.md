# Automatic encoding from natural language to Horn clauses

**Encoding system:**
A system that use GPT-4 to encode natural language norms to first-order Horn clauses.

Clone this repo and install necessary requirements specified in `requirements-txt`. 
Add index and norms to the `data/batch_sentences.tsv` file. These are the norm sentences that will be encoede to Horn clause representations.
Create a .env file with personal OpenAI API key.
Edit second line in `encoding_system.py`to local path.
Run `encoding_system.py`. Results will be saved to `data/results.tsv`.

Results from running norms from the NL norm dataset can be found in `results/encoding_results.tsv`. 

Manually encoded norms from the NL norm dataset and evaluation of faithfulness of the automatically encoded FOLs can be found in `results/annotated-encodings.tsv`.

Clingo program with all valid Horn clauses represented as ASP facts and norms can be found in `results/horn_inconsistency_checker.lp`.

Code for creating the Clingo program and performing sentiment analysis of the evaluation constants.
