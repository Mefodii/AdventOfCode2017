# --- Part Two ---
# For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two
# words that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged
# to form any other word in the passphrase.
#
# For example:
#
#   -   abcde fghij is a valid passphrase.
#   -   abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
#   -   a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
#   -   iiii oiii ooii oooi oooo is valid.
#   -   oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
#
# Under this new system policy, how many passphrases are valid?


# Prepare libs
import time

# Prepare input
start = time.time()
f = open('../Input/Day4-A.txt', 'r')

# Process
valid_passphrasess = 0
for line in f:
    original_passphrase_list = line.split()
    processed_passhrase_list = original_passphrase_list.copy()

    for i in range(0, len(processed_passhrase_list)):
        processed_passhrase_list[i] = ''.join(sorted(processed_passhrase_list[i]))
    processed_passhrase_list = list(set(processed_passhrase_list))

    if len(original_passphrase_list) - len(processed_passhrase_list) == 0:
        valid_passphrasess += 1

print("##--RESULT--##")
print("Number of valid passphrases: " + str(valid_passphrasess))


# Execution time
end = time.time()
print(end - start)