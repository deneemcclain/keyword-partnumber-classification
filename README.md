# keyword-partnumber-classification
A containerized and deployable linear SVC model that classifies search terms as keywords and part numbers

# Introduction 
This project asks the question - can we build a machine learning model that can tell us whether or not a given search term is a keyword search or a part number search?

# Getting Started
Stored in this repo should be:
- the raw search term data
- the code to generate the search term training data
- the data used to train the model
- the code to train the model / analysis of the results of the model

## Raw Search Term Data
search_terms.txt
This file contains 14,652 lines of real search terms searched on Mouser.com pulled from Google Analytics and Lucidworks.

## Code to Generate Training Data
The Python file generate_keyword_data.py contains the code used to generate the training data. This code expects a file called search_terms.txt, which contains the raw search term data that was pulled from Google Analytics and Lucidworks.
The code runs through each search term, trims and scrubs it, and generates the columns in the training data.

## Search Term Training/Test Data
search_terms.csv
Rows: 14,357
Columns:
- term - string - The search term
- length - integer - The length of the search term
- letterCount - integer - The count of letters in the search term
- numberCount - integer - The count of digits in the search term
- spaceCount - integer - The count of spaces in the search term
- startsWithNumber - integer - 1 if the first character in the search term is a digit or if the first character is '.' and the second character is a digit, 0 otherwise
- endsWithNumber - integer - 1 if the last character in the search term is a digit
- isPartNumber - integer - 1 if the search term is a part number, 0 otherwise. This field was manually filled out.

# Build and Test
The project code can be found in the KeywordPartNumberDistinction.ipynb file. This file contains the code to load the data, perform exploratory data analysis on the data, model the data, and analyze the results of the model.

In order to run or view a Jupyter notebook, you must have [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) or [Jupyter](https://docs.jupyter.org/en/latest/install.html) installed on your machine, as well as [Python](https://www.python.org/downloads/).

# Deploy & Integrate with Lucidworks Fusion

## Containerize model
The code to containerize and export the classification model can be found in the ContainerizeKeywordPartNumberClassificationModel.ipynb file. This file contains code that creates a directory containing the necessary files for the classification model, writes a Docker file to containerize the directory, builds the Docker file, and pushes it to a repository.

In order to properly use the code in this Jupyter notebook, you must have [Docker](https://docs.docker.com/desktop/install/windows-install/) installed.

## Deploy model with Lucidworks Fusion
The steps to accomplish this are as follows. Please see screenshots in the 'code' folder for details.
1. Create a Seldon Core model deployment job within Fusion that will pull your containerized model from its repository and compile it.
2. Run the job to make your model available within Fusion

## Call model within Lucidworks Fusion pipeline
The steps to accomplish this are as follows. Please see screenshots in the 'code' folder for details.
1. Create a copy of the mouser query pipeline and give it a unique name, for example 'mouser_denee_ml'
2. Create a query profile that points to this query pipeline and give it a unique name, for example 'mouser_ml'
3. Add a stage to the POC pipeline that calls the classification model

# Results
Please refer to the images in the 'analysis' folder to see examples of the results returned by the two pipelines.

## Search term '23uf'
The regular pipeline returns 24 results, while the test pipeline returns 6 results. The top 17 results returned by the regular pipeline have '23uf' somewhere in the part number. Since when the test pipeline calls the classification model, it classifies '23uf' as a keyword search, it only searches the keyword fields, bringing back less results, but more relevant results.

## Search term '100cm'
The regular pipeline returns 435 results, and the top 58 have '100cm' in the part number. The test pipeline brings back only 372 results, but the top results are more relevant since '100cm' was classified as a keyword and only the keyword fields were queried.

## Search term 'ddr5'
The regular pipeline brings back 557 results. Even though the test pipeline classifies this search term as a part number, it brings back only 235 results, because it is querying only the part number fields.

## Search term 'mt10'
The regular pipeline returns 2,277 results, while the test pipeline returns a similar count, 2,274. The test pipeline classified the search term as a part number, but since almost all of the results match on the part number fields, excluding the keyword fields from being queried does not affect the result count nearly as much.

# Conclusions
When the classification model classifies a search term as a keyword, we see less results returned by the test pipeline in comparison to the regular pipeline (the one not calling the classification model), but the results returned are more relevant. Since the part number fields are not being searched, there are no useless matches on the part number when the user is searching for an attribute value of a part. (Examples: '22uf', '23uf', '800v', '100cm', '200mm')
However, when the classification model classifies a search term as a part number, we see one of two scenarios taking place. Sometimes the test pipeline (the one calling the classification model) returns much less results than the regular pipeline (Examples: 'ddr5', 'q200') because it's searching only the part number fields and missing the parts that match the search term in their keyword fields. Other times, the test pipeline brings back almost equal result counts to the regular pipeline (Examples: 'mt10', '3106') because the parts that match the search term happen to match only on their part number fields.
Obviously the desired results will depend on the use case, but this project has shown that classiying a passed in search term can be used to produce more relevant results.

# Contribute & Further Study
This project can be expanded on by testing the classification model in different query pipelines, and testing different ways to use the classification returned by the classification model. Perhaps instead of excluding query fields based on the classification, choosing which fields to boost or bury can be based on the classification.
