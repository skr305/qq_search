from django.urls import path
import polls.views

polls_patterns = [
    
    path('test/', polls.views.test),
    path('qq_code/', polls.views.query_by_QQNum),
    path('nick/', polls.views.query_by_Nick),
]