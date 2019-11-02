#########################
#  Cipher breaker       #
#  @Cole Hanson         #
#  @Erik Carleson       #
#########################
import sys

def test(k,c,r):
    '''
    calculate key qualities by looking at char. frequencies.
    For caesar and Viginere, we mainly use this function to calculate the
    frequencies in Reference text. After doing this once we use testHelper which
    does everything the same as here, but without calculating the frequencies of
    the reference text again.
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

    #calculate char freq percentages in ref. text and ciphertext
    for i in range(0,26):
        j = (i - k) % 26
        r_char_frac = r_freq.get(chr(i+97), 0)/reference_text_length
        c_char_frac = c_freq.get(chr(j+97), 0)/ciphertext_length

        product= r_char_frac * c_char_frac

        sum += product
        sum = sum%26

    #print(sum)
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

        #calculate char freq percentages in ref. text and ciphertext
        for i in range(0,26):
            j = (i - k) % 26
            r_char_frac = r_freq.get(chr(i+97), 0)/reference_text_length
            c_char_frac = c_freq.get(chr(j+97), 0)/ciphertext_length

            product= r_char_frac * c_char_frac

            sum += product
            sum = sum%26

        return sum


def breakCaesar(c,r):
    '''
    decrypt text based on key
    '''
    test(0,c,r)
    k = caesarHelper(c,r)

    decrypted_text = ""
    #string of alpha chars
    alpha = "abcdefghijklmnopqrstuvwxyz"

    #iterate through ciphertext an decrypt with shift
    for j in c:
        if j.lower() not in alpha:
            decrypted_text += j
        else:
            cap = False
            if j.isupper():
                cap = True
            j= j.lower()
            glyph = ord(j) - 97
            glyph = (glyph + k) % 26
            glyph = chr(glyph + 97)
            if cap == True:
                glyph = glyph.upper()
            decrypted_text += glyph


    print(decrypted_text)
    return decrypted_text

def caesarHelper(c,r):
    '''
    helper function for breakCaesar() that does not call test
    '''
    max = 0
    k=0

    #find optimal key
    for i in range(0,26):
        cur_max = testHelper(i, c, r)
        if cur_max > max:
            max = cur_max
            k = i

    return k

def breakVigenere(c,r):
    '''
    breaks Vigenere cipher by testing different keys of different lengths
    '''
    test(0,c,r)
    keys = []

    #iterate through key lengths 1-100
    for i in range(1,101):
        solution_string= ''
        char_n = []
        key_qualities = []
        #put chars into string based on index in respective key
        for j in range(0,i):
            char_n.append('')
            for k in range(0,len(c)):
                if k%i == j:
                    char_n[j] += c[k]

        #break caesar on each individual string
        for l in range(0, len(char_n)):
            ans = caesarHelper(char_n[l],r)
            quality = testHelper(ans,char_n[l],r)
            key_qualities.append(quality)
            solution_string += str(chr(ans+97))

        #finding a quality for the key
        sum = 0
        for m in range(0,len(key_qualities)):
            sum += key_qualities[m]

        avg_quality = sum/ len(key_qualities)
        keys.append([solution_string,avg_quality])

    max = 0
    solution= ""
    for n in range(0, len(keys)):
        if keys[n][1] > max:
            max = keys[n][1]
            solution = keys[n][0]

    #print(solution)

    decrypted_text = ""
    #string of alpha chars
    alpha = "abcdefghijklmnopqrstuvwxyz"


    #decrypt text with key
    for j in range(0, len(c)):
        index_of_key= j% len(solution)
        if c[j].lower() not in alpha:
            decrypted_text += c[j]
        else:
            cap = False
            if c[j].isupper():
                cap = True
            letter = c[j].lower()
            glyph = ord(letter) - 97
            glyph = (glyph + ord(solution[index_of_key])-97) % 26
            glyph = chr(glyph + 97)
            if cap == True:
                glyph = glyph.upper()
            decrypted_text += glyph

    print(decrypted_text)
    return decrypted_text

def main():
    #open reference text from file
    with open(sys.argv[2], 'r') as f:
        reference_text = f.read()
    #open ciphertext from file
    with open(sys.argv[1], 'r') as f:
        ciphertext = f.read()

    #test(0, ciphertext, reference_text)
    #breakCaesar(ciphertext, reference_text)
    #breakVigenere(ciphertext, reference_text)


if __name__ == "__main__":
    main()
