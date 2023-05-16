call poetry install 
call poetry run python -m spacy download en_core_web_trf
call poetry run python -m spacy download en_core_web_lg
call poetry run python -m spacy download es_core_news_lg
call poetry run python -m spacy download pt_core_news_lg
call poetry run python -m spacy download nl_core_news_lg
call poetry run python -m spacy download de_core_news_lg
call poetry run python -m spacy download fr_core_news_lg
call poetry run python prelabel_ne.py
ECHO Installation completed. Press any key to exit CMD window
pause >nul