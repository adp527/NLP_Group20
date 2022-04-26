from turtle import st
import jsonlines
import string
import ahocorasick as ac

dictionary_path = "idioms_wiktionary_augmented.txt"
corupus_path = "magpie_unfiltered.jsonl"

A = ac.Automaton()


# Load dictionary
idx = 0
with open(dictionary_path, "r") as f:
    for line in f:
        x = line.strip()
        A.add_word(x, (idx, x))
        idx += 1

A.make_automaton()

# Load corpus
instances = 0
total_identified = 0
accurately_identified = 0
curr = 0
print("Running tests\n")
with jsonlines.open(corupus_path) as reader:
    for instance in reader:
        curr += 1
        print("\r{}".format(curr), end="")
        if instance["confidence"] == 1.0:
            instances += 1
            idiom_begin = instance["offsets"][0][0]
            idiom_end = instance["offsets"][-1][1] - 1
            context_list = instance["context"]

            # keep set of used start indices, to ensure only one match is found for each candidate
            used_start_indices = {}

            # Aho-Corasick is rediculously fast
            for context in context_list:
                context = context.lower()
                for end_index, (insert_order, original_value) in A.iter(context):
                    start_index = end_index - len(original_value) + 1
                    if start_index not in used_start_indices:
                        used_start_indices[start_index] = end_index
                        total_identified += 1
                    elif end_index > used_start_indices[start_index]:
                        used_start_indices[start_index] = end_index
                        #In the final version, where we need to return the actual indices, we can defer to the longest match

                    if idiom_begin == start_index and idiom_end == end_index:   
                        accurately_identified += 1
                    elif idiom_begin == start_index and idiom_end - 1 == end_index and context[idiom_end] == '\u2019':
                        accurately_identified += 1

print("")
print(str(accurately_identified) + " " + str(total_identified))
        

print("")
print("Precision: " + str(accurately_identified/total_identified))
print("Recall: " + str(accurately_identified/instances))
