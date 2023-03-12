from recipe_scrapers import scrape_me
import re
import nltk
from nltk.tokenize import sent_tokenize
import nltk.tag, nltk.data
import spacy
from spacy.symbols import ORTH, POS, NOUN, VERB

nlp_spacy = spacy.load("en_core_web_sm")

to_veg_link = "https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/"
fat_to_h_link = "https://www.allrecipes.com/recipe/16167/beef-bourguignon-i/"

descriptions = ['baked', 'beaten', 'blanched', 'boiled', 'boiling', 'boned', 'breaded', 'brewed', 'broken', 'chilled',
		'chopped', 'cleaned', 'coarse', 'cold', 'cooked', 'cool', 'cooled', 'cored', 'creamed', 'crisp', 'crumbled',
		'crushed', 'cubed', 'cut', 'deboned', 'deseeded', 'diced', 'dissolved', 'divided', 'drained', 'dried', 'dry',
		'fine', 'firm', 'fluid', 'fresh', 'frozen', 'grated', 'grilled', 'halved', 'hard', 'hardened',
		'heated', 'heavy', 'juiced', 'julienned', 'jumbo', 'large', 'lean', 'light', 'lukewarm', 'marinated',
		'mashed', 'medium', 'melted', 'minced', 'near', 'opened', 'optional', 'packed', 'peeled', 'pitted', 'popped',
		'pounded', 'prepared', 'pressed', 'pureed', 'quartered', 'refrigerated', 'rinsed', 'ripe', 'roasted',
		'roasted', 'rolled', 'rough', 'scalded', 'scrubbed', 'seasoned', 'seeded', 'segmented', 'separated',
		'shredded', 'sifted', 'skinless', 'sliced', 'slight', 'slivered', 'small', 'soaked', 'soft', 'softened',
		'split', 'squeezed', 'stemmed', 'stewed', 'stiff', 'strained', 'strong', 'thawed', 'thick', 'thin', 'tied', 
		'toasted', 'torn', 'trimmed', 'wrapped', 'vained', 'warm', 'washed', 'weak', 'zested', 'wedged',
		'skinned', 'gutted', 'browned', 'patted', 'raw', 'flaked', 'deveined', 'shelled', 'shucked', 'crumbs',
		'halves', 'squares', 'zest', 'peel', 'uncooked', 'butterflied', 'unwrapped', 'unbaked', 'warmed', 'unseasoned',
        'toasted', 'bunch', 'pre-cooked', 'taste', 'no-boil']

conjunction_list = ['and', 'or', 'but', 'for', 'to']

cooking_utensils = ['apple corker', 'apple cutter', 'baster', 'biscuit cutter', 'blow torch', 'pot', 'pan', 'bowls', 'pans', 'tong', 'skillet', 'wok', 'knife',
        'bottle opener', 'bowl', 'bread knife', 'baking sheet', 'butter curler', 'cheese knife', 'cherry pitter', 'chinois', 'cleaver',
        'colander', 'strainer', 'corkscrew', 'crab cracker', 'dough scraper', 'egg piercer', 'egg poacher', 'egg timer', 'fillet knife',
        'fish scaler', 'scale', 'flour sifter', 'food mill', 'funnel', 'garlic press', 'grater', 'ladle', 'spoon', 'spatula', 'fork',
        'lemon squeezer', 'lobster pick', 'measuring cup', 'meat grinder', 'thermometer', 'melon baller', 'mezzaluna', 'nutcracker',
        'oven mitt', 'oven glove', 'peeler', 'pepper mill', 'pizza cutter', 'potato masher', 'pot-holder', 'poultry shears', 'rolling pin', 'scissors',
        'tongs', 'whisk', 'wooden spoon', 'zester', 'cutting board', 'waffle iron', 'oven', 'microwave', 'blender', 'stove', 'aluminum foil', 'foil', 'baking dish', 
        'plastic wrap', 'wrap', 'dish', 'board', 'cutting board', 'grill', 'smoker', 'saucepan', 'mixer']

cooking_actions = ["preheat", "chop", "mince", "dice", "slice", "julienne", "grate", "peel", "crush", "mash", "puree", "blend", "whisk", "beat",
        "stir", "mix", "knead", "roll", "cut", "trim", "season", "marinate", "brine", "roast", "bake", "broil", "grill", "fry", "saute", "simmer",
        "boil", "steam", "poach", "blanch", "deglaze", "reduce", "glaze", "baste", "stuff", "garnish", "plate", "serve", "store", "freeze", "defrost",
        "thaw", "clean", "sanitize", "set up", "clean up", "heat", "discard", "pour"]

meat_to_veg = {
    'beef': 'portobello mushrooms',
    'chicken': 'tofu',
    'pork': 'jackfruit',
    'turkey': 'tofu',
    'lamb': 'eggplant',
    'fish': 'tofu',
    'shrimp': 'tofu',
    'bacon': 'tempeh bacon',
    'sausage': 'vegan sausage made from soy, seitan, or tempeh',
    'ground beef': 'textured vegetable protein (TVP)',
    'steak': 'portobello mushrooms',
    'meatballs': 'vegan meatballs made from TVP, seitan, or lentils',
    'hot dogs': 'vegan hot dogs made from soy, seitan, or tempeh',
    'ribs': 'seitan ribs',
    'meatloaf': 'vegan meatloaf made from lentils, TVP, or seitan',
    'chorizo': 'vegan chorizo made from soy or seitan',
    'ham': 'seitan ham',
    'duck': 'seitan duck',
    'beef jerky': 'vegan jerky made from soy, mushroom, or seitan',
    'chicken nuggets': 'vegan nuggets made from soy, seitan, or tempeh'}

veg_to_meat = {
    'portobello mushrooms': 'steak',
    'tofu': 'chicken',
    'jackfruit': 'pork',
    'eggplant': 'lamb',
    'seitan': 'chicken',
    'lentils': 'ground beef',
    'black beans': 'beef',
    'textured vegetable protein (TVP)': 'ground beef',
    'chickpeas': 'griound turkey',
    'mushrooms': 'beef',
    'tempeh': 'chicken',
    'tempeh bacon': 'bacon',
    'coconut bacon': 'bacon',
    'mushroom bacon': 'bacon',
    'vegan sausage': 'sausage',
    'vegan meatballs': 'meatballs',
    'seitan ribs': 'ribs',
    'vegan meatloaf': 'meatloaf',
    'vegan chorizo': 'chorizo',
    'seitan ham': 'ham',
    'seitan duck': 'duck',
    'vegan jerky': 'beef jerky',
}

fat_to_health = {
    'sour cream': 'greek yogurt',
    'cheese': 'low fat cheese',
    'butter': 'coconut oil',
    'vegetable oil': 'coconut oil',
    'canola oil': 'avocado oil',
    'dairy milk': 'almond milk',
    'whole milk': 'almond milk',
    '2% milk': 'almond milk',
    'milk': 'almond milk',
    'all-purpose flour': 'whole wheat flour',
    'white rice': 'brown rice',
    'pasta': 'zucchini noodles (zoodles)',
    'rice': 'cauliflower rice',
    'mayonnaise or butter': 'avocado',
    'eggs': 'chia seeds',
    'ground beef': 'black beans',
    'meat': 'tofu',
    'white potatoes': 'sweet potatoes',
    'lettuce in salads': 'spinach',
    'chocolate': 'unsweetened cocoa powder',
    'ground beef': 'ground turkey',
    'bread crumbs': 'rolled oats',
    'sugar': 'honey or maple syrup'
}

health_to_fat = {
    'greek yogurt': 'sour cream',
    'low fat cheese': 'cheese',
    'coconut oil': 'butter',
    'avocado oil': 'canola oil',
    'almond milk': 'whole milk',
    'whole wheat flour': 'all-purpose flour',
    'brown rice': 'white rice',
    'zucchini noodles (zoodles)': 'pasta',
    'cauliflower rice': 'rice',
    'chia seeds': 'eggs',
    'black beans': 'ground beef',
    'tofu': 'meat',
    'sweet potatoes': 'white potatoes',
    'spinach': 'lettuce',
    'unsweetened cocoa powder': 'milk chocolate',
    'ground turkey': 'ground beef',
    'rolled oats': 'bread crumbs',
    'maple syrup': 'corn syrup',
    'honey': 'sugar'
}


to_italian = {
    "butter": "olive oil",
    "beef": "italian sausage",
    "duck": "italian sausage",
    "chorizo": "italian sausage",
    "cheese": "mozzarella",
    "herbs": "basil, oregano, rosemary, or thyme",
    "garlic": "fresh garlic",
    "rice": "risotto",
    "wine": "chianti",
    "vinegar": "balsamic vinegar",
    "heavy cream": "whole milk or half-and-half",
    "soy sauce": "balsamic vinegar",
    "cilantro": "parsley or basil",
    "ground beef": "ground italian sausage",
    "peanut oil": "olive oil",
    "sour cream": "ricotta cheese",
    "brown sugar": "honey",
    "soy milk": "almond milk",
    "ginger": "garlic",
    "white sugar": "raw sugar or honey"
}

to_thai = {
    "butter": "Coconut oil or palm oil",
    "chicken": "lemongrass chicken",
    "beef": "thai basil beef",
    "lamb": "massaman curry with lamb",
    "cheese": "coconut milk",
    "basil": "Thai basil",
    "tomatoes": "tamarind paste",
    "pasta": "rice noodles",
    "vinegar": "rice vinegar"
}

to_gluten_free = {
    "wheat flour": "almond flour",
    "rice": "quinoa",
    "couscous": "quinoa",
    "soy sauce": "tamari or coconut aminos",
    "tortillas": "corn tortillas",
    "pasta": "gluten-free pasta",
    "noodles": "sweet potato noodles",
    "oatmeal": "quinoa flakes"
}

gluten_free_to_gluten = {
    "almond flour": "wheat flour",
    "quinoa": "rice",
    "tamari": "soy sauce",
    "oconut aminos": "soy sauce",
    "corn tortillas": "tortillas",
    "gluten-free pasta": "pasta",
    "sweet potato noodles": "noodles",
    "quinoa flakes": "oatmeal"
}

to_lactose_free = {
    "milk substitutes": "almond milk",
    "butter substitutes": "vegan butter",
    "cheese substitutes": "vegan cheese",
    "cream substitutes": "coconut cream",
    "yogurt substitutes": "coconut yogurt",
    "ice cream substitutes": "non-dairy ice cream",
    "sour cream substitutes": "coconut cream",
    "condensed milk substitutes": "coconut condensed milk",
    "whipped cream substitutes": "coconut cream",
    "chocolate substitutes": "dark chocolate",
    "protein powder substitutes": "plant-based protein powders",
    "sweetened condensed milk substitutes": "coconut sweetened condensed milk"
}

lactose_free_to_dairy = {
    "almond milk": "milk substitutes",
    "vegan butter": "butter substitutes",
    "vegan cheese": "cheese substitutes",
    "coconut cream": "sour cream",
    "coconut yogurt": "yogurt substitutes",
    "non-dairy ice cream": "ice cream substitutes",
    "dark chocolate": "chocolate substitutes",
    "plant-based protein powders": "protein powder substitutes"
}




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
        return "Step " + str(self.step_num) + ": " + self.step_text
    
    def printStepIng(self):
        print("Step " + str(self.step_num))
        print("INGREDIENTS")
        for i in self.ingredients:
            print(i)
        print("\n")

class RecipeIngredient:
    def __init__(self, init_text):
        self.i_text = init_text
        self.ingredient = ""
        self.quantity = "NA"
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
        return float(str)
    except ValueError:
        return "NA"

def buildIngredient(i_text):
    measures = ["cup", "teaspoon", "tablespoon", "ounce", "fluid ounce", "quart", "pint", "gallon", "package", "jar", "can", "container", "pound", "clove"]

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

    i_class.quantity = isFloat(i_list[0])
    if i_class.quantity != "NA":
        i_list.pop(0)

    class_ingredient_list = []

    for element in i_list:
        #print(element)
        if element in measures or element in makePlural(measures):
            i_class.unit = element
        elif element in descriptions:
            i_class.descrips.append(element)
        else:
            if element not in conjunction_list:
                class_ingredient_list.append(element)

    i_class.ingredient = (" ").join(class_ingredient_list)

    return i_class
        
def recipe_ingredients(scraper):
    ingredients = scraper.ingredients()
    #print(ingredients)
    global all_ingredients
    global all_ingredients_text
    all_ingredients_text = []
    all_ingredients = []
    for ing in ingredients:
        # pass 
        ing_class = buildIngredient(ing)
        all_ingredients.append(ing_class)
        #print(ing_class.ingredient)
        all_ingredients_text.append(ing_class.ingredient)

    return


def DoubleIt(all_ingredients):
    for i in all_ingredients:
        if i.quantity != "NA":
                bool = False
                if i.quantity <= 1:
                    bool = True
                temp = i.quantity
                i.quantity = temp*2
                if i.quantity > 1 and bool == True:
                    if i.unit != "":
                        i.unit = i.unit + "s"

def HalfIt(all_ingredients):
    for i in all_ingredients:
        if i.quantity != "NA":
                bool = False
                if i.quantity >= 1:
                    bool = True
                temp = i.quantity
                i.quantity = temp/2
                if i.quantity < 1 and bool == True:
                    if i.unit != "":
                        i.unit = i.unit[0:len(i.unit)-1]
                    
def Transform(type, steps_list):
    #for i in all_ingredients:
    #    for j in type.keys():
    #        if i.ingredient == j:
    #           i.i_text = i.i_text.replace(i.ingredient, type[j])
    #            i.ingredient = type[j]

    for step in steps_list:
        print(step.step_text)
        for i in step.ingredients:
            print(i.ingredient)
            try:
                print("TRANSFORM! Autobots, Roll Out!")
                print(i.ingredient)
                i.i_text = i.i_text.replace(i.ingredient, type[i.ingredient])
                step.step_text = step.step_text.replace(i.ingredient, type[i.ingredient])
                i.ingredient = type[i.ingredient]
                print(i.i_text)
            except:
                continue
                

def findIngredient(text):
    for i in all_ingredients:
        if text in i.ingredient:
            return i

#helper to check if word is already present in a list
def checkList(text, list):
    is_present = False
    for element in list:
        if text in element.lower():
            is_present = True
    return is_present

def setStepFields(step):
    banned_words = ["heat", "sauce", "degrees", "c", "f", "temperature"]

    step_text = step.step_text.lower()
    spacy_doc = nlp_spacy(step_text)
   # print("STEP: " + step_text)
    #print(all_ingredients_text)

    step_ingredients = []
    step_mats = []
    step_acts = []

    for chunk in spacy_doc.noun_chunks:
        #print("TEXT: " + chunk.text, "ROOT: " + chunk.root.text, "ROOT DEP: " + chunk.root.dep_, "ROOT HEAD: " + chunk.root.head.text)
        if chunk.root.text in cooking_utensils:
            step_mats.append(chunk.text)
            step.materials.append(chunk.text)
        if chunk.text in all_ingredients_text:
            step_ingredients.append(chunk.text)
            step.ingredients.append(findIngredient(chunk.text))
        elif checkList(chunk.root.text, all_ingredients_text) and not any(word in chunk.text for word in banned_words):
            step_ingredients.append(chunk.text)
            step.ingredients.append(findIngredient(chunk.text))


    for token in spacy_doc:
        #print("TEXT: " + token.text, "POS: " + token.pos_, "TAG: " + token.tag_)
        if (token.text in cooking_actions or token.pos_ == "VERB") and token.text not in step_acts:
            step_acts.append(token.text)
            step.actions.append(token.text)
        elif token.pos_ == "NOUN" and token.text in cooking_utensils:
            if not checkList(token.text, step_mats):
                step_mats.append(token.text)
                step.materials.append(chunk.text)
        elif token.text in all_ingredients_text and not checkList(token.text, step_ingredients):
            # if we are here, we have found an ingredient
            # add the corresponding ingredient object
            #step.ingredients.append(findIngredient(token.text))
            #if not checkList(token.text, step_ingredients):
            step_ingredients.append(token.text)
            step.ingredients.append(findIngredient(token.text))
        elif checkList(token.text, all_ingredients_text) and token.text not in banned_words:
            step_ingredients.append(token.text)
            step.ingredients.append(findIngredient(token.text))

        #elif checkList(token.text, all_ingredients_text):
            #step_ingredients.append(token.text)
            
    
    #print("STEP MATS: " + str(step_mats))
    print("STEP INGS: " + str(step_ingredients))
    #print("STEP ACTIONS: " + str(step_acts))

    
    #print('\n')
    return

def printSteps(steps_array):
    for i in steps_array:
        print(i)
        i.printStepIng()


#builds a step class array
def buildStepsArray(scraper):
    #prolly want to keep track of where each action and ingredient falls in the step (later)
    instructions = scraper.instructions_list()
    new_instruction_list = []
    for instruction in instructions:
        new_instruction_list += sent_tokenize(instruction)


    steps_array = []

    for c, element in enumerate(new_instruction_list):
        #print("Loading Step " + str(c+1))
        step = recipeStep(c+1, element)
        setStepFields(step)
        steps_array.append(step)

    return steps_array

def prettyPrint(steps_array):
    print("Ingredients:\n")
    for i in all_ingredients:
        print(i.i_text, "\n")

    print("\nRecipe Steps:\n")
    for step in steps_array:
        print(step, "\n")


def runChatbot(steps_array):
    print("Welcome to Recipe Extravaganza 2.0!\n")
    #printHelp()
    booli = True
    while booli:
        try:
            recipe = input("Please give me a link to a recipe:\n")
            if recipe == "quit":
                print("Gone so soon? Come back with a recipe, have a nice day.")
                return
            scraper = scrape_me(recipe, wild_mode = True)
            recipe_ingredients(scraper)
            title = scraper.title()
            steps_array = buildStepsArray(scraper)
            booli = False
        except:
            #print("\nWhat, are you baked? You didn't give us a good link! Please try again\n")
            print("\nHmm not sure I can read that link. We recommend you give us a recipe from one of these websites:\nFoodNetwork.com\nAllRecipes.com\nTasteOfHome.com\nDelish.com\n")
       
    while True:
        query = input("")
        #query = related(query)
        if query == "1":
            Transform(meat_to_veg, steps_array)
            title = ("Vegetarian ")
        elif query == "2":
            Transform(veg_to_meat, steps_array)
        elif query == "3":
            Transform(fat_to_health, steps_array)
        elif query == "4":
            Transform(health_to_fat, steps_array)
        elif query == "5":
            Transform(to_italian, steps_array)
        elif query == "6":
            Transform(to_thai, steps_array)
        elif query == "7":
            Transform(to_gluten_free, steps_array)
        elif query == "8":
            Transform(gluten_free_to_gluten, steps_array)
        elif query == "9":
            Transform(to_lactose_free, steps_array)
        elif query == "10":
            Transform(lactose_free_to_dairy, steps_array)
        elif query == "11":
            DoubleIt(all_ingredients)
        elif query == "12":
            HalfIt(all_ingredients)
        
        print(title)
        prettyPrint(steps_array)
        
if __name__ == "__main__":

    preprocessSpacy()

    #link = fat_to_h_link
    #scraper = scrape_me(link, wild_mode = True)


    #recipe_ingredients(scraper)
    #print(all_ingredients_text)

    #steps_array = buildStepsArray(scraper)
    #printSteps(steps_array)

    runChatbot()

    #for i in all_ingredients:
    #    print(i)

    #for i in all_ingredients:
    #    print(i)

    #Transform(fat_to_health, steps_array)

    #print("START OF TRANFROM STEPS")
    #printSteps(steps_array)

   #for i in all_ingredients:
    #    print(i)
   

    #for i in all_ingredients:
    #    if i.ingredient == "onion":
    #        i.ingredient = "FUCKER"

    #printSteps(steps_array)

    
    #print("VEGETARIAN TRANSFORM")

    #for i in all_ingredients:
        #print(i)

    #print("DOUBLING RECIPE")
    #DoubleIt(all_ingredients)

    #for i in all_ingredients:

    #    print(i)

