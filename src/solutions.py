from helpers import *
from cryptography_functions import *
import string


##############
# Q1
##############

# print(vigenere("Attack at dawn", "lemon"))

# print(vigenere("Lxfopvefrnhr",   "lemon", decode=True))


#################
# Q3
#################

### BOB ###
ALICE_KEYS = dict(zip(["pk", "sk", "factors"], RSA_key_generator()))
BOB_MESSAGE = "the quick brown fox jumps over the lazy Dog"
VIGENERE_KEY = vigenere_key_generator(200)

normed = normalise_string(BOB_MESSAGE)

message_encoded = vigenere(normed, VIGENERE_KEY)
print(message_encoded)

# Bob uses Alice's public key to encode the v-key
encrypted_key = encrypt_rsa(VIGENERE_KEY, ALICE_KEYS.get("pk"))


### ALICE ###
decrypted_key = decrypt_rsa(encrypted_key, ALICE_KEYS.get("pk"), ALICE_KEYS.get("sk"))
recovered_key = "".join(convert_to_text(m) for m in decrypted_key)

print(recovered_key == VIGENERE_KEY)

message_decoded = vigenere(message_encoded, recovered_key, decode=True)
print(message_decoded)






###################
# Q4
###################

print("\n\n\n\n\nQ4\n")

N_BIGRAMS = 400

#### BOB #####

# bob makes his bigrams
bigram_masks = create_bigram_masks(N_BIGRAMS)

# he masks his messsage with them
masked = mask_string_bigrams(normed, bigram_masks)
print(masked)

# vigerene cyphers the masked message, hiding letter frequency
masked_encoded = vigenere(masked, VIGENERE_KEY)

# add the bigrams in an understandable format to the key
hybrid_key = create_hybrid_key(VIGENERE_KEY, bigram_masks)

# encrypt this hybird string with RSA
encrypted_key = encrypt_rsa(hybrid_key, ALICE_KEYS.get("pk"))

# pretend now Bob has sent the masked messsage and the encrypted key to Alice

##### ALICE #######

# Alice decrypts key+bigrams using RSA secret key
decrypted_key = decrypted_key = decrypt_rsa(encrypted_key, ALICE_KEYS.get("pk"), ALICE_KEYS.get("sk"))
text_key = "".join(convert_to_text(m) for m in decrypted_key)

# she is not done, need to seperate the text key
v_key, mappings = read_hybrid_key(text_key)

# decrypt the vigerene cypher with the key
recovered_masked = vigenere(masked_encoded, v_key, decode=True)

# she unmasks the decrypted message
recovered_message = unmask_string_bigrams(recovered_masked, mappings).strip()

print("The message is:")
print(recovered_message)
print(normed)
if recovered_masked == normed: print("poggies")

print()

print(convert_to_integer(r"a:{ak,ab,fk}&b:{fe,gq}"))
print(convert_to_text(132158451435657439334922421607028343646858954670567805))

# for letter, bigset in bigram_masks.items():
#     print(set_to_string(bigset))

hybrid = create_hybrid_key("lemon", bigram_masks)
# print(hybrid.split("&"))

v_key, mappings =read_hybrid_key(hybrid)

# print(v_key)
# print(mappings == bigram_masks)