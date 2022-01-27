# Wordy document analyser

A simple example of natural language processing.

## Specification

### Primary user story

I am an end-user with many documents. I want to see  which
interesting words occur most frequently, so that I  can
identify important topics across all documents.

### Scenarios

**View results**

```gherkin
Given documents are parsed
When the user opens the page
Then display words sorted by frequency
And display a sample sentence from each document
```

**Upload a new file**

```gherkin
Given the filename has not been used before
When the user uploads the file
Then parse the contents
And display the updated results
```

**Upload an existing file**

```gherkin
Given the filename has been used before
When the user uploads the file
Then replace the old contents
And parse the new contents
And display the updated results
```

### Sample output

| Word       | Count | Samples                                             |
|------------|-------|-----------------------------------------------------|
| philosophy | 42    | I don't have time for philosophy... (document X)    |
|            |       | Surely this was a touch of... (document Y)          |
|            |       | Still, her pay-as-you-go philosophy... (document Z) |

### Notable features

* Stopwords (a, the, and...) are removed

### Limitations

**This site is not production-ready!**

* No file validation
* No performance optimisation
* Requires admin access to delete documents

### Out of scope

* Access rights and granular permissions
* Database instance (i.e. other than SQLite)
* Fully offline operation
* Languages other than English (American spelling?)
* Microservice architecture
* REST API

## Screenshot

![Interesting words by frequency](screenshot.png)

## Run from source

### Prerequisites

* Python 3.8
* [pipenv](https://pipenv.pypa.io/en/latest/install/)

### Steps

1. Create a virtual environment for Python:

   ```
   cd simplenlp
   pipenv install
   ```

2. Bootstrap Django:

   ```
   pipenv shell
   # activate virtual environment

   python manage.py migrate
   # create schema for SQLite database

   python manage.py createsuperuser
   # follow prompts to create an admin user
   
   python runserver
   # start Django site
   ```

3. Open http://localhost:8080 in your browser to see the latest
   results.


4. Upload a `.txt` file to add it to the results. (This might take
   a while. The page will refresh once done.)


5. Hover over a sample to see the full sentence containing the
   interesting word.

**Notes**

* To view database contents, visit the admin site
  http://localhost:8080/admin/ and log in with the superuser
  credentials created above.


* To remove a document from the results, you must delete it
  through the admin interface.
