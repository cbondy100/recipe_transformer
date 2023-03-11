from recipe_scrapers import scrape_me
import re
import nltk
import nltk.tag, nltk.data
import spacy
from spacy.symbols import ORTH, POS, NOUN, VERB

nlp_spacy = spacy.load("en_core_web_sm")



descriptions = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'broken', 'chilled',
		'chopped', 'cleaned', 'coarse', 'cold', 'cooked', 'cool', 'cooled', 'cored', 'creamed', 'crisp', 'crumbled',
		'crushed', 'cubed', 'cut', 'deboned', 'deseeded', 'diced', 'dissolved', 'divided', 'drained', 'dried', 'dry',
		'fine', 'firm', 'fluid', 'fresh', 'frozen', 'grated', 'grilled', 'ground', 'halved', 'hard', 'hardened',
		'heated', 'heavy', 'juiced', 'julienned', 'jumbo', 'large', 'lean', 'light', 'lukewarm', 'marinated',
		'mashed', 'medium', 'melted', 'minced', 'near', 'opened', 'optional', 'packed', 'peeled', 'pitted', 'popped',
		'pounded', 'prepared', 'pressed', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'ripe', 'roasted',
		'roasted', 'rolled', 'rough', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'separated',
		'shredded', 'sifted', 'skinless', 'sliced', 'slight', 'slivered', 'small', 'soaked', 'soft', 'softened',
		'split', 'squeezed', 'stemmed', 'stewed', 'stiff', 'strained', 'strong', 'thawed', 'thick', 'thin', 'tied', 
		'toasted', 'torn', 'trimmed', 'wrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned', 'patted', 'raw', 'flaked', 'deveined', 'shelled', 'shucked', 'crumbs',
		'halves', 'squares', 'zest', 'peel', 'uncooked', 'butterflied', 'unwrapped', 'unbaked', 'warmed', 'unseasoned',
        'toasted', 'bunch', 'pre-cooked', 'all-purpose', 'taste']

conjunction_list = ['and', 'or', 'but', 'for', 'to']

cooking_utensils = ['apple corker', 'apple cutter', 'baster', 'biscuit cutter', 'blow torch', 'pot', 'pan', 'bowls', 'pans', 'tong', 'skillet', 'wok', 'knife',
        'bottle opener', 'bowl', 'bread knife', 'baking sheet', 'butter curler', 'cheese knife', 'cherry pitter', 'chinois', 'cleaver',
        'colander', 'strainer', 'corkscrew', 'crab cracker', 'dough scraper', 'egg piercer', 'egg poacher', 'egg timer', 'fillet knife',
        'fish scaler', 'scale', 'flour sifter', 'food mill', 'funnel', 'garlic press', 'grater', 'ladle', 'spoon', 'spatula', 'fork',
        'lemon squeezer', 'lobster pick', 'measuring cup', 'meat grinder', 'thermometer', 'melon baller', 'mezzaluna', 'nutcracker',
        'oven mitt', 'oven glove', 'peeler', 'pepper mill', 'pizza cutter', 'potato masher', 'pot-holder', 'poultry shears', 'rolling pin', 'scissors',
        'tongs', 'whisk', 'wooden spoon', 'zester', 'cutting board', 'waffle iron', 'oven', 'microwave', 'blender', 'stove', 'aluminum foil', 'foil', 'baking dish', 
        'plastic wrap', 'wrap', 'dish', 'board', 'cutting board', 'grill', 'smoker']

def preprocessSpacy():
    # retagging known entities for our spacy POS tagger

    ruler = nlp_spacy.get_pipe("attribute_ruler")
    patterns = [
        { 
            "patterns": [[{"ORTH": "cook"}], [{"ORTH": "season"}]], 
            "attrs": {"POS" : "VERB"},
        }
    ]
    ruler.add_patterns(patterns)

class recipeStep:
    def __init__(self, step_num, step_text):
        self.step_num = step_num
        self.step_text = step_text
        # this should store ingredient object
        self.ingredients = []
        self.materials = []
        self.actions = []
    def __str__(self):
        return "Step " + str(self.step_num) + ": " + self.step_text + "\n"
        

class RecipeIngredient:
    def __init__(self, init_text):
        self.i_text = init_text
        self.ingredient = []
        self.quantity = 0
        self.unit = ""
        self.descrips = []

    def __str__(self):
        return "Text: " + self.i_text + "\n" + "Ingredient: " + str(self.ingredient) + "\n" + "Quantity: " + str(self.quantity) + "\n" + "Unit: " + str(self.unit) + "\n" + "Descrips: " + str(self.descrips) + "\n"

def makePlural(list):
    plural_list = []
    for i in list:
        plural_list.append(i + "s")
    return plural_list

def isFloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def buildIngredient(i_text):
    measures = ["cup", "teaspoon", "tablespoon", "ounce", "fluid ounce", "quart", "pint", "gallon", "package"]

    i_class = RecipeIngredient(i_text)

    my_regex = "\s\(.*?\)"
    new_str = re.sub(my_regex, "", i_text)

    #checking for commas with descrips
    if "," in new_str:
        clause = new_str.split(", ")
        i_class.descrips.append(clause[1])
        new_str = clause[0]

    i_list = new_str.split(" ")
    # check if its a number first

    if isFloat(i_list[0]):
        i_class.quantity = i_list[0]
        i_list.pop(0)

    for element in i_list:
        #print(element)
        if element in measures or element in makePlural(measures):
            i_class.unit = element
        elif element in descriptions:
            i_class.descrips.append(element)
        else:
            if element not in conjunction_list:
                i_class.ingredient.append(element)

    return i_class
        
def recipe_ingredients(scraper):
    ingredients = scraper.ingredients()
    print(ingredients)
    global all_ingredients
    all_ingredients = []
    for ing in ingredients:
        # pass 
        all_ingredients.append(buildIngredient(ing))

    return

def setStepFields(step):
    step_text = step.step_text.lower()
    spacy_doc = nlp_spacy(step_text)
    print("STEP: " + step_text)

    for token in spacy_doc:
        print("TEXT: " + token.text, "POS: " + token.pos_, "TAG: " + token.tag_)
        if token.pos_ == "VERB":
            step.actions.append(token.text)
        if token.pos_ == "NOUN" and token.text in cooking_utensils:
            step.materials.append(token.text)

    print('\n')
    return

#builds a step class array
def buildStepsArray(scraper):
    #prolly want to keep track of where each action and ingredient falls in the step (later)
    instructions = scraper.instructions_list()
    steps_array = []

    for c, element in enumerate(instructions):
        #print("Loading Step " + str(c+1))
        step = recipeStep(c+1, element)
        setStepFields(step)
        steps_array.append(step)

    return steps_array

if __name__ == "__main__":

    preprocessSpacy()

    link = "https://www.allrecipes.com/recipe/42890/turkey-a-la-king/"
    scraper = scrape_me(link, wild_mode = True)

    recipe_ingredients(scraper)

    for i in all_ingredients:
        print(i)

    buildStepsArray(scraper)

