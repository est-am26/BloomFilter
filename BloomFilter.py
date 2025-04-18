import BitHash
import BitVector 

class BloomFilter(object):
    
    # Return the estimated number of bits needed in a Bloom Filter:
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        # Use Equation B to get the desired phi from P and d:
        phi = (1 - (maxFalsePositive**(1/numHashes))) 
        # Use Equation D to get the needed N from d, phi and n:
        N = numHashes / (1 - (phi**(1/numKeys)))
        # Return the estimated number of bits needed:
        return int(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # Initialize a number of keys the Bloom Filter will store:
        self.__numKeys = numKeys         
        # Number of hash functions to use:
        self.__numHashes = numHashes         
        # Desired false positive rate:
        self.__maxFalsePositive = maxFalsePositive         
        # Initialize a bit vector calling the __bitsNeeded method to calculate the 
        # number of bits needed for the Bloom Filter based on the provided parameters:
        self.__bitsNeeded = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bitVector = BitVector.BitVector(size=self.__bitsNeeded)        
        # Initialize a variable to keep track of the number of 
        # bits that have been set to one in the Bloom Filter:
        self.__bitsSetToOne = 0

    # Insert the specified key into the Bloom Filter:
    def insert(self, key):
        # Iterate through the times of number of hash functions to use:
        for i in range(1, self.__numHashes+1):
            # Calculate the hash value for the key using a hash function:
            hashVal = BitHash.BitHash(key, i) % len(self.__bitVector)
            # If the bit at the calculated hash value position is not set to 1 
            # yet, increment the count of bits set to one:     
            if self.__bitVector[hashVal] == 0:
                self.__bitsSetToOne += 1
            # Set the bit at the calculated hash value position in the bit vector to 1:
            self.__bitVector[hashVal] = 1 
    
    # Check if the specified key might be in the Bloom Filter.
    def find(self, key):
        # Iterate through the times of hashes:
        for i in range(1, self.__numHashes+1):
            # Calculate the hash value for the key using a hash function:
            hashVal = BitHash.BitHash(key, i) % len(self.__bitVector)
            # If the bit at the calculated hash value position is 0,
            # the key doesn't exist in the Bloom Filter, so return False:           
            if self.__bitVector[hashVal] == 0:
                return False
        # Otherwise, it might be in the Bloom Filter, so return True:
        return True
                
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits ACTUALLY set in this Bloom Filter. 
    def falsePositiveRate(self):
        # Calculate the bits that are still set to 0:
        phi = (len(self.__bitVector) - self.__bitsSetToOne) /  len(self.__bitVector)
        # Calculate the probability of a false positive, and return it:      
        P = (1 - phi) ** self.__numHashes   
        return P 
    
    # Returns the current number of bits ACTUALLY set to 1 in this Bloom Filter:
    def numBitsSet(self):
        return self.__bitsSetToOne 

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # Create the Bloom Filter:
    bF = BloomFilter(numKeys, numHashes, maxFalse)
    
    # Read the first numKeys words from the file and insert them 
    # into the Bloom Filter:
    fin = open("wordlist.txt")
    for i in range(numKeys):
        line = fin.readline()
        bF.insert(line)
    
    # Close the input file:
    fin.close()
    
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter:    
    print("Projected theoretical false positive rate: ", bF.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing:
    fin = open("wordlist.txt")
    
    wordsMissing = 0
    for i in range(numKeys):
        line = fin.readline()
        if bF.find(line) == False:
            wordsMissing += 1
            
    print("There are", wordsMissing, "words missing from the Bloom Filter.")
    
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter:  
    wordsFound = 0
    for i in range(numKeys):
        line = fin.readline()
        if bF.find(line) == True:
            wordsFound += 1   
            
    print("There were", wordsFound, "false positives.")
    
    # Print out the percentage rate of false positives:  
    print("Percentage rate of false positives:", wordsFound/numKeys)

    
if __name__ == '__main__':
    __main()       

