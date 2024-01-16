# prompt 1: Initial prompt example
def prompt_1(sentence):
    return [
    {"role": "system", "content": "You are an assistent that translates English natural language sentences into well formulated first-order logic formulas.\
        Strictly use these signs and operators: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','"},
    {"role": "user", "content": "The one who created this repo is either a human or an alien"},
    {"role": "assistant", "content": "CreatedBy(repo, human) ⋁ CreatedBy(repo, alien)"},
    {"role": "user", "content": sentence}]

    
# prompt 2: Trying to fix Expectation(Love(x))) and  evaluation(¬good)) cases
def prompt_2(sentence):
    return [
    {"role": "system", "content": "Your task is to convert English sentences into precise first-order logic formulas using specific symbols ('⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','). \
        Use predicates (e.g. 'People()'), variables (e.g. 'x'), and constants (e.g. 'bad'). \
        Predicates can only contain variables and constants, such as 'ShouldSleepAround(x)' and 'RevealEverything(x, y))'\
        It is strictly forbidden for predicates to contain other predicates, such as 'ShouldExpect(x, RevealEverything(y))' and 'ok(Frustrated(x))'. \
        Remember, only predicates can be negated, not variables. \
        Also, '¬evaluation(good)' isn't the same as 'evaluation(bad).' \
        You get two examples that show the wanted output format."},
    {"role": "user", "content": "it's good to meet new people when you go shopping."},
    {"role": "assistant", "content": "∀x∀y(Shopping(x) ∧ Meets(x,y) ∧ New(y) → evaluation(good))"},
    {"role": "user", "content": "people should root for the success of their friends' relationships."},
    {"role": "assistant", "content": "∀x∀y∀z(People(x) ∧ Friends(x,y) ∧ Relationship(z) ∧ Has(y,z) → ShouldRootFor(x,z))"},
    {"role": "user", "content": sentence}]
    

# "You are an assistent that translates English natural language sentences into well formulated first-order logic formulas.\
#         Strictly use these signs and operators: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ',' \
#         The translations should use predicates (such as 'People()'), variables (such as 'x') and constants (such as 'bad').\
#         Predicates cannot take other predicates as arguments. \
#         The formula '∀x∀y(Friends(x,y) → ShouldExpect(x, RevealEverything(y))) is an example of an invalid formula because ShouldExpect(x, RevealEverything(y)) is not allowed according to the previous rule.'\
#         Variables cannot be negated, only predicates can be negated. \
#         ¬evaluation(good) is not equivalent to evaluation(bad). \
#         You get two examples that show the wanted output format."


# prompt 3: Trying to fix 'you should'-cases and information loss.
def prompt_3(sentence):
    return [
    {"role": "system", "content": "Your task is to convert English sentences into precise first-order logic formulas using specific symbols ('⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','). \
        Try to make the translations as semantically equal to the English sentences as possible, without adding properties that are not explicitly stated.\
        Use variables (e.g. 'x'), constants (e.g. 'bad') and predicates (e.g. 'People(x)'). \
        The scope of a predicate must not be empty, (e.g. 'Person()').\
        Ensure that the scope of a predicate does not contain other predicates or nested structures. Predicates should only involve variables and constants directly, without further nesting. For example, 'Expect(x, ToBe(y, perfectPerson))', '¬ExpectationOf(CutOff(x))', '¬Always(GetRegistrationInfo(x))', and similar constructions are strictly forbidden. The generated predicates should adhere to a flat structure, including only variables, constants, and the necessary logical connectives ('∧', '∨', '¬', etc.), without introducing additional layers of nested predicates or complex structures.\
        DO NOT INCLUDE negated variables, e.g. (evaluation(¬good)). \
        Also, '¬evaluation(good)' isn't the same as 'evaluation(bad)'. \
        When 'you should' is stated, it implies a universal context ('everyone should').\
        You get two examples that show the wanted output format."},
    {"role": "user", "content": "it's good to meet new people when you go shopping."},
    {"role": "assistant", "content": "∀x∀y(Shopping(x) ∧ Meets(x,y) ∧ New(y) → evaluation(good))"},
    {"role": "user", "content": "you should not always get registration information when in an accident"},
    {"role": "assistant", "content": "∀y∃x(Accident(x) ∧ In(y,x) ∧ ¬ShouldGetRegistrationInfo(y))"},
    {"role": "user", "content": sentence}]

# Predicates must not be empty, (e.g 'Predicate()'), and can ONLY contain variables and constants, valid examples: 'ShouldSleepAround(x)' and 'RevealEverything(tom, y))'\
# A predicate CANNOT be inside the scope of another predicate.\

# LEGG INN NOE OM AT 'YOU SHOULD' BETYR 'FOR ALLE'
# OG AT 'IT'S GOOD/NOT OKAY' BETYR 'EVALUATION(GOOD/NOT OKAY)'


# Rephrasing of prompt 3 with new examples
def prompt_4(sentence):
    return [
        {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            You should use the following symbols: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should use variables (e.g. 'x'), constants (e.g. 'bad') and predicates (e.g. 'People(x)').\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            You should not negate variables or constants, e.g. (evaluation(¬good)).\
            When 'you should' is stated, it implies a universal context ('everyone should').\
            When 'it's good' is stated, it implies a consequence interpreted as 'evaluation(good)'.\
            '¬evaluation(good)' isn't the same as 'evaluation(bad)'.\
            You get two examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "```it's good to care about your family's history.```"},
        {"role": "assistant", "content": "∀x∀y(FamilyHistory(x,y) ∧ Cares(x,y) → evaluation(good))"},
        {"role": "user", "content": "```you should sleep around if you don't want an std.```"},
        {"role": "assistant", "content": "∀x(¬WantSTD(x) → ShouldSleepAround(x))"},
        {"role": "user", "content": sentence}
        
    ] 
    
# LEGG INN AT BAD IKKE ER DET SAMME SOM NOT GOOD


def adjustment_prompt_1(sentence, formula):
    return [
    {"role": "system", "content": "Your task is to refine the provded first-order formula in order to make it as logically precise and semantically equilvalent to its respected natural language English formulation provided.\
        You can change the syntax, structure, or phrasing  as you see fit, as long as the resulting formula is a valid first order formula and respects the rules below. \
        Strictly use these signs and operators: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','\
        Use variables (e.g. 'x'), constants (e.g. 'bad') and predicates (e.g. 'People(x)'). \
        The scope of a predicate must not be empty, (e.g. 'Person()').\
        Ensure that the scope of a predicate does not contain other predicates or nested structures.\
        DO NOT INCLUDE negated variables, e.g. (evaluation(¬good)). \
        Also, '¬evaluation(good)' isn't the same as 'evaluation(bad), and vice versa.' \
        When 'you should' is stated, it implies a universal context ('everyone should').\
        If the formula is logcially precise as is, return the formula as is.\
        Only return the adjusted/original formula alone.\
        You get two examples that show the wanted output format."},
    {"role": "user", "content": "NL English sentence: ```it's bad to take an advantage in life when you see it.```. Formula: ```∀x∀y((Sees(x,y) ∧ AdvantageInLife(y)) → evaluation(bad))``` ."},
    {"role": "assistant", "content": "∀x∀y(Advantage(x) ∧ See(y,x) ∧ Take(y,x) → evaluation(bad))"},
    {"role": "user", "content": "NL English sentence: ```it's not okay to expect someone care about to be a perfect person.```. Formula: ```∀x(ExpectPerfectPerson(x) → ¬evaluation(okay))``` ."},
    {"role": "assistant", "content": "∀x(CareAbout(x,y) ∧ ExpectsToBePerfect(x,y) → ¬evaluation(okay))"},
    {"role": "user", "content": f"NL English sentence: ```{sentence}```. Formula: ```{formula}``` ."}]
    
    
def adjustment_prompt_2(sentence, formula):
    return [
        {"role":"system", "content": "You are a system tasked with adjusting a first-order formula to make sure it captures the sentiment expressed in the natural language sentence as accurately and complete as logically possible.\
            You should use the following symbols: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should use variables (e.g. 'x'), constants (e.g. 'bad') and predicates (e.g. 'People(x)').\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            You should not negate variables or constants, e.g. (evaluation(¬good)).\
            When 'you should' is stated, it implies a universal context ('everyone should').\
            When 'it's good' is stated, it implies a consequence interpreted as 'evaluation(good)'.\
            '¬evaluation(good)' isn't the same as 'evaluation(bad)'.\
            You should not change the formula if it is already as precise as it can be, then you should just return the formula as is.\
            You get two examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "NL English sentence: ```it is unexpected people will feel proud of their country.```. Formula: ```∀x(People(x) ∧ Country(x) → ¬ExpectedProudOf(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Country(x) ∧ People(y) ∧ BelongsTo(y,x) ∧ FeelProud(y,x) → evaluation(unexpected))"},
        {"role": "user", "content": "NL English sentence: ```you should ask too much of your family.```. Formula: ```∀x(Family(x) → ShouldAskTooMuch(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Family(x,y) → ShouldAskTooMuch(y,x))"},
        {"role": "user", "content": f"NL English sentence: ```{sentence}```. Formula: ```{formula}``` ."}]
        
        
        
# Ensuring evaluation implication in each formula
def prompt_5(sentence):
    return [
        {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            You should use the following symbols: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should use variables in lowercase (e.g. 'x'), constants in uppercase (e.g. 'BAD') and predicates (e.g. 'People(x)').\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            You should not negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            '¬evaluation(GOOD)' is not the same as 'evaluation(BAD)'.\
            You get two examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "```it's good to care about your family's history.```"},
        {"role": "assistant", "content": "∀x∀y(FamilyHistory(x,y) ∧ Cares(x,y) → evaluation(GOOD))"},
        {"role": "user", "content": "```getting circumcised isn't normal.```"},
        {"role": "assistant", "content": "∀x(GettingCircumcised(x) → ¬evaluation(NORMAL))"},
        {"role": "user", "content": sentence}
        
    ] 
    
# Adjustment prompt that ensure implication in each formula
def adjustment_prompt_3(sentence, formula):
    return [
        {"role":"system", "content": "You are a system tasked with adjusting a first-order formula to make sure it captures the sentiment expressed in the natural language sentence as accurately and complete as logically possible.\
            You should use the following symbols: '⊕', '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should use variables in lowercase (e.g. 'x'), constants in uppercase (e.g. 'BAD') and predicates (e.g. 'People(x)').\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            You should not negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            '¬evaluation(GOOD)' is not the same as 'evaluation(BAD)'.\
            You get two examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "NL English sentence: ```it is unexpected people will feel proud of their country.```. Formula: ```∀x(People(x) ∧ Country(x) → ¬ExpectedProudOf(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Country(x) ∧ People(y) ∧ BelongsTo(y,x) ∧ FeelProud(y,x) → evaluation(UNEXPECTED))"},
        {"role": "user", "content": "NL English sentence: ```you should ask too much of your family.```. Formula: ```∀x(People(x) ∧ Family(x) → ShouldAskTooMuch(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Family(x,y) ∧ AskTooMuch(y,x) → evaluation(GOOD))"},
        {"role": "user", "content": f"NL English sentence: ```{sentence}```. Formula: ```{formula}``` ."}]
    
    
    
    
    
    
    
    
    
    
    
    


# Ensuring positive evaluations, not equality and precise constants (457 tokens).
# CURRENTLY BEST
def prompt_6(sentence):
    return [
        {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
            Ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            Use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            Use variables in lowercase (e.g., 'x', 'y', 'z'), constants in uppercase (e.g., 'BAD', 'EMMA', 'FACEBOOK'), and predicates (e.g., 'People(x)', Friends(EMMA,y), Explains(x,y,z)).\
            Ensure that the scope of a predicate does not contain other predicates or nested structures.\
            Don't negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            The 'evaluation' predicate should not be negated, neither should the constant within the 'evaluation' predicate. Rather, the negation sentiment should be part of the constant, for example 'evaluation(NOT_GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
            Double check that all requirements specified above are met before giving your answer.\
            You get three examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "it's good to care about your family's history."},
        {"role": "assistant", "content": "∀x∀y(FamilyHistory(x,y) ∧ Cares(x,y) → evaluation(GOOD))"},
        {"role": "user", "content": "getting circumcised isn't normal."},
        {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
        {"role": "user", "content": "it's not ok to be frustrated when you work at the University of Bergen."},
        {"role": "assistant", "content": "∀x(WorksAt(x, UNIVERSITY_OF_BERGEN) ∧ Frustrated(x) → evaluation(NOT_OK))"},
        {"role": "user", "content": f"{sentence}"}  
    ] 
    

# Ensuring positive evaluations, not equality and precise constants.
# CURRENTLY BEST
def adjustment_prompt_4(sentence, formula):
    return [
        {"role":"system", "content": "You are a system tasked with adjusting a first-order formula to make sure it captures the sentiment expressed in the natural language sentence as accurately and complete as logically possible.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            If the first-order formula does not need correction, your answer should be only the formula as is.\
            Use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            Use variables in lowercase (e.g., 'x', 'y', 'z'), constants in uppercase (e.g., 'BAD', 'EMMA', 'FACEBOOK'), and predicates (e.g., 'People(x)', Friends(EMMA,y), Explains(x,y,z)).\
            Ensure that the scope of a predicate does not contain other predicates or any nested structures.\
            Don't negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            The 'evaluation' predicate should not be negated, neither should the constant within the 'evaluation' predicate. Rather, the negation sentiment should be part of the constant, for example 'evaluation(NOT_GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
            Double check that all requirements specified above are met before giving your answer.\
            You get three examples that show correct adjustment and the wanted output format."},
        {"role": "user", "content": "NL English sentence: people are not expected to love their family. Formula: ∀x∀y((People(x) ∧ BelongsTo(x,Family(y)) → ¬ExpectedToLove(x,y)) → evaluation(NOT_GOOD)"},
        {"role": "assistant", "content": "∀x∀y(People(x) ∧ Family(x,y) ∧ Love(x,y) → evaluation(NOT_EXPECTED))"},
        {"role": "user", "content": "NL English sentence: you should ask too much of your family. Formula: ∀x(People(x) ∧ Family(x) → ShouldAskTooMuch(x))"},
        {"role": "assistant", "content": "∀x∀y(Family(x,y) ∧ AskTooMuch(y,x) → evaluation(GOOD))"},
        {"role": "user", "content": "NL English sentence: it's taboo to admit that you don't like your step child. Formula: ∀x∀y(StepChild(x,y) ∧ Admit(x,DontLike(x,y)) → evaluation(TABOO))"},
        {"role": "assistant", "content": "∀x∀y(¬LikingStepChild(x) ∧ Admits(y,x) → evaluation(TABOO))"},
        {"role": "user", "content": f"NL English sentence: {sentence} Formula: {formula}"}]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# Prompt using less instructions and more examples (505 tokens)
def prompt_7(sentence):
    return [
        {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            You should use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            You get five examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "```it's good to care about your family's history.```"},
        {"role": "assistant", "content": "∀x∀y(FamilyHistory(x,y) ∧ Cares(x,y) → evaluation(GOOD))"},
        {"role": "user", "content": "```getting circumcised isn't normal.```"},
        {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
        {"role": "user", "content": "```you shouldn't get help if your anxiety is interfering with your daily life```"},
        {"role": "assistant", "content": "∀x∀y(Anxiety(x) ∧ InterfereWithDailyLife(x,y) ∧ ¬Help(y) → evaluation(GOOD))"},
        {"role": "user", "content": "```it's not ok to be frustrated when you work on amazon mechanical turk.```"},
        {"role": "assistant", "content": "∀x(WorksOn(x, AMAZONMECHANICALTURK) ∧ Frustrated(x) → evaluation(NOT_OK))"},
        {"role": "user", "content": "```you should not always get registration information when in an accident```"},
        {"role": "assistant", "content": "∀y∃x(Accident(x) ∧ In(y,x) ∧ ¬GetRegistrationInfo(y) → evaluation(GOOD))"},
        {"role": "user", "content": f"```{sentence}```"}  
    ] 
    
# Adjustment prompt using less instructions and more examples.
def adjustment_prompt_5(sentence, formula):
    return [
        {"role":"system", "content": "You are a system tasked with adjusting a first-order formula to make sure it captures the sentiment expressed in the natural language sentence as accurately and complete as logically possible.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            If the first-order formula does not need correction, your answer should be the formula as is.\
            You should use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            You get five examples that show correct adjustment and the wanted output format."},
        {"role": "user", "content": "NL English sentence: ```it is unexpected people will feel proud of their country.```. Formula: ```∀x(People(x) ∧ Country(x) → ¬ExpectedProudOf(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Country(x) ∧ People(y) ∧ BelongsTo(y,x) ∧ FeelProud(y,x) → evaluation(UNEXPECTED))"},
        {"role": "user", "content": "NL English sentence: ```it's good to be excited about getting your first paycheck.```. Formula: ```∀x(People(x) ∧ Excited(x, FirstPaycheck(x)) → evaluation(GOOD))``` ."},
        {"role": "assistant", "content": "∀x∀y((Paycheck(x) ∧ Gets(y,x) → ExcitedAbout(y,x)) → evaluation(GOOD))"},
        {"role": "user", "content": "NL English sentence: ```you shouldn't get help if your anxiety is interfering with your daily life```. Formula: ```∀x(People(x) ∧ Family(x) → ShouldAskTooMuch(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Anxiety(x) ∧ InterfereWithDailyLife(x,y) ∧ ¬Help(y) → evaluation(GOOD))"},
        {"role": "user", "content": "NL English sentence: ```getting circumcised isn't normal.```. Formula: ```∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))``` ."},
        {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
        {"role": "user", "content": "NL English sentence: ```it's taboo to admit that you don't like your step child.```. Formula: ```∀x∀y(StepChild(x,y) ∧ Admit(x,¬Likes(x,y)) → evaluation(TABOO))``` ."},
        {"role": "assistant", "content": "∀x∀y(¬LikingStepChild(x) ∧ Admits(y,x) → evaluation(TABOO))"},
        {"role": "user", "content": f"NL English sentence: ```{sentence}```. Formula: ```{formula}``` ."}]
    

# GPT enhanced prompt 6
def prompt_8(sentence):
    return [
    {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
        Ensure precise and valid first-order formulas conveying the sentiment of the original sentence accurately.\
        Use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
        Represent variables in lowercase (e.g., 'x', 'y', 'z'), constants in uppercase (e.g., 'BAD', 'EMMA', 'FACEBOOK'), and predicates (e.g., 'People(x)', Friends(x,y), Explains(x,y,z)).\
        Ensure that the scope of a predicate does not contain other predicates or nested structures.\
        Do not negate variables or constants, e.g., (evaluation(¬GOOD)).\
        Formulate each formula as an implication, where the conclusion is always an evaluation, for example, 'evaluation(GOOD)'.\
        The 'evaluation' predicate should not be negated. The negation sentiment should be part of the constant, for example, 'evaluation(NOT_GOOD)'.\
        When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
        When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
        'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
        You get three examples that show correct translations and the wanted output format."},
    
    {"role": "user", "content": "it's good to care about your family's history."},
    {"role": "assistant", "content": "∀x∀y(Cares(x,y) ∧ FamilyHistory(x,y) → evaluation(GOOD))"},
    
    {"role": "user", "content": "getting circumcised isn't normal."},
    {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
    
    {"role": "user", "content": "it's not ok to be frustrated when you work at the University of Bergen."},
    {"role": "assistant", "content": "∀x(WorksAt(x,UNIVERSITY_OF_BERGEN) ∧ Frustrated(x) → evaluation(NOT_OK))"},
    
    {"role": "user", "content": f"{sentence}"}  
]


def adjustment_prompt_6(sentence, formula):
    return [
    {"role": "system", "content": "You are a system tasked with adjusting a first-order formula to accurately capture the sentiment expressed in the given natural language sentence. \
        Ensure precise and valid first-order formulas. If the formula does not require correction, maintain it as is. \
        Utilize the symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','. \
        Avoid nested structures within predicate scopes. \
        Formulate each formula as an implication, where the conclusion is always an evaluation, e.g., 'evaluation(GOOD)'. \
        You will receive five examples demonstrating correct adjustments and the desired output format."},
    
    {"role": "user", "content": "NL English sentence: ```it is unexpected people will feel proud of their country.```. Formula: ```∀x(People(x) ∧ Country(x) → ¬ExpectedProudOf(x))```."},
    {"role": "assistant", "content": "∀x∀y(People(y) ∧ Country(x) ∧ FeelsProud(y, x) → evaluation(UNEXPECTED))"},
    
    {"role": "user", "content": "NL English sentence: ```it's good to be excited about getting your first paycheck.```. Formula: ```∀x(People(x) ∧ Excited(x, FirstPaycheck(x)) → evaluation(GOOD))```."},
    {"role": "assistant", "content": "∀x∀y((Paycheck(x) ∧ Gets(y, x) → ExcitedAbout(y, x)) → evaluation(GOOD))"},
    
    {"role": "user", "content": "NL English sentence: ```you shouldn't get help if your anxiety is interfering with your daily life```. Formula: ```∀x(Anxiety(x) ∧ InterfereWithDailyLife(x) → ¬GetHelp(x))```."},
    {"role": "assistant", "content": "∀x(Anxiety(x) ∧ InterfereWithDailyLife(x) ∧ ¬GetHelp(x) → evaluation(GOOD))"},
    
    {"role": "user", "content": "NL English sentence: ```getting circumcised isn't normal.```. Formula: ```∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))```."},
    {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
    
    {"role": "user", "content": "NL English sentence: ```it's taboo to admit that you don't like your stepchild.```. Formula: ```∀x∀y(StepChild(x, y) ∧ Admit(x, ¬Likes(x, y)) → evaluation(TABOO))```."},
    {"role": "assistant", "content": "∀x∀y(Admits(x, ¬Likes(x, y)) → evaluation(TABOO))"},
    
    {"role": "user", "content": f"NL English sentence: ```{sentence}```. Formula: ```{formula}```."},
]
    
    



# Try to fix issues:
# - Uses NOT in predicate instead of ¬:
#   NotPerformingUpToStandard(y) instead of ¬PerformingUpToStandard(y)
# - Does not connect actors with its actions/properties:
#   ∀x(Fetish(x)) instead of ∀x∀y(Fetish(x) ∧ HasFetish(x,y))
# - Expresses actions with one joint predicate instead of separating, which makes it less informative:
#   EatingBurger(x) instead of Burger(y) ∧ Eating(x,y)
# - Uses nested predicates:
#   Eats(Burgers(x))

# Expansion of prompt 6.
def prompt_9(sentence):
    return [
        {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
            Ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            Use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            Use variables in lowercase (e.g., 'x', 'y', 'z'), constants in uppercase (e.g., 'BAD', 'EMMA', 'FACEBOOK'), and predicates (e.g., 'People(x)', Friends(EMMA,y), Explains(x,y,z)).\
            Ensure that the scope of a predicate does not contain other predicates or nested structures.\
            Don't negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            The 'evaluation' predicate should not be negated, neither should the constant within the 'evaluation' predicate. Rather, the negation sentiment should be part of the constant, for example 'evaluation(NOT_GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
            Make sure each action/property that has an actor is connected to its actor, e.g. 'Thing(x) ∧ BelongsTo(x,y)'.\
            It's better to divide the formula into several predicates that express separate parts than combining all information into a single predicate, e.g. 'Man(x) ∧ Old(x)' insted of 'OldMan(x)'.\
            Double check that all requirements specified above are met before giving your answer.\
            You get three examples that show correct translations and the wanted output format."},
        
        {"role": "user", "content": "it's good to care about your family's history."},
        {"role": "assistant", "content": "∀x∀y(FamilyHistory(x,y) ∧ Cares(x,y) → evaluation(GOOD))"},
        
        {"role": "user", "content": "getting circumcised isn't normal."},
        {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
        
        {"role": "user", "content": "it's not ok to be frustrated when you work at the University of Bergen."},
        {"role": "assistant", "content": "∀x(WorksAt(x, UNIVERSITY_OF_BERGEN) ∧ Frustrated(x) → evaluation(NOT_OK))"},
        
        {"role": "user", "content": f"{sentence}"}  
    ] 
    

# Expansion of adjustment_prompt 4.
def adjustment_prompt_9(sentence, formula):
    return [
        {"role":"system", "content": "You are a system tasked with adjusting a first-order formula to make sure it captures the sentiment expressed in the natural language sentence as accurately and complete as logically possible.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            If the first-order formula does not need correction, your answer should be only the formula as is.\
            Use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            Use variables in lowercase (e.g., 'x', 'y', 'z'), constants in uppercase (e.g., 'BAD', 'EMMA', 'FACEBOOK'), and predicates (e.g., 'People(x)', Friends(EMMA,y), Explains(x,y,z)).\
            Ensure that the scope of a predicate does not contain other predicates or any nested structures.\
            Don't negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            The 'evaluation' predicate should not be negated, neither should the constant within the 'evaluation' predicate. Rather, the negation sentiment should be part of the constant, for example 'evaluation(NOT_GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
            Make sure each action/property that has an actor is connected to its actor, e.g. 'Thing(x) ∧ BelongsTo(x,y)'.\
            It's better to divide the formula into several predicates that express separate parts than combining all information into a single predicate, e.g. 'Man(x) ∧ Old(x)' insted of 'OldMan(x)'.\
            Double check that all requirements specified above are met before giving your answer.\
            You get three examples that show correct adjustment and the wanted output format."},
        
        {"role": "user", "content": "NL English sentence: people are not expected to love their family. Formula: ∀x∀y((People(x) ∧ BelongsTo(x,Family(y)) → ¬ExpectedToLove(x,y)) → evaluation(NOT_GOOD)"},
        {"role": "assistant", "content": "∀x∀y(People(x) ∧ Family(x,y) ∧ Love(x,y) → evaluation(NOT_EXPECTED))"},
        
        {"role": "user", "content": "NL English sentence: you shouldn't drink someone's beer. Formula: ∀x∀y(People(x) ∧ Beer(y) ∧ Drink(x,y) → evaluation(BAD))"},
        {"role": "assistant", "content": "∀x∀y∀z(Beer(y) ∧ BelongsTo(y,x) ∧ Drink(z,y) → evaluation(BAD))"},
        
        {"role": "user", "content": "NL English sentence: it's taboo to admit that you don't like your step child. Formula: ∀x∀y(StepChild(x,y) ∧ Admit(x,DontLike(x,y)) → evaluation(TABOO))"},
        {"role": "assistant", "content": "∀x∀y(¬LikingStepChild(x) ∧ Admits(y,x) → evaluation(TABOO))"},
        
        {"role": "user", "content": f"NL English sentence: {sentence} Formula: {formula}"}]


