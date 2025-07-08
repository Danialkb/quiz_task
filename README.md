# Deploy instructions (LOCAL). Execute from root directory of project (quiz_task)
> docker compose -f deploy/docker-compose.yml up --build -d
# !!! Database will be automatically populated with script

# Swagger UI doc can be accessed on 
> 0.0.0.0:8000/docs


# Run tests
> docker exec -it quiz_backend uv run pytest -vvv 



# Endpoint description

Headers required:
X-User-ID - UUID
X-Language - Optional default is english. In test data we have 2 languages - en(English), es(Spanish)

## /api/v1/health GET
Check that service is available

## /api/v1/quizzes GET
List all available quizzes

## /api/v1/quizzes/{id} GET
Fetch specific quiz details, can return 404 NotFound API exception

## /api/v1//quizzes/{quiz_id}/questions GET
Fetch specific quiz questions with options

## /api/v1/quiz_sessions POST
Create quiz session(start answering) for specific user


## /api/v1/quiz_sessions GET
List quiz session. Data will be filtered by X-User-ID.

## /api/v1/quiz_sessions/{id}/finish
Finish quiz_session - calculate bonus and send it to user balances service. 
Raises 404 if session not found and 400 if session already finished.

## /api/v1/user_answers POST
Submit user answer for quiz session and specific question with option. 
In response we have flag identifying correctness of answer and correct options


