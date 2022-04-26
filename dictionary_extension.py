

from matplotlib.pyplot import stem


original_dictionary_path = "idioms_wiktionary.txt"
modified_dictionary_path = "idioms_wiktionary_augmented.txt"

VERBS_ONLY = False
IGNORE_CUSTOM_DERIVATIONS = True



# Use a Python Dictionary to store word groups and their modified forms
morphology_dictionary_path = "catvar_english_morphology.txt"
stem_derivations = {}
root = {}

# Load the morphological dictionary
print("Loading morphemes...")
for line in open(morphology_dictionary_path, "r"):
    line = line.strip().split()
    is_verb = line[2][1] == "V"
    if VERBS_ONLY and not is_verb:
        continue
    if line[1] not in stem_derivations:
        stem_derivations[line[1]] = []
    stem_derivations[line[1]].append(line[0])
    root[line[0]] = line[1]

additional_derivations_path = "custom_derivations.txt"
print("Loading custom derivations...")
if not IGNORE_CUSTOM_DERIVATIONS:
    for line in open(additional_derivations_path, "r"):
        line = line.strip().split() 
        if(len(line) < 2):
            continue
        while len(line) > 2:
            line[0] = line[0] + " " + line[1]
            line.pop(1)
        if line[1] not in stem_derivations:
            stem_derivations[line[1]] = []
        stem_derivations[line[1]].append(line[0])
        root[line[0]] = line[1]

def recursive_search(words):
    if len(words) == 0:
        return [""]
    else:
        prev_result = recursive_search(words[1:])
        if words[0] not in root:
            root[words[0]] = words[0]
            stem_derivations[words[0]] = [words[0]]
        curr_root = root[words[0]] 
        result = []
        for word in prev_result:
            for derivation in stem_derivations[curr_root]:
                result.append(derivation + " " + word)
        return result
            


# Get file for outputing new dictionary
output_file = open(modified_dictionary_path, "w")


# Load the original dictionary
print("Beginning dictionary modification...")
current_line = 0
for line in open(original_dictionary_path, "r"):
    line = line.strip().split()
    print("\rCurrent line: {}".format(current_line), end="")
    current_line += 1
    all_derivations = recursive_search(line)
    for derivation in all_derivations:
        derivation.replace("n't", " n't")
        derivation.replace("'ve", " 've")
        derivation.replace("'ll", " 'll")
        derivation.replace("'d", " 'd")
        derivation.replace("'s", " 's")
        derivation.replace("'re", " 're")
        derivation.replace("'m", " 'm")
        derivation.replace("'em", " 'em")
        derivation.replace("gonna", "gon na")
        derivation.replace("gotta", "got ta")
        output_file.write(derivation + "\n")

output_file.close()

    
    


