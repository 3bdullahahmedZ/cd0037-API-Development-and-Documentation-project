# Backend - Trivia API

## Setting up the Backend

### Dependencies

1. Python 3.9.6
2. Virtual environment

To install requirements after making a Virtual environment
```bash
pip install -r requirements.txt
```



### Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs. Success state and the total number of categories

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
}
```

`GET '/questions?page=<int:page>'`

- Fetches a dictionary with a list of questions in which the keys are the ids, questions, answers, categories and difficulties and their values. A dictionary of categories, the current catagory, success state and the total of questions
- Request Arguments: int: page
- Returns: An object with 10 paginated questions, a list of categories, the currnet category and the total number of questions
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
    ],
    "success": true,
    "total_questions": 20
}
```

`DELETE '/questions/<int:question_id>'`

- Deletes the question with the given id 
- Request Arguments: int: question_id
- Returns: A success state 
```
{
    "success": true
}
```

`POST '/questions'`

- Adds a new question wiht the given arguments 
- Request Arguments: string: question, string:answer, int:difficulty, int:category
- Returns: A success state 
```
{
    "success": true
}
```

`POST '/questions'`

- Adds a new question wiht the given arguments 
- Request Arguments: string: searchTerm
- Returns: an object of questions with the search term in the question attribute, the total number of questions in the object, the current category and a success state
```
{
    "current_category": null,
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

`GET '/categories/<int:category_id>/questions?page=<int:page>'`

- Fetches a dictionary with a list of questions within the given category in which the keys are the ids, questions, answers, categories and difficulties and their values. The current catagory, success state and the total of questions
- Request Arguments: int: category_id, int: page
- Returns: An object with 10 paginated questions, the currnet category and the total number of questions in the category
```
 "current_category": {
        "1": "Science"
    },
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
    ],
    "success": true,
    "total_questions": 1
}
```

`POST '/quizzes'`

- Fetches a random question within the given category  
- Request Arguments: list: previous_questions, category:{sting:id, string:type}
- Returns: A random question that is not one of the given previous questions and within the given category and a success state

```
{
    "question": {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
}
```

