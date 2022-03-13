import collections
from collections import defaultdict
import time

class Node:
    def __init__(self, freq, set, left=None, right=None):
        self.code = '' # huffman code for current node
        self.freq = freq
        self.set = set # set of characters
        self.left = left
        self.right = right

# takes a tree and builds a mapping for encoding/decoding
def BuildDict(map, node, val=''):
    huffmanCode = val + str(node.code)

    if(node.left):
        BuildDict(map, node.left, huffmanCode)
    if(node.right):
        BuildDict(map, node.right, huffmanCode)
    
    # if node is a leaf node
    if(not node.left and not node.right):
        map[node.set].append(huffmanCode)


def BuildHuffmanCodeTree(characters, frequencies):
    nodes = []

    for x in range(len(characters)):
        nodes.append(Node(frequencies[x], characters[x]))

    # make sure that there are still two nodes in the list
    while len(nodes) >= 2:
        nodes = sorted(nodes, key=lambda node: node.freq)

        left = nodes[0]
        right = nodes[1]

        left.code = 0
        right.code = 1
        combined = Node(left.freq + right.freq, left.set + right.set, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(combined)

    return nodes[0]

# need to create two versions of encode and decode - one version with the map, another just traversing the tree
# you can use contains on the node's set to check what letters are in the left or right branch

def Encode(message, tree):
    output = ""
    curr = tree
    for char in message:
        while char in curr.left.set or char in curr.right.set:
            if(char in curr.left.set):
                output += '0'
                curr = curr.left
                if not curr.left or not curr.right:
                    break
            elif(char in curr.right.set):
                output += '1'
                curr = curr.right
                if not curr.left or not curr.right:
                    break
        curr = tree
    #prints the number of bits for the encoding
    print("Encoding bit size: " + str(len(output)))
    #prints the encoding itself
    print(output)
    return output

def Decode(message, root):
    output = ""
    curr = root
    for char in message:
        if char == '0':
            curr = curr.left
        elif char == '1':
            curr = curr.right
        if curr.left == None and curr.right == None:
            output += ''.join(curr.set)
            curr = root
    print(output)
    return output


def EncodeUsingMap(message, hashmap):
    encodedstring = ''
    for char in message:
        encodedstring+=hashmap.get(char)[0]
    print(encodedstring)
    return encodedstring

def DecodeUsingMap(encodedstring, hashmap):
    decodedstring = ''
    start_index = 0
    end_index = 1
    max_index = len(encodedstring)
    reversed_map = {hashmap[k][0]: k for k in hashmap}
    while(start_index != max_index):
        if encodedstring[start_index:end_index] in reversed_map:
            decodedstring += reversed_map[encodedstring[start_index:end_index]]
            start_index = end_index
        end_index += 1
    print(decodedstring)
    return decodedstring


if __name__ == "__main__":
    #message1
    test1 = BuildHuffmanCodeTree(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], [24,21,15,17,16,18,22,16,15,15,24,21,26,20,13,14,23,21,18,24,19,20,18,28,13,19])
    Encode("ecyfxsgqkruiqtdlxxlgstmtgbpxaaeqkjmwyhdmzjdvcgrxnutnioqxkenxxnlqjmhtctlcfbnbwrbkzwrdwupvzvhfhgtjiwnighpunymsqnjhjwapvzqzmjktsqbxgenxpsufklsmukhdrvqtymxflmskgvhagloxemdsqmpbxvbtwrlxtyquqkenixiehoyascorgabommjusczezwgvcvnhjlglqfpcxrgeysxzzwmtvvtamknodkuuavdkslffrbhiwjbnldafngmfrwmnwufyfrdlzedlhbmqzltkhrmkltaoflageqiluutvdchsxnrkaokfajsvldyzanwbfvapixpoqtbtiuzwpmiwvqjczxrgurtibobtvaapbobydznqkudrkvgzfjyrkucsqeshjxxbplxpeymwgtcakgrqhcxgcjasuqrrakluiczeqxfsaeytxmrmdpoxtweamkzammizbgbkbavwfdtnoqnikxgv", test1)
    map = collections.defaultdict(list)
    BuildDict(map, test1)
    sum1 = 0
    for i in [24,21,15,17,16,18,22,16,15,15,24,21,26,20,13,14,23,21,18,24,19,20,18,28,13,19]:
        sum1 += i
    print("Total number of characters in message 1: " + str(sum))
    #message2
    test2 = BuildHuffmanCodeTree(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ',',','-','.',';',':','(',')',"'"],[384,67,109,212,581,125,94,293,293,7,32,146,100,337,354,70,4,304,295,429,123,45,118,3,83,2,1001,94,14,21,12,3,1,1,3])
    Encode("it was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of light, it was the season of darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to heaven, we were all going direct the other way- in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only. there were a king with a large jaw and a queen with a plain face, on the throne of england; there were a king with a large jaw and a queen with a fair face, on the throne of france. in both countries it was clearer than crystal to the lords of the state preserves of loaves and fishes, that things in general were settled for ever. it was the year of our lord one thousand seven hundred and seventy-five. spiritual revelations were conceded to england at that favoured period, as at this. mrs. southcott had recently attained her five-and-twentieth blessed birthday, of whom a prophetic private in the life guards had heralded the sublime appearance by announcing that arrangements were made for the swallowing up of london and westminster. even the cock-lane ghost had been laid only a round dozen of years, after rapping out its messages, as the spirits of this very year last past (supernaturally deficient in originality) rapped out theirs. mere messages in the earthly order of events had lately come to the english crown and people, from a congress of british subjects in america: which, strange to relate, have proved more important to the human race than any communications yet received through any of the chickens of the cock-lane brood. france, less favoured on the whole as to matters spiritual than her sister of the shield and trident, rolled with exceeding smoothness down hill, making paper money and spending it. under the guidance of her christian pastors, she entertained herself, besides, with such humane achievements as sentencing a youth to have his hands cut off, his tongue torn out with pincers, and his body burned alive, because he had not kneeled down in the rain to do honour to a dirty procession of monks which passed within his view, at a distance of some fifty or sixty yards. it is likely enough that, rooted in the woods of france and norway, there were growing trees, when that sufferer was put to death, already marked by the woodman, fate, to come down and be sawn into boards, to make a certain movable framework with a sack and a knife in it, terrible in history. it is likely enough that in the rough outhouses of some tillers of the heavy lands adjacent to paris, there were sheltered from the weather that very day, rude carts, bespattered with rustic mire, snuffed about by pigs, and roosted in by poultry, which the farmer, death, had already set apart to be his tumbrils of the revolution. but that woodman and that farmer, though they work unceasingly, work silently, and no one heard them as they went about with muffled tread: the rather, forasmuch as to entertain any suspicion that they were awake, was to be atheistical and traitorous. in england, there was scarcely an amount of order and protection to justify much national boasting. daring burglaries by armed men, and highway robberies, took place in the capital itself every night; families were publicly cautioned not to go out of town without removing their furniture to upholsterers' warehouses for security; the highwayman in the dark was a city tradesman in the light, and, being recognised and challenged by his fellow-tradesman whom he stopped in his character of the captain, gallantly shot him through the head and rode away; the mail was waylaid by seven robbers, and the guard shot three dead, and then got shot dead himself by the other four, in consequence of the failure of his ammunition: after which the mail was robbed in peace; that magnificent potentate, the lord mayor of london, was made to stand and deliver on turnham green, by one highwayman, who despoiled the illustrious creature in sight of all his retinue; prisoners in london gaols fought battles with their turnkeys, and the majesty of the law fired blunderbusses in among them, loaded with rounds of shot and ball; thieves snipped off diamond crosses from the necks of noble lords at court drawing-rooms; musketeers went into st. giles's, to search for contraband goods, and the mob fired on the musketeers, and the musketeers fired on the mob, and nobody thought any of these occurrences much out of the common way. in the midst of them, the hangman, ever busy and ever worse than useless, was in constant requisition; now, stringing up long rows of miscellaneous criminals; now, hanging a housebreaker on saturday who had been taken on tuesday; now, burning people in the hand at newgate by the dozen, and now burning pamphlets at the door of westminster hall; to-day, taking the life of an atrocious murderer, and to-morrow of a wretched pilferer who had robbed a farmer's boy of sixpence. all these things, and a thousand like them, came to pass in and close upon the dear old year one thousand seven hundred and seventy-five. environed by them, while the woodman and the farmer worked unheeded, those two of the large jaws, and those other two of the plain and the fair faces, trod with stir enough, and carried their divine rights with a high hand. thus did the year one thousand seven hundred and seventy-five conduct their greatnesses, and myriads of small creatures-the creatures of this chronicle among the rest-along the roads that lay before them.", test2)
    sum2 = 0
    for i in [384,67,109,212,581,125,94,293,293,7,32,146,100,337,354,70,4,304,295,429,123,45,118,3,83,2,1001,94,14,21,12,3,1,1,3]:
        sum2 += i
    print("Total number of characters in message 2: " + str(sum2))

    # Problem 5 reading the text
    f = open('TaleOfTwoCities.txt')

    d = defaultdict(int)

    contents = f.read()
    for c in contents:
        d[c] += 1
    
    print(d)

    numUniqueChars = 0
    numTotalChars = 0
    commonKey = ""
    commonKeyFreq = 0
    for key, value in d.items():
        if commonKeyFreq < value:
            commonKey = key
            commonKeyFreq = value
        numUniqueChars += 1
        numTotalChars += value
    print(numUniqueChars)
    print(numTotalChars)

    print(commonKey)
    print(commonKeyFreq)

    characters = []
    frequencies = []

    for key, value in d.items():
        characters.append(key)
        frequencies.append(value)

    taleOfCitiesTree = BuildHuffmanCodeTree(characters, frequencies)
    start = time.time()
    taleOfCitiesEncoding = Encode(contents, taleOfCitiesTree)
    end = time.time()
    print("Encoding time: " + str(end - start))
    
    start = time.time()
    Decode(taleOfCitiesEncoding, taleOfCitiesTree)
    end = time.time()
    print("Decoding time: " + str(end - start))

    map = collections.defaultdict(list)
    BuildDict(map, taleOfCitiesTree)
    start = time.time()
    EncodeUsingMap(contents, map)
    end = time.time()
    print("Encoding with map: " + str(end - start))
