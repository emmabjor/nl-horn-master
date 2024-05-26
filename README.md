# Automatic encoding from natural language to Horn clauses

**Encoding system:**
A system that use GPT-4 to encode natural language norms to first-order Horn clauses. Prompts can be found and edited in the file [promtps.py](prompts.py). The code includes functionality to write all Horn clauses to a clingo script found in file [results.horn_inconsistency_checker.lp](results.horn_inconsistency_checker.lp). Additionally, the file includes functionality for using a sentiment analysis model able to predict the evaluation constant for the norms. The sentiment analysis is trained using the [sentiment_analysis_labeled.tsv](sentiment_analysis_labeled.tsv) examples.

We have made the following delimitations to the encodings:
- Each encoding should be an implication where the antecedent represents the situation as a conjunction of predicates and the consequent should represent the moral judgment of the situation using a predicate evaluation, with the moral judgment as a constant, such as evaluation(GOOD) or evaluation(BAD).
- Positive moral judgements should be encoded with the consequent evaluation(GOOD), while negative moral judgements should be encoded with the consequent evaluation(BAD).
- Each NL norm that expresses the evaluation part using the phrases “you should” or “you should not” should be interpreted respectively as “it’s good to” or “it’s bad to”.
- The evaluation predicate should not be negated.
- The logical connective symbolizing equivalence = should not be used.
- Norms that are not grammatically correct or have nonsensical formulations should not be encoded.

## Installation and running:
Use Python 3.8.19

1. Clone this repo and install necessary requirements specified in [requirements.txt](requirements.txt): `pip install -r requirements.txt`
2. Add your personal OpenAI API key in the [.env](.env) file.

3. Add index and norms to the [data/batch_sentences.tsv](data/batch_sentences.tsv) file. This file currently contains two examples. These are the norm sentences that will be encoede to Horn clause representations.
3. Edit second line in [encoding_system.py](encoding_system.py) to local path.
4. Run [encoding_system.py](encoding_system.py). Results will be saved to [data/results.tsv](data/results.tsv).

Manually encoded norms from the NL norm dataset and evaluation of faithfulness of the automatically encoded FOLs can be found in [results/annotated-encodings.tsv](results/annotated-encodings.tsv). The column `automated_fol_encoding-eval` contains the manaul faithfulness evaluation of each encoded norm. 0: Syntactically invalid encoding, 1: Wrong encoding, 2: Lacking encoding, 3: Accurate encoding.

Clingo program with all valid Horn clauses represented as ASP facts and norms can be found in [results/horn_inconsistency_checker.lp](results/horn_inconsistency_checker.lp).

Results from running norms from the NL norm dataset can be found in [results/encoding_results.tsv](results/encoding_results.tsv). 

Code for creating the Clingo program and performing sentiment analysis of the evaluation constants is found in [solver_and_sa.ipynb](solver_and_sa.ipynb).

The code in the [First-order-Logic-resolution-master](First-order-Logic-resolution-master) is copied from this repository: https://github.com/wjdanalharthi/First-order-Logic-resolution (Alharthi, 2019).

The [fol_parser.py](fol_parser.py) file is copied from this repository: https://github.com/gblackout/LogicLLaMA (Yang, 2023).



Wjdan Alharthi. First-order logic resolution. https://github.com/wjdanalharthi/F
irst-order-Logic-resolution, 2019. Accessed January 2024

Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi, and Faramarz Fekri. Harnessing
the power of large language models for natural language to first-order logic translation,
2023.

