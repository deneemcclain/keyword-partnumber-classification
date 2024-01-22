# import packages
import re
import csv

'''
This method takes a search term and returns a row of data describing the term, 
including the length, the count of letters, the count of digits, etc.
If the search term is null or empty or less than 3 characters long, an empty row of data will be returned.
'''
def generateSearchTermData(term):
    term_data = []
    if term is not None and len(term) > 2:
        term_data.append(term) # term
        term_data.append(len(term)) # length
        # flag for unexpected characters in term
        badCharacterFound = False
        # get ready to count
        letterCount = 0
        digitCount = 0
        spaceCount = 0
        # loop through term characters
        for char in term:
            if char.isalpha():
                letterCount += 1
            elif char.isdigit():
                digitCount += 1
            elif char.isspace():
                spaceCount += 1
            elif char != '.': # ignore periods, but if weird non-period character in here, don't want
                badCharacterFound = True
                print(f"Search term: {term} contains non-alphanumeric/non-space character.")
                break
        if not badCharacterFound:
            term_data.append(letterCount) # letterCount
            term_data.append(digitCount) # numberCount
            term_data.append(spaceCount) # spaceCount
            term_data.append('1' if term[0].isdigit() or (term[0] == '.' and term[1].isdigit()) else '0') # startsWithNumber
            term_data.append('1' if term[-1].isdigit() else '0') # endsWithNumber
            term_data.append('') # empty col for isPartNumber - labelling will occur manually
    return term_data
        
    
if __name__ == "__main__":
    # Open file & read search terms
    search_term_file = open('search_terms.txt', 'r', encoding='utf8')
    search_terms = search_term_file.readlines()

    # list of lists of string for search term data
    search_term_data = []

    # loop through search terms
    for term in search_terms:
        # remove special characters
        term_scrubbed = re.sub("[^A-Za-z0-9\s.]", "", term).strip()
        # generate data
        term_data = generateSearchTermData(term_scrubbed)
        if len(term_data) == 8: # all columns present
            search_term_data.append(term_data)
        
    # write data to csv
    with open('search_terms.csv', 'w', newline='') as csvfile:
        # create writer object
        csvwriter = csv.writer(csvfile)
        
        # write the header row
        csvwriter.writerow(['term', 'length', 'letterCount', 'numberCount', 'spaceCount', 'startsWithNumber', 'endsWithNumber', 'isPartNumber'])
        
        # write the data rows
        csvwriter.writerows(search_term_data)
