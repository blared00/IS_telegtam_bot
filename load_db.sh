#!/bin/bash
python3 manage.py loaddata dump_data/db_admin.json

python3 manage.py loaddata dump_data/db_polls.json
python3 manage.py loaddata dump_data/db_poll_questionoptions.json
python3 manage.py loaddata dump_data/db_poll_lesson.json
python3 manage.py loaddata dump_data/db_poll_question.json


python3 manage.py loaddata dump_data/db_game_questioncategory.json
python3 manage.py loaddata dump_data/db_game_questionoptions.json
python3 manage.py loaddata dump_data/db_game_question.json

python3 manage.py loaddata dump_data/db_pinmessage.json
