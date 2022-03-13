import hashlib

#implentation of get bytes, returns the array of 
#bytes for each character in a given word
def get_bytes(s, k):
    count = 0
    byte_array = []
    hasher = hashlib.sha256()
    hasher.update(s.encode("utf-8"))
    hash=hasher.digest()
    for i in range(len(s)):
        if count<k:
            byte_array.append(hash[count])
        count+=1
    remainder = k - len(s)
    for i in range(remainder):
        byte_array.append(255)
    return byte_array

#1a - gets the first three bytes of 'hello'
one_a = get_bytes("hello", 3)
print(one_a)

#1b - implementation of hash table using sha-256
def hash_table(text_file):
    with open(text_file, 'r') as f:
        readfile = f.read()
        table = []
        split_text = readfile.split(" ")
        for i in range(256):
            table.append([[],[]])
        for i in range(len(split_text)):
            first_byte = get_bytes(split_text[i], 1)
            if (split_text[i] in table[first_byte[0]][0]):
                index = table[first_byte[0]][0].index(split_text[i])
                table[first_byte[0]][1][index] += 1
            else:
                table[first_byte[0]][0].append(split_text[i])
                table[first_byte[0]][1].append(1)
        return table

def lookup(table, word):
    byte = get_bytes(word, 1)[0]
    index = table[byte][0].index(word)
    return table[byte][1][index]


#1c - gets the count of words from streams.txt
stream_count= hash_table('stream.txt')

print(lookup(stream_count, "the"))
print(lookup(stream_count, "are"))
print(lookup(stream_count, "sydney"))
print(lookup(stream_count, "london"))

#1d - modified hash table implementation to produce byte count
def hash_bytes(table):
    count = 0
    for i in table:
        for wordlist in i[0]:
            count += len(wordlist)
        count += len(i[1]) * 4
    return count

print(hash_bytes(stream_count))

#2a - implementation of cms, lines that have been commented out indicate tests 
#for why test on 'her' is producing 1203 instead of 1186. I got the values of
#53, 76, and 191 from manually testing the byte values of 'her'. 
#I don't know why my data is producing 1203 instead of 1186 for 'her' while 
#producing the proper amounts for 'paris' and 'well'.

def cms(text_file, word):
    with open(text_file, 'r') as f:
        readfile = f.read()
        split_text = readfile.split(" ")
        table2 = []
        for r in range(5):
            table = []
            for i in range(256):
                table.append(0)
            table2.append(table)
        #hercount0 = 0
        #hercount1 = 0
        #hercount2 = 0
        for i in range(len(split_text)):
            byte = get_bytes(split_text[i], 5)
            for d in range(5):
                table2[d][byte[d]]+=1
                #if(d==0 and byte[d]==53):
                    #hercount0+=1
                #if(d==1 and byte[d]==76):
                    #hercount1+=1
                #if(d==2 and byte[d]==191):
                    #hercount2+=1
        #if(word=='her'):
            #print(hercount0)
            #print(hercount1)
            #print(hercount2)
        values = []
        word_bytes = get_bytes(word, 5)
        for i in range(5):
            values.append(table2[i][word_bytes[i]])
        return min(values)

print(cms('stream.txt', "paris"))
print(cms('stream.txt', "her"))
print(cms('stream.txt', "well"))
print(cms('stream.txt', "the"))
print(cms('stream.txt', "are"))
print(cms('stream.txt', "sydney"))
print(cms('stream.txt', "london"))

def conservative_cms(text_file, word):
    with open(text_file, 'r') as f:
        readfile = f.read()
        split_text = readfile.split(" ")
        table2 = []
        count = 0
        for r in range(5):
            table = []
            for i in range(256):
                table.append(0)
            table2.append(table)
        for i in range(len(split_text)):
            byte = get_bytes(split_text[i], 5)
            counts = []
            for x in range(5):
                counts.append(table2[x][byte[x]])
            min_count = min(counts)
            for d in range(5):
                if(table2[d][byte[d]]==min_count):
                    table2[d][byte[d]]+=1
        values = []
        word_bytes = get_bytes(word, 5)
        for i in range(5):
            values.append(table2[i][word_bytes[i]])
        return min(values)

print(conservative_cms('stream.txt', "the"))
print(conservative_cms('stream.txt', "are"))
print(conservative_cms('stream.txt', "sydney"))
print(conservative_cms('stream.txt', "london"))
