#Using "War and Peace" and "Swann's Way" ("pg2600.txt" and "pg7178.txt")
#the program scores 70% correct and takes roughly 20-30 seconds to run.
#Using those books and "The Complete Works of Shakespeare" ("shakespeare.txt")
#it scores 80% and takes roughly 2-3 minutes to run.

'''
Semantic Similarity
Author: Andrew Ilersich. Last modified: Nov. 10, 2014.
'''

import math, time


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    
    Arguments:
    vec is type dict_items. Represent the vector corresponding to a semantic
                            descriptor.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    
    Arguments:
    vec1 is type dict_items. Represent the vector corresponding to the semantic
                             descriptor for the first word.
    vec2 is type dict_items. Represent the vector corresponding to the semantic
                             descriptor for the second word.
    '''
    
    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    try:
        return dot_product / (norm(vec1) * norm(vec2))
    except ZeroDivisionError:
        return -1


def get_sentence_lists(text):
    '''Return a list of sentences in the string text with each entry as a list
    of the words as strings in that sentence. The words are all in lowercase
    letters and without punctuation.
    
    Arguments:
    text is type string. Represent a reference English text.
    '''
    
    #Remove all exclamation and question marks by turning them into periods,
    #then split the text into sentence lists.
    
    text = text.replace("!", ".")
    text = text.replace("?", ".")
    sentences = text.split(".")
    
    #List of the punctuation marks that the program will remove from words.
    
    punctuation = [",", "-", "--", ":", ";", "!", "?", ".", "\"", "\'"]
    
    for index in range(len(sentences)):
        sentence = sentences[index]
        
        #Remove all punctuation by turning them into spaces, then split the
        #sentences into word lists.
        
        for punc_mark in punctuation:
            sentence = sentence.replace(punc_mark, " ")
        sentences[index] = sentence.split()
        
        #Remove all empty words from the word lists.
        
        i = 0
        while "" in sentences[index]:
            if sentences[index][i] == "":
                del sentences[index][i]
            else:
                i += 1
        
    #Remove all empty sentences from the sentence lists.
    
    j = 0
    while [] in sentences:
        if sentences[j] == []:
            del sentences[j]
        else:
            j += 1
    
    #Convert all the words to lowercase, since this program shouldn't be
    #case-sensitive.
    
    for index in range(len(sentences)):
        for k in range(len(sentences[index])):
            sentences[index][k] = sentences[index][k].lower()
    
    #When all empty entries are removed and the words are in lowercase, return
    #the list sentences.
    
    return sentences


def get_sentence_lists_from_files(filenames):
    '''Return the text as sentence lists from text files, taken as strings of
    file names.
    
    Arguments:
    filenames is type list containing elements of type string. Represent the
                           filenames that the program will open and read.
    '''
    
    file_sentences = []
    
    #Go through every file in filenames, and add each list of sentences to the
    #file list.
    
    for file in filenames:
        f = open(file)
        file_sentences.append(get_sentence_lists(f.read()))
    
    #When done, return the three dimensional list.
    
    return file_sentences


def build_semantic_descriptors(text_lists):
    '''Return a dictionary of words that contains the semantic descriptors for
    each word in the texts in text_lists, taken as a list of strings.
    
    Arguments:
    text_lists is type list. Three dimensional, ultimately containing elements
                             of type string. Represent the list of words
                             obtained from each text.
    '''
    
    #Create the dictionary that will become the semantic descriptors.
    
    word_dict = {}
    
    #Iterate through every text, then every sentence, then every word.
    
    for sentences in text_lists:
        for sentence in sentences:
            
            #To prevent multiple instances of the same word causing every other
            #word to be counted multiple times, every word once used is appended
            #to words_already_counted. If it was already counted, it is skipped.
            
            words_already_counted = []
            
            for word in sentence:
                if word in words_already_counted:
                    continue
                
                words_already_counted.append(word)
                
                #Check whether there exists a dictionary entry for this word
                #already. If not, create the entry as an empty dictionary.
                
                try:
                    word_dict[word]
                except KeyError:
                    word_dict[word] = {}
                
                #Iterate through every other word in the sentence.
                
                for other_word in sentence:
                    if word != other_word:
                        
                        #If there already exists an entry for the other_word
                        #associated with word, increment it by 1. If not, create
                        #it and set it to 1.
                        
                        try:
                            word_dict[word][other_word] += 1
                        except KeyError:
                            word_dict[word][other_word] = 1
    
    #When done, return the dictionary.
    
    return word_dict
    
    
def most_similar_word(word, choices, semantic_descriptors):
    '''Return the word in list choices with the greatest cosine similarity to
    string word according to semantic_descriptors
    
    Arguments:
    word is type string. Represent the word whose synonym the program will find.
    choices is type list with elements of type string. Represent the set of
                         words that contains the synonym for word.
    semantic_descriptors is type dict. Contain dicts of integers. Represent the
                         semantic descriptor of words from the reference texts.
    '''
    
    #At first, assume value for greatest similarity to -1 and the most similar
    #word to be the first choice.
    
    max_sim = -1
    max_sim_word = choices[0]
    
    #For every word choice in list choices:
    
    for choice in choices:
        
        #Try to find the cosine similarity of the word and the current choice.
        #If they doesn't exist in the semantic descriptors, similarity is -1.
        
        try:
            sim = cosine_similarity(semantic_descriptors[word],
                                    semantic_descriptors[choice])
        except KeyError:
            sim = -1
        
        #If the similarity of the current choice is greater than the previous
        #maximum, the current choice becomes the new maximum.
        
        if sim > max_sim:
            max_sim = sim
            max_sim_word = choice
    
    #When done, return the choice with the greatest similarity to word.
    
    return max_sim_word


def run_similarity_test(filename, semantic_descriptors):
    '''Return a float value between 0 and 100 that represents the percentage of
    questions the program answered correctly.
    
    Arguments:
    filename is type string. Represent the file that contains the questions.
    semantic_descriptors is type dict. Contain dicts of integers. Represent the
                         semantic descriptor of words from the reference texts.
    '''
    
    #Open the file that contains the synonym test questions.
    
    questions = open(filename)
    
    #Initialize counter variables for right answers and wrong answers.
    
    right_answers = 0
    wrong_answers = 0
    
    #Every line in the list questions.readlines() corresponds to a question.
    #For every question in the list of questions:
    
    for question in questions.readlines():
        
        #Turn the string question into a list of strings that contains the word,
        #the correct answer, and the choices.
        
        question = question.split()
        
        #Find the most similar word to the first word among all the choices.
        
        closest_word = most_similar_word(question[0], question[2:len(question)],
                                         semantic_descriptors)
        
        #If the word returned by the program is the correct answer, increment
        #right_answers by 1. If not, increment wrong_answers by 1.
        
        if question[1] == closest_word:
            right_answers += 1
        else:
            wrong_answers += 1
    
    #When done, divide right_answers by the total answers and multiply by 100 to
    #obtain the percentage of correct answers.
    
    return (right_answers / (wrong_answers + right_answers)) * 100


def run(file_list, test_file):
    '''Print the progress of the program as it runs, and finally the score as a
    percentage and the time taken to execute.
    
    Arguments:
    file_list is type list. Elements are type string. Represent the file names
                            of the reference texts.
    '''
    
    #If the test_file does not exist, end function.
    
    try:
        open(test_file)
    except FileNotFoundError:
        print("Test file not found!")
        return
    
    #Start the clock to measure how long the program runs.
    
    start_time = time.clock()
    
    #Print that the program is importing files, then get sentence lists from the
    #list of reference files.
    
    print("Importing Files... ", end = "")
    
    text_lists = get_sentence_lists_from_files(file_list)
    
    #Print that it is building the semantic descriptors, then build semantic
    #descriptors from the sentence lists.
    
    print("Done!\nBuilding Semantic Descriptors... ", end = "")
    
    semantic_descriptors = build_semantic_descriptors(text_lists)
    
    #Print that it is running the similarity tests, then run the similarity test
    #for a given test file.
    
    print("Done!\nRunning Similarity Tests... ", end = "")
    
    result = run_similarity_test(test_file, semantic_descriptors)
    
    #Print the results of the similarity test and the time taken for the program
    #to execute.
    
    print("Done!\nResult: " + str(result) + "% correct answers\nTime:",
          round(time.clock() - start_time), "seconds")

if __name__ == "__main__":
    #War and Peace, Swann's Way, and The Complete Works of Shakespeare
    #and normal test file
    run(["pg2600.txt", "pg7178.txt", "shakespeare.txt"], "test.txt")
