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
    


# Ensuring positive evaluations, not equality and precise constants.
def prompt_6(sentence):
    return [
        {"role":"system", "content": "You are a system tasked with translating sentences in natural language English to first-order logic formulas.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            You should use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should use variables in lowercase (e.g. 'x'), constants in uppercase (e.g. 'BAD') and predicates (e.g. 'People(x)').\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            You should not negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            The 'evaluation' predicate should not be negated, neither should the constant within the 'evaluation' predicate. Rather, the negation sentiment should be part of the constant, for example 'evaluation(NOT_GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
            You get two examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "```it's good to care about your family's history.```"},
        {"role": "assistant", "content": "∀x∀y(FamilyHistory(x,y) ∧ Cares(x,y) → evaluation(GOOD))"},
        {"role": "user", "content": "```getting circumcised isn't normal.```"},
        {"role": "assistant", "content": "∀x(GettingCircumcised(x) → evaluation(NOT_NORMAL))"},
        {"role": "user", "content": f"```{sentence}```"}
        
    ] 
    

# Ensuring positive evaluations, not equality and precise constants.
def adjustment_prompt_4(sentence, formula):
    return [
        {"role":"system", "content": "You are a system tasked with adjusting a first-order formula to make sure it captures the sentiment expressed in the natural language sentence as accurately and complete as logically possible.\
            You should ensure precise and valid first-order formulas that convey the sentiment of the original sentence as accurately as possible.\
            You should use the following symbols: '∨', '∧', '→', '↔', '∀', '∃', '¬', '(', ')', ','.\
            You should use variables in lowercase (e.g. 'x'), constants in uppercase (e.g. 'BAD') and predicates (e.g. 'People(x)').\
            You should ensure that the scope of a predicate does not contain other predicates or nested structures.\
            You should not negate variables or constants, e.g. (evaluation(¬GOOD)).\
            Each formula should be formulated as an implication, where the conclusion should always be an evaluation, for example 'evaluation(GOOD)'\
            The 'evaluation' predicate should not be negated, neither should the constant within the 'evaluation' predicate. Rather, the negation sentiment should be part of the constant, for example 'evaluation(NOT_GOOD)'\
            When 'you should' is stated, it implies a universally good evaluation ('evaluation(GOOD)').\
            When 'it's nice' is stated, it implies a consequence interpreted as 'evaluation(NICE)'.\
            'evaluation(NOT_GOOD)' is not the same as 'evaluation(BAD)'.\
            You get two examples that show correct translations and the wanted output format."},
        {"role": "user", "content": "NL English sentence: ```it is unexpected people will feel proud of their country.```. Formula: ```∀x(People(x) ∧ Country(x) → ¬ExpectedProudOf(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Country(x) ∧ People(y) ∧ BelongsTo(y,x) ∧ FeelProud(y,x) → evaluation(UNEXPECTED))"},
        {"role": "user", "content": "NL English sentence: ```you should ask too much of your family.```. Formula: ```∀x(People(x) ∧ Family(x) → ShouldAskTooMuch(x))``` ."},
        {"role": "assistant", "content": "∀x∀y(Family(x,y) ∧ AskTooMuch(y,x) → evaluation(GOOD))"},
        {"role": "user", "content": f"NL English sentence: ```{sentence}```. Formula: ```{formula}``` ."}]