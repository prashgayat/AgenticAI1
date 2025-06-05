# rank_jobs.py – Delegates to search_jobs_ranked.py

from search_jobs_ranked import evaluate_jobs as ranked_evaluator

def evaluate_jobs():
    return ranked_evaluator()
