# Automatic encoding from natural language to Horn clauses

**Encoding system:**
A system that use GPT-4 to encode natural language norms to first-order Horn clauses. Prompts can be found and edited in the file [promtps.py](prompts.py). Additionally, the code includes functionality to write all Horn clauses to a clingo script [results.horn_inconsistency_checker.lp](results.horn_inconsistency_checker.lp). 

Use Python 3.8.19

1. Clone this repo and install necessary requirements specified in [requirements.txt](requirements.txt): `pip install -r requirements.txt`
2. Add your personal OpenAI API key in the [.env](.env) file.

3. Add index and norms to the [data/batch_sentences.tsv](data/batch_sentences.tsv) file. This file currently contains two examples. These are the norm sentences that will be encoede to Horn clause representations.
3. Edit second line in [encoding_system.py](encoding_system.py) to local path.
4. Run [encoding_system.py](encoding_system.py). Results will be saved to [data/results.tsv](data/results.tsv).

Manually encoded norms from the NL norm dataset and evaluation of faithfulness of the automatically encoded FOLs can be found in [results/annotated-encodings.tsv](results/annotated-encodings.tsv).

Clingo program with all valid Horn clauses represented as ASP facts and norms can be found in [results/horn_inconsistency_checker.lp](results/horn_inconsistency_checker.lp).

Results from running norms from the NL norm dataset can be found in [results/encoding_results.tsv](results/encoding_results.tsv). 

Code for creating the Clingo program and performing sentiment analysis of the evaluation constants is found in [solver_and_sa.ipynb](solver_and_sa.ipynb).

The code in the [First-order-Logic-resolution-master](First-order-Logic-resolution-master) is copied from this repository: https://github.com/wjdanalharthi/First-order-Logic-resolution

The [fol_parser.py](fol_parser.py) file is copied from this repository: https://github.com/gblackout/LogicLLaMA
