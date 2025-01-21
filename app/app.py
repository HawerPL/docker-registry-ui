import babel
from flask import request, session
from app import create_app

app = create_app()

@app.template_filter()
def format_datetime(value, format_date='medium'):
    if format_date == 'full':
        format_date = "EEEE, d. MMMM y 'at' HH:mm"
    elif format_date == 'medium':
        format_date = "EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format_date)


@app.before_request
def before_request():
    request.lang = request.accept_languages.best_match(['en', 'pl'])


