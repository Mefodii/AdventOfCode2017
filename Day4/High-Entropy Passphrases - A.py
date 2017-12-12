# --- Day 4: High-Entropy Passphrases ---
# A new system policy has been put in place that requires all accounts to use a passphrase instead of simply a password.
# A passphrase consists of a series of words (lowercase letters) separated by spaces.
#
# To ensure security, a valid passphrase must contain no duplicate words.
#
# For example:
#
#   -   aa bb cc dd ee is valid.
#   -   aa bb cc dd aa is not valid - the word aa appears more than once.
#   -   aa bb cc dd aaa is valid - aa and aaa count as different words.
#
# The system's full passphrase list is available as your puzzle input. How many passphrases are valid?


# Prepare libs
import time

# Prepare input
start = time.time()
f = open('../Input/Day4-A.txt', 'r')

# Process
valid_passphrasess = 0
for line in f:
    original_passphrase_list = line.split()
    processed_passhrase_list = list(set(original_passphrase_list))
    if len(original_passphrase_list) - len(processed_passhrase_list) == 0:
        valid_passphrasess += 1

print("##--RESULT--##")
print("Number of valid passphrases: " + str(valid_passphrasess))


# Execution time
end = time.time()
print(end - start)