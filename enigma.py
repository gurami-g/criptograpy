import math 

def score_likelihood(decrypted_text, perc_dict):
    total_likelihood = 0
    for i in range(len(decrypted_text) - 1):
        pair_likelihood = perc_dict[decrypted_text[i]][decrypted_text[i+1]]
        total_likelihood += pair_likelihood
    return total_likelihood

def shuffle_pair(current_dict):
    a, b = random.sample(current_dict.keys(), 2)
    proposed_dict = current_dict.copy()
    proposed_dict[a], proposed_dict[b] = proposed_dict[b], proposed_dict[a]
    return proposed_dict

def eval_proposal(proposed_score, current_score):
    diff = proposed_score - current_score
    diff = min(1, diff)
    diff = max(-1000, diff)
    ratio = math.exp(diff)
    if ratio >= 1 or ratio > np.random.uniform(0,1):
        return True
    else:
        return False 
    
def decrypt_MCMC(cyphered_text, perc_dict, iters, known_chars, verbose = False):
    best_score = []
    best_text = []
    
    # Step 1 - Create a random decryption key 
    current_key = create_rand_crypt(known_chars)
    current_dict = str_to_key(known_chars, crypt_keys)
    # Step 2 - Decrypt the text
    current_decrypted = apply_dict(cyphered_text, current_dict)
    # Step 3 - Score the (log) likelihood of the decrypted text
    current_score = score_likelihood(current_decrypted, perc_dict)
    
    for i in range(iters):
        # Step 4 - Randomly shuffle two letter pairings
        proposed_dict = shuffle_pair(current_dict)
        # Step 5 - Decrypt the text again with the new key
        proposed_decrypted = apply_dict(cyphered_text, proposed_dict)
        # Step 6 - Recompute the log-likelihood score
        proposed_score = score_likelihood(proposed_decrypted, perc_dict)
        # Step 7 - Evaluate the difference
        # If the likelihood has improved, accept the new key
        # If the likelihood hasn't improved but the value exceeds a randomly drawn value between 0-1, also accept the new key
        # Otherwise, reject the new key
        if eval_proposal(proposed_score, current_score):
            current_dict = proposed_dict
            current_score = proposed_score
            current_decrypted = proposed_decrypted
        # Repeat the above for the given amount of iterations
        
        if i % 500 == 0:
            best_score.append(current_score)
            best_text.append(current_decrypted)
        
        if verbose == True and i % 1000 == 0:
            print("Iteration: " + str(i) + ". Score: " + str(current_score) + '. Message: ' + current_decrypted[0:70])
            
    
            
    return current_dict, best_score, best_text

