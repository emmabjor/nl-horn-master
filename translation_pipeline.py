import os
import openai 
import pandas as pd
import re
from dotenv import load_dotenv
from random import randint

from fol_parser import parse_text_FOL_to_tree
import prompts

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from juliacall import Main as jl
jl.include("/Users/emmabjorkas/Documents/Informasjonsvitenskap/Master/gpt_pipeline/First-order-Logic-resolution-master/hw2.jl")

"""
Eval codes:

Valid: 1
Invalid at this stage: 0
Error at this stage: -1
Invalid at an earlier stage: -2
"""

############################# GPT Translation #############################

def gpt_call(prompt):
    """Calls on GPT-4 with the provided prompt.

    Args:
        prompt (list): The prompt to be used

    Returns:
        str: The response content from GPT-4
    """
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = prompt)
    return response['choices'][0]['message']['content']





############################# FOL Validity #############################

def check_fol_val(f):
    """Uses the fol_parser to check if a FOL formula is valid.

    Args:
        f (str): The formula to be checked

    Returns:
        int: 0 if invalid, 1 if valid
    """
    tree = parse_text_FOL_to_tree(f)
    if tree == None:
        print(f'Formula: {f}\nINVALID')
        return 0
    else:
        print(f'Formula: {f}\nVALID')
        return 1





############################# Data Saving #############################

def save_values(df, filename):
    """Adds the values from the list to the dataframe and saves it to a file.

    Args:
        formulas (list): Translated formulas from GPT
        evals (list): Evaluation of formulas' validity (1 for valid, 0 for invalid)
        df (DataFrame): The dataframe containing the data we want to save.
        prompt_iteration (str): Name of the prompt iteration
    """
    df.to_csv(filename, sep='\t', mode='a', index=False, header=False)
             
        

############################# NL to FOL #############################

        
def nl_to_fol(df, prompt_function):
    """Iterates through a dataframe and calls for gpt to translate each sentence.
    Evaluates each translation as valid (1) or invalid (0), in addition to errors (-1).
    Saves the translations and evaluation to the file containing all translations.

    Args:
        df (DataFrame): The dataframe to iterate through
        prompt_iteration (str): Name of the prompt iteration
        save_file (str, optional): Filepath to save valid translations. Defaults to "".
        discard_file (str, optional): Filepath to save invalid translations. Defaults to "".
    """
    formulas = []
    evals = []
    for i in df['input_sequence']:
        prompt = prompt_function(i)
        try:
            formula = gpt_call(prompt)
        except:
            formulas.append('ERROR')
            evals.append(-1)
            continue
        if check_fol_val(formula) == 1:
            formulas.append(formula)
            evals.append(1)
        else:
            formulas.append(formula)
            evals.append(0)
    return formulas, evals
    # save_metadata(df, prompt_iteration)


def nl_to_fol_adjustment(df, prompt_iteration, adjustment):
    """Iterates through a dataframe and calls for gpt to adjust each sentence.
    Evaluates each translation as valid (1) or invalid (0), in addition to errors (-1).
    Saves the translations and evaluation to the file containing all translations.

    Args:
        df (DataFrame): The dataframe to iterate through
        prompt_iteration (str): Name of the prompt iteration
    """
    formulas = []
    evals = []
    for s, f in zip(df['input_sequence'], df[f'{prompt_iteration}-translations']):
        prompt = adjustment(sentence=s, formula=f) 
        try:
            formula = gpt_call(prompt)
        except:
            formulas.append('ERROR')
            evals.append(-1)
            continue
        if check_fol_val(formula) == 1:
            formulas.append(formula)
            evals.append(1)
        else:
            formulas.append(formula)
            evals.append(0)
    return (formulas, evals)




############################# CNF convertion #############################

### Pre-processing ###

def check_repeat_var(f):
    """
    Checks if there are repeated variables in the given formula.

    Args:
        f (str): The formula to check.

    Returns:
        bool: True if there are repeated variables, False otherwise.
    """
    vars = []
    eval = False
    for i in range(len(f)):
        if f[i] == '∃' or f[i] == '∀':
            if f[i+1] not in vars:
                vars.append(f[i+1])
            else:
                eval = True
    return eval


def push_quantifiers(f):
    """
    Removes quantifiers (∀, ∃) from the input string and pushes them to the beginning of the string.

    Args:
        f (str): The input string containing quantifiers.

    Returns:
        str: The modified string with quantifiers pushed to the beginning.
    """
    quants = ""
    new_f = f
    for i in range(len(f)-2):
        if f[i] == "∀" or f[i] == "∃":
            try:
                quants += f[i:i+3]
                new_f = new_f.replace(f[i:i+3], "")
            except:
                quants += f[i:i+2]
                new_f = new_f.replace(f[i:i+2], "")
    new_f = quants+new_f
    return new_f


def rename_quantifier_variables(F, current_variable="init", current_quantifiers = {"init":0}, new = ""):
    """
    Renames the all quantifier variables in a given formula.

    Parameters:
    - F (str): The formula to rename the quantifier variables in.
    - current_variable (str): The current variable being processed. Default is "init".

    Returns:
    - str: The formula with renamed quantifier variables.
    """
    form = F+"*"
    num_parent = 1
    i=0
    while form[i] != "*":
        if form[i]=='∀' or form[i] == "∃":
            new = new+form[i]
            var = form[i+1]
            if var in current_quantifiers:
                current_quantifiers[var] = current_quantifiers[var] + 1
                return rename_quantifier_variables(form[i+1:], var, current_quantifiers, new)
            else:
                current_quantifiers[var] = 0
                return rename_quantifier_variables(form[i+1:], var, current_quantifiers, new)
        elif form[i] in current_quantifiers:
            pre = form[i-1]
            post = form[i+1]
            if re.search("[a-zA-Z]", pre) == None and re.search("[a-zA-Z]", post) == None:
                new = new + form[i]+str(current_quantifiers[form[i]]) 
            else:
                new = new + form[i]
        elif form[i] == '(':
            new = new + form[i]
            num_parent += 1
        elif form[i] == ')':
            new = new + form[i]
            num_parent -= 1
        else:
            new = new + form[i]
        if num_parent == 0:
            current_quantifiers[current_variable] -= 1
        i+=1
    return(new)


def replace_op(formula):
    """
    Replaces the operators in a formula to woek with Julia code.

    Args:
        formula (str): The formula to be edited

    Returns:
        str: The edited formula
    """
    formula = formula.replace('∨', '|')
    formula = formula.replace('∧', '&')
    formula = formula.replace('→', '==>')
    formula = formula.replace('↔', '<=>')
    formula = formula.replace('¬', '~')
    return formula


### Conversion ###

def fol_to_cnf_converter(lst):
    """Converts a list of FOL formulas to CNF using Julia code.

    Args:
        lst (list): The list of FOL formulas to be converted

    Returns:
        lst: The list of converted formulas.
    """
    clauses = jl.map(jl.skolemize, jl.map(jl.toCNF, jl.map(jl.toClause, jl.map(jl.lexer, lst))))
    translated_formulas = []
    for i in clauses:
        formatted = jl.printClause(i)
        translated_formulas.append(formatted)
    return translated_formulas


def fol_to_cnf(df, prompt_iteration, adjustment_iteration):
    """Creates a data frame of the CNF translations and evaluations.

    Args:
        df (DataFrame): The dataframe to iterate through
        col_name (str): Name of the column to save the translations and evaluations to
        prompt_iteration (str): Name of the prompt iteration
        adjustment_iteration (str): Name of the prompt iteration
    """
    fol_formulas = list(df[f'{prompt_iteration}_{adjustment_iteration}-translations'])
    fol_evals = list(df[f'{prompt_iteration}_{adjustment_iteration}-evals'])

    cnf_formulas = []
    cnf_evals = []

    for index in range(len(fol_formulas)):
        if fol_evals[index] == 1:
            try:
                eval = check_repeat_var(fol_formulas[index])
                if eval == False:
                    pre_processed_formula = push_quantifiers(fol_formulas[index])
                else:
                    renamed_vars = rename_quantifier_variables(fol_formulas[index])
                    pre_processed_formula = push_quantifiers(renamed_vars)
                if check_fol_val(pre_processed_formula) == 0:
                    cnf_formulas.append(pre_processed_formula)
                    cnf_evals.append(0)
                    print(f'INVALID CNF\n')
                else:
                    converted = fol_to_cnf_converter([replace_op(pre_processed_formula)])
                    cnf_formulas.append(converted[0])
                    cnf_evals.append(1)
                    print(f'FOL: {fol_formulas[index]}\nCNF: {converted[0]}\n')
            except:
                cnf_formulas.append('ERROR')
                cnf_evals.append(-1)
                print(f'FOL: {fol_formulas[index]}\nCNF: ERROR\n')
        else:
            cnf_formulas.append('INVALID')
            cnf_evals.append(-2)
            print(f'INVALID\n')
            
    return(cnf_formulas, cnf_evals)
    
    
    
    
    
############################# CNF to Horn #############################


def split_formula(f):
    """
    Splits a CNF formula into its antecedent and consequence parts.

    Args:
        f (str): The CNF formula to split.

    Returns:
        tuple: A tuple containing the antecedent and consequence parts of the formula.
    """
    antecedent = []
    consequence = []
    f = f.strip()
    f = f[1:-1]
    formula_splt = f.split('|')
    for predicate in formula_splt:
        if '~' not in predicate:
            consequence.append(predicate.strip())
        else:
            i = predicate.replace('~', '¬')
            antecedent.append(i.strip())
    return antecedent, consequence


def join_formula(antecedent, consequence):
    """
    Joins the antecedent and consequence parts of a Horn formula.

    Args:
        antecedent (list): The antecedent part of the Horn formula.
        consequence (list): The consequence part of the Horn formula.

    Returns:
        str: The joined Horn formula.
    """
    joined = (' ∨ ').join(antecedent)
    if len(consequence) > 0:
        joined = (' ∨ ').join([joined, consequence[0]])
    return '('+joined+')'


def add_parenthesis(f):
    splitted_f = f.split('&')
    joined_f = ""
    for i in splitted_f:
        joined_f += ("("+i.strip()+") & ")
    return joined_f[:-3]


def create_horn(f):
    if "|" not in f:
        return f
    antecedent, consequence = split_formula(f)
    if len(consequence) > 1: # Formula has more than one positive literal and is not Horn
        return None
    else: # Formula is Horn 
        joined = join_formula(antecedent, consequence)
        return joined
    

def cnf_to_horn(df, cnf_col_name):
    """Converts a data frame of CNF formulas to Horn formulas.

    Args:
        df (DataFrame): The dataframe to iterate through
        horn_col_name (str): Name of the column to save the translations and evaluations to
        cnf_col_name (str): Name of the column to iterate through
    """

    cnf_formulas = list(df[f'{cnf_col_name}-translations'])
    cnf_evals = list(df[f'{cnf_col_name}-evals'])

    horn_formulas = []
    horn_evals = []

    for index in range(len(cnf_formulas)):
        if cnf_evals[index] == 1: # Formula is valid FOL
            
            try:
                formula = add_parenthesis(cnf_formulas[index])
                horn_sentence = ""
                is_horn = True
                for i in formula.split('&'):
                    sub_horn = create_horn(i)
                    
                    if sub_horn is None: # One of the conjunctions is not Horn
                        horn_formulas.append('INVALID HORN')
                        horn_evals.append(0)
                        print(f'CNF: {cnf_formulas[index]}\nHorn: INVALID HORN\n')
                        is_horn = False
                        break
                    
                    else: # The conjunction is Horn
                        horn_sentence += sub_horn.strip() + " ∧ "
                        
                if is_horn: # All conjunctions are Horn
                    horn_formulas.append(horn_sentence[:-3])
                    horn_evals.append(1)
                    print(f'CNF: {cnf_formulas[index]}\nHorn: {horn_sentence[:-3]}\n')
                    
            except Exception as e: # Error in parsing
                horn_formulas.append('ERROR')
                horn_evals.append(-1)
                print(f'CNF: {cnf_formulas[index]}\nHorn: {e}\n')
                
                    
        else: # Formula is not valid FOL and therefore not valid Horn
            horn_formulas.append('INVALID')
            horn_evals.append(-2)
            print(f'INVALID\n')
    return horn_formulas, horn_evals
    

def update_df(df_save, col_name, formulas, evals):
    """Updates the dataframe with the new formulas and evaluations.

    Args:
        df (DataFrame): The dataframe to update
        col_name (str): Name of the column to save the translations and evaluations to
        formulas (list): List of formulas to save
        evals (list): List of evaluations to save
    """
    df_save[f'{col_name}-translations'] = formulas
    df_save[f'{col_name}-evals'] = evals
    return df_save
        
    
    
############################# MAIN #############################

def main():
    
    # Reading the file with all translations (correct version)
    
    filename = 'data/all_translations.tsv' 
    batchfile = 'data/batch_sentences.tsv' 
    #filename = 'data/test.tsv' # Testing 
    df_save = pd.read_csv(batchfile, sep='\t', header=0) # ------------- CHANGE FILENAME HERE -------------
    prompt_function = prompts.prompt_6 # ------------- CHANGE PROMPT HERE -------------
    prompt_iteration = "prompt_6" # ------------- CHANGE PROMPT_ITERATION HERE -------------
    adjustment_function = prompts.adjustment_prompt_4 # ------------- CHANGE ADJUSTMENT HERE -------------
    adjustment_iteration = "adjustment_prompt_4" # ------------- CHANGE ADJUSTMENT_ITERATION HERE -------------
    cnf_col_name = "cnf" 
    horn_col_name = "horn" 
    
    #### Batch Handling ####
    df_format = pd.read_csv(filename, sep='\t', header=0, nrows=0)
    df_save = pd.concat([df_format, df_save])
    
    # Testing
    # lst = [["(¬A(x) ∨ B(x)) ∧ C(x) ∧ (¬D(x) ∨ ¬E(x))", 1],
    #        ["¬A(x) ∨ ¬B(x)", 1],
    #        ["INVALID", 0]]
    # df_save = pd.DataFrame(lst, columns=["prompt_5_adjustment_prompt_3-translations","prompt_5_adjustment_prompt_3-evals"])
    # prompt_iteration = "prompt_5" # ------------- CHANGE PROMPT_ITERATION HERE -------------
    # adjustment_iteration = "adjustment_prompt_3" # ------------- CHANGE ADJUSTMENT_PROMPT_ITERATION HERE -------------
    
    #### NL TO FOL ####
    fol_formulas, fol_evals = nl_to_fol(df_save, prompt_function) # ADD (OPTIONAL) FILEPATH HERE
    print("FOL translations finished. Saving values...")
    df_save = update_df(df_save, prompt_iteration, fol_formulas, fol_evals)
    
    fol_adjustment_formulas, fol_adjustment_evals = nl_to_fol_adjustment(df_save, prompt_iteration, adjustment_function)
    print("FOL adjustments finished. Saving values...")
    df_save = update_df(df_save, f'{prompt_iteration}_{adjustment_iteration}', fol_adjustment_formulas, fol_adjustment_evals)
            
        
    #### FOL TO CNF ####
    cnf_formulas, cnf_evals = fol_to_cnf(df_save, prompt_iteration, adjustment_iteration)
    print("CNF convertion finished. Saving values...")
    df_save = update_df(df_save, cnf_col_name, cnf_formulas, cnf_evals)
    
    
    # #### CNF TO Horn ####
    horn_formulas, horn_evals = cnf_to_horn(df_save, cnf_col_name)
    print("Horn conversion finished. Saving values...")
    df_save = update_df(df_save, horn_col_name, horn_formulas, horn_evals)
    
    
    try:
        save_values(df_save, filename)
    except:
        num = f"{str(randint(0,9))}" +f"{str(randint(0,9))}"+f"{str(randint(0,9))}"
        backup_file = 'data/gpt_data_'+num+'.tsv'
        print("Error saving values. Data frame saved to file gpt_data_"+num+".tsv")
        df_save.to_csv(backup_file, sep='\t', mode='w', index=False, header=True)
        


if __name__ == "__main__":
    main()
