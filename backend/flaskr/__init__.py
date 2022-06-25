
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE

    formated = [question.format() for question in questions]
    current_questions = formated[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PUT, POST, DELETE, OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formated = {}
        for category in categories:
            formated.update({f'{category.id}': category.type})
        if len(categories) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "categories": formated,
            "total_categories": len(categories)
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        # questions: result.questions,
        # totalQuestions: result.total_questions,
        # categories: result.categories,
        #currentCategory: result.current_category
        questions = Question.query.order_by(Question.id).all()
        paged_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        formated = {}
        for category in categories:
            formated.update({f'{category.id}': category.type})
        if len(paged_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': paged_questions,
            'total_questions': len(questions),
            'categories': formated,
            'currentCategory': None
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            question.delete()
            return jsonify({'success': True})
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        search = body.get('searchTerm', None)
        try:
            if search:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{search}%'))
                formated = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'questions': formated,
                    'total_questions': len(formated),
                    'current_category': None
                })
            else:
                if question is None:
                    abort(422)
                new_question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)
                new_question.insert()
                return jsonify({'success': True})

        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_category(category_id):
        questions = Question.query.order_by(Question.id).filter(
            Question.category == category_id)
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        formated = paginate_questions(request, questions)
        if len(formated) == 0 or category is None:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formated,
            'total_questions': questions.count(),
            'current_category': {f'{category.id}': category.type}
        })
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        category = body.get('quiz_category', None)
        if category is None:
            questions = Question.query.order_by(Question.id).filter(
                Question.category == int(category['id']))
        else:
            questions = Question.query.order_by(Question.id).all()
        new_questions = []
        for q in questions:
            if q.id not in previous_questions:
                new_questions.append(q)
        formated = [question.format() for question in new_questions]
        if len(new_questions) == 0:
            abort(404)
        question = random.choice(formated)
        return jsonify({
            'success': True,
            'question': question,
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            'success': False, 'error': 404, 'message': 'not found'
        }), 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success': False, 'error': 422, 'message': 'unprocessable'
        }), 422)

    return app
