#####################################
#  Kasiski Examination              #
#  @Cole Hanson                     #
#  @Erik Carleson                   #
#####################################
import sys

def caesar(c,r):
    '''
    Solves a caesar encryption and returns the key
    '''
    max = 0
    k=0
    for i in range(0,26):
        cur_max = testHelper(i, c, r)
        if cur_max > max:
            max = cur_max
            k = i

    return k

def test(k,c,r):
    '''
    calculate key qualities by looking at char. frequencies.
    We mainly use this function to calculate the frequencies in Reference text.
    After doing this once we use testHelper which does everything the same as here,
    but without calculating the frequencies of the reference text again.
    '''

    #string of alpha chars
    alpha = "abcdefghijklmnopqrstuvwxyz"

    #initialize dictionary for word frequency in ciphertext
    c_freq = {}
    #initialize dictionary for word frequency in reference_text
    global r_freq
    r_freq = {}


    #iterate through ciphertext and calculate char frequency
    for i in c:
        if i.lower() not in alpha:
            pass
        elif i.lower() in c_freq:
            c_freq[i.lower()] += 1
        else:
            c_freq[i.lower()] = 1

    #iterate through reference_text and calculate char frequency
    for i in r:
        if i.lower() not in alpha:
            pass
        elif i.lower() in r_freq:
            r_freq[i.lower()] += 1
        else:
            r_freq[i.lower()] = 1


    ciphertext_length = len(c)
    reference_text_length = len(r)
    r_char_frac = 0
    c_char_frac = 0
    sum = 0

    for i in range(0,26):
        j = (i - k) % 26
        r_char_frac = r_freq.get(chr(i+97), 0)/reference_text_length
        c_char_frac = c_freq.get(chr(j+97), 0)/ciphertext_length

        product= r_char_frac * c_char_frac

        sum += product
        sum = sum%26

    return sum

def testHelper(k,c,r):
        '''
        helper function for test that calculates char. frequencies in
        the ciphertext (not the reference text) and finds optimal shift
        '''
        #string of alpha chars
        alpha = "abcdefghijklmnopqrstuvwxyz"

        #initialize dictionary for word frequency in ciphertext
        c_freq = {}
        #iterate through ciphertext and calculate char frequency
        for i in c:
            if i.lower() not in alpha:
                pass
            elif i.lower() in c_freq:
                c_freq[i.lower()] += 1
            else:
                c_freq[i.lower()] = 1


        ciphertext_length = len(c)
        reference_text_length = len(r)
        r_char_frac = 0
        c_char_frac = 0
        sum = 0

        for i in range(0,26):
            j = (i - k) % 26
            r_char_frac = r_freq.get(chr(i+97), 0)/reference_text_length
            c_char_frac = c_freq.get(chr(j+97), 0)/ciphertext_length

            product= r_char_frac * c_char_frac

            sum += product
            sum = sum%26

        return sum

def kasiskiHelper(c):
    '''
    finds the optimal key length for a ciphertext
    '''
    c = c.lower()

    alpha = "abcdefghijklmnopqrstuvwxyz"

    gram_freq = {}
    gram_index = {}

    #get trigrams in ciphertext
    for i in range(0, len(c)-2):
        cur_trigram = c[i:i+3]
        #cur_bigram = c[i:i+2]

        if cur_trigram in gram_freq:
            gram_freq[cur_trigram] +=1

        elif cur_trigram not in gram_freq:
            gram_freq[cur_trigram] = 1

        if cur_trigram in gram_index:
            gram_index[cur_trigram].append(i)

        elif cur_trigram not in gram_index:
            gram_index[cur_trigram] = [i]

    #calculate distance of repeated trigrams
    distances = []
    for trigram in gram_freq:
        if gram_freq[trigram] > 10:
            #print(gram_index[trigram])
            #print(trigram)
            for i in range(0, gram_freq[trigram] - 1):
                for j in range(0, gram_freq[trigram] - 1):
                    if j == i: pass

                    else:
                        distances.append(gram_index[trigram][j]-gram_index[trigram][i])

    #calculate number of factors for each distance
    fac_percentage =[1,1]
    num_distances = len(distances)
    highest_divider = 1
    for i in range(2, 101):
        num_divides = 0
        for number in distances:
            if number % i == 0:
                num_divides += 1
        fac_percentage.append(num_divides/num_distances)
    #print(fac_percentage)

    #find the key length by looking at factors of distances
    i=2
    factor=1
    while i<101:
        if fac_percentage[i]*i > 1.5*fac_percentage[factor]*factor:
            factor = i
            i = 2*factor
            #print(factor)
        else:
            i += factor

    return factor

def decipher_setup(key_len,c,r):
    '''
    find the key and decipher the ciphertext
    '''
    solution_string= ''
    char_n = []

    #put chars into string based on index in respective key
    for j in range(0,key_len):
        char_n.append('')
        for k in range(0,len(c)):
            if k%key_len == j:
                char_n[j] += c[k]

    #break caesar on each individual string
    for l in range(0, len(char_n)):
        ans = caesar(char_n[l],r)
        solution_string += str(chr(ans+97))

    #print("key:" + solution_string)

    decrypted_text = ""
    #string of alpha chars
    alpha = "abcdefghijklmnopqrstuvwxyz"

    #decrypt text with key
    for j in range(0, len(c)):
        index_of_key= j% len(solution_string)
        if c[j].lower() not in alpha:
            decrypted_text += c[j]
        else:
            cap = False
            if c[j].isupper():
                cap = True
            letter = c[j].lower()
            glyph = ord(letter) - 97
            glyph = (glyph + ord(solution_string[index_of_key])-97) % 26
            glyph = chr(glyph + 97)
            if cap == True:
                glyph = glyph.upper()
            decrypted_text += glyph

    #print(decrypted_text)
    return decrypted_text

def kasiski(c,r):
    '''
    Function that uses the Kasiski method to decipher a vigenere encoded text by calling our other functions.
    '''
    key_len = kasiskiHelper(c)

    test(0,c,r)

    solution = decipher_setup(key_len,c,r)

    print(solution)

    return solution

def main():
    #open reference text from file
    with open(sys.argv[2], 'r') as f:
        reference_text = f.read()

    with open(sys.argv[1], 'r') as f:
        ciphertext = f.read()

    kasiski(ciphertext,reference_text)


if __name__ =="__main__":
    main()
