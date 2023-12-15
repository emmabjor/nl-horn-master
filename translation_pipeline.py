import os
import openai 
import pandas as pd
import re
from dotenv import load_dotenv

from fol_parser import parse_text_FOL_to_tree
import prompts

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from juliacall import Main as jl
jl.include("/Users/emmabjorkas/Documents/Informasjonsvitenskap/Master/First-order-Logic-resolution-master/hw2.jl")



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
        

def save_metadata(df, prompt_iteration):
    """Saves metadata to a file.

    Args:
        df (DataFrame): The dataframe to gather meta data from
        prompt_iteration (str): Name of the prompt iteration
    """
    if -1 in df[f'{prompt_iteration}-evals'].values:
        prompt_error = df[f'{prompt_iteration}-evals'].value_counts()[-1]
    else: 
        prompt_error = 0
    
    if 0 in df[f'{prompt_iteration}-evals'].values:
        prompt_invalid = df[f'{prompt_iteration}-evals'].value_counts()[0]
    else: 
        prompt_invalid = 0
        
    if 1 in df[f'{prompt_iteration}-evals'].values:
        prompt_valid = df[f'{prompt_iteration}-evals'].value_counts()[1]
    else: 
        prompt_valid = 0

    num_formulas = len(df)
    
    data = [num_formulas, prompt_valid, prompt_invalid, prompt_error]
    
    meta_df = pd.read_csv('data/meta_data.tsv', sep='\t', header=0)
    meta_df[prompt_iteration] = data
    
    with open('data/meta_data.tsv', 'w') as f:
        meta_df.to_csv(f, sep='\t', index=False, header=True)
        
        
        

############################# NL to FOL #############################

        
def nl_to_fol(df):
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
        prompt = prompts.prompt_5(i) # ------------- CHANGE PROMPT HERE -------------
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
    return formulas, evals, df
    # save_metadata(df, prompt_iteration)


def nl_to_fol_adjustment(df, prompt_iteration):
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
        prompt = prompts.adjustment_prompt_3(sentence=s, formula=f) # ------------- CHANGE PROMPT HERE -------------
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
    return (formulas, evals, df)
    # save_metadata(df, f'{prompt_iteration}_{adjustment_iteration}')




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
                test = int(f[i+2])
                quants += f[i:i+3]
                new_f = new_f.replace(f[i:i+3], "")
            except:
                quants += f[i:i+2]
                new_f = new_f.replace(f[i:i+2], "")
    new_f = quants+new_f
    return new_f


def rename_quantifier_variables(F, current_variable="init", current_quantifiers = {"init":0}, new = ""):
    """
    Renames the quantifier variables in a given formula.

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
                    cnf_formulas.append('INVALID')
                    cnf_evals.append(0)
                    print(f'INVALID\n')
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
            cnf_evals.append(0)
            print(f'INVALID\n')
            
    return(df, cnf_formulas, cnf_evals)
    
    
    
    
    
############################# CNF to Horn #############################

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
        if cnf_evals[index] == 1:
            if "&" in cnf_formulas[index]:
                horn_formulas.append('INVALID')
                horn_evals.append(0)
                print(f'Not CNF\n')
            else:
                try:
                    antecedent = []
                    consequence = []
                    formula = cnf_formulas[index]
                    formula_splt = formula.split('|')
                    for predicate in formula_splt:
                        if predicate.strip()[0] != '~':
                            consequence.append(predicate.strip())
                        else:
                            i = predicate.replace('~', '¬')
                            antecedent.append(i.strip())

                    if len(consequence) > 1:
                        horn_formulas.append('NOT HORN')
                        horn_evals.append(0)
                        print(f'CNF: {cnf_formulas[index]}\nHorn: Not Horn\n')
                    else:
                        joined = (' ∨ ').join(antecedent)
                        if len(consequence) > 0:
                            joined = (' ∨ ').join([joined, consequence[0]])
                        #print(joined)
                        horn_formulas.append(joined)
                        horn_evals.append(1)
                        print(f'CNF: {cnf_formulas[index]}\nHorn: {joined}\n')
                except Exception as e:
                    horn_formulas.append('ERROR')
                    horn_evals.append(-1)
                    print(f'CNF: {cnf_formulas[index]}\nHorn: {e}\n')
        else:
            horn_formulas.append('INVALID')
            horn_evals.append(0)
            print(f'INVALID\n')
    return df, horn_formulas, horn_evals
    

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
    
    filename = 'data/all_translations.tsv' # ------------- CHANGE FILENAME HERE -------------
    batchfile = 'data/batch_sentences.tsv' # ------------- CHANGE FILENAME HERE -------------
    #filename = 'data/test.tsv' # Testing # ------------- CHANGE FILE HERE -------------
    df_save = pd.read_csv(batchfile, sep='\t', header=0) 
    prompt_iteration = "prompt_5" # ------------- CHANGE PROMPT_ITERATION HERE -------------
    adjustment_iteration = "adjustment_prompt_3" # ------------- CHANGE ADJUSTMENT_ITERATION HERE -------------
    cnf_col_name = "cnf" # ------------- CHANGE COL_NAME HERE -------------
    horn_col_name = "horn" # ------------- CHANGE COL_NAME HERE -------------
    
    #### Batch Handling ####
    df_format = pd.read_csv(filename, sep='\t', header=0, nrows=0)
    df_save = pd.concat([df_format, df_save])
    
    #### NL TO FOL ####
    fol_formulas, fol_evals, fol_df = nl_to_fol(df_save) # ADD (OPTIONAL) FILEPATH HERE
    print("FOL translations finished. Saving values...")
    df_save = update_df(df_save, prompt_iteration, fol_formulas, fol_evals)
    #save_values(fol_df, prompt_iteration, fol_formulas, fol_evals, filename)
    
    fol_adjustment_formulas, fol_adjustment_evals, fol_adjustment_df = nl_to_fol_adjustment(df_save, prompt_iteration)
    print("FOL adjustments finished. Saving values...")
    df_save = update_df(df_save, f'{prompt_iteration}_{adjustment_iteration}', fol_adjustment_formulas, fol_adjustment_evals)
    #save_values(fol_adjustment_df, f'{prompt_iteration}_{adjustment_iteration}', fol_adjustment_formulas, fol_adjustment_evals, filename)    
        
        
    #### FOL TO CNF ####
    cnf_df, cnf_formulas, cnf_evals = fol_to_cnf(df_save, prompt_iteration, adjustment_iteration)
    print("CNF convertion finished. Saving values...")
    df_save = update_df(df_save, cnf_col_name, cnf_formulas, cnf_evals)
    #save_values(cnf_df, cnf_col_name, cnf_formulas, cnf_evals, filename)
    
    
    #### CNF TO Horn ####
    horn_df, horn_formulas, horn_evals = cnf_to_horn(df_save, cnf_col_name)
    print("Horn conversion finished. Saving values...")
    df_save = update_df(df_save, horn_col_name, horn_formulas, horn_evals)
    
    
    save_values(df_save, filename)


if __name__ == "__main__":
    main()
