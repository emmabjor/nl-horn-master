def initial_prompt(sentence):
    return [
        {"role":"system", "content": 
            
        """You are a system tasked with translating sentences from natural language English to first-order logic formulas.
        Ensure precise and valid first-order formulas that convey the explicit sentiment of the original sentence as accurately as possible.
        Use the following symbols: "∨", "∧", "→", "↔", "∀", "∃", "¬", "(", ")", ",".
        Use variables in lowercase (e.g., "x", "y", "z"), constants in uppercase (e.g., "BAD", "EMMA", "FACEBOOK"), and predicates 
            (e.g., "People(x)", "Friends(EMMA,y)", "Explains(x,y,z)").
        Ensure that the scope of a predicate does not contain other predicates or nested structures.
        Don't negate variables or constants.
        Each formula should be formulated as an implication, where the conclusion should always be "evaluation(GOOD)" or "evaluation(BAD)".
        Use the negation-symbol in the antecedent when predicates express negation, 
            such that "do/can/will not <predicate>" translates to "¬<Predicate>()".
        When "you should" is stated it implies the consequence "evaluation(GOOD)".
        When "you shouln't" is stated it implies the consequence "evaluation(BAD)".
        When something is positively stated, such as "it's ok" or "it's expected", it implies the consequence "evaluation(GOOD)".
        When something is negatively stated, such as "it's rude" or "it's not expected", it implies the consequence "evaluation(BAD)".
        When "others" or "someone else" is mentioned, these should be represented with existential quantifier, 
            such that "other people" translates to "∃x(People(x)).
        When "sometimes" is expressed, all quantifiers should be existential, 
            such that "sometimes people eat meat" translates to "∃x∃y(People(x) ∧ Meat(y) ∧ Eat(x,y))".
        Make sure each action/property that has an actor is connected to its actor, 
            e.g. "your things" translates to "Thing(x) ∧ BelongsTo(x,y)", or "your family" translates to "FamilyOf(x,y)".
        It's better to divide the formula into several predicates that express separate parts rather than combining all information into a single predicate, 
            e.g. "old man" translates to "Man(x) ∧ Old(x)".
        Double check that all requirements specified above are met before giving your answer.
        Try reading out loud your translation to make sure the sentiment aligns with the English sentence before giving your answer. 
            Adjust if sentiment does not align.
        You get three examples that show correct translations and the wanted output format."""},
        
        {"role": "user", "content": "it's fine to care about your family's history."},
        {"role": "assistant", "content": "∀x∀y∀z(FamilyOf(x,y) ∧ HistoryOf(z,x) ∧ CaresAbout(y,z) → evaluation(GOOD))"},
        
        {"role": "user", "content": "you shouldn't talk to other people about your fetishes."},
        {"role": "assistant", "content": "∀x∀y∃z(Fetish(x) ∧ BelongsTo(x,y) ∧ People(z) ∧ TalkToAbout(y,z,x) → evaluation(BAD))"},
        
        {"role": "user", "content": "it's not ok to be frustrated when you work at the University of Bergen."},
        {"role": "assistant", "content": "∀x(WorksAt(x, UNIVERSITY_OF_BERGEN) ∧ Frustrated(x) → evaluation(BAD))"},
        
        {"role": "user", "content": f"{sentence}"}  
    ] 
    

def adjustment_prompt(sentence, formula):
    return [
        {"role":"system", "content": """You are a system tasked with correcting a first-order formula to make sure it captures 
            the explicit sentiment expressed in the natural language sentence as accurately and complete as logically possible.
        If the first-order formula does not need correction, you should answer with the formula exactly as it is without any changes 
            or explanations.
        Do not change the evaluation constant unless the evaluation sentiment expressed in the natural language sentence is different 
            from the one in the provided formula.
        Use the following symbols: "∨", "∧", "→", "↔", "∀", "∃", "¬", "(", ")", ",".
        Use variables in lowercase (e.g., "x", "y", "z"), constants in uppercase (e.g., "BAD", "EMMA", "FACEBOOK"), 
            and predicates (e.g., "People(x)", "Friends(EMMA,y)", "Explains(x,y,z)").
        Ensure that the scope of a predicate does not contain other predicates or any nested structures.
        Don't negate variables or constants.
        Each formula should be formulated as an implication, where the conclusion should always be "evaluation(GOOD)" or 
            "evaluation(BAD)".
        Use the negation-symbol in the antecedent when predicates express negation, such that "do/can/will not <predicate>" 
            translates to "¬<Predicate>()".
        When "you should" is stated it implies the consequence "evaluation(GOOD)".
        When "you shouln't" is stated it implies the consequence "evaluation(BAD)".
        When something is positively stated, such as "it's ok" or "it's expected", it implies the consequence "evaluation(GOOD)".
        When something is negatively stated, such as "it's rude" or "it's not expected", it implies the consequence "evaluation(BAD)".
        When "others" or "someone else" is mentioned, this should be represented with existential quantifier, 
            such that "other people" translates to "∃x(People(x))".
        When "sometimes" is expressed, all quantifiers should be existential, 
            such that "sometimes people eat meat" translates to "∃x∃y(People(x) ∧ Meat(y) ∧ Eat(x,y))".
        Make sure each action/property that has an actor is connected to its actor,  
            e.g. "someone's things" translates to "Thing(x) ∧ BelongsTo(x,y)", or "your family" translates to "FamilyOf(x,y)".
        It's better to divide the formula into several predicates that express separate parts rather than combining all 
            information into a single predicate, e.g. "old man" translates to "Man(x) ∧ Old(x)".
        Double check that all requirements specified above are met before giving your answer.
        Try reading out loud your translation to make sure the sentiment aligns with the English sentence before giving your answer. 
            Adjust if sentiment does not align.
        Once again, if the first-order formula does not need correction, you should answer with the formula exactly as it is 
            without any changes or explanations.
        You get three examples that show correct adjustment and the wanted output format."""},
        
        {"role": "user", "content": "NL English sentence: it is ok to kiss someone else's significant other. \
                                    Formula: ∃x∀y∀z(HasSignificantOther(x,y) ∧ Kiss(z,y) → evaluation(GOOD))"},
        {"role": "assistant", "content": "∃x∀y∀z(HasSignificantOther(x,y) ∧ Kiss(z,y) → evaluation(GOOD))"},
        
        {"role": "user", "content": "NL English sentence: you shouldn't drink someone's beer. \
                                    Formula: ∀x∀y(People(x) ∧ Beer(y) ∧ Drink(x,y) → evaluation(BAD))"},
        {"role": "assistant", "content": "∀x∀y∀z(Beer(y) ∧ BelongsTo(y,x) ∧ Drink(z,y) → evaluation(BAD))"},
        
        {"role": "user", "content": "NL English sentence: it's ok to not join in on fun activities. \
                                    Formula: ∀x∀y(Activity(x) ∧ Fun(x) ∧ NotJoinInOn(y,x) → evaluation(GOOD))"},
        {"role": "assistant", "content": "∀x∀y(Activity(x) ∧ Fun(x) ∧ ¬JoinInOn(y,x) → evaluation(GOOD))"},
        
        {"role": "user", "content": f"NL English sentence: {sentence} Formula: {formula}"}]
