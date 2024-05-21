


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
from django.shortcuts import render
from django.db.models import Q
from .models import Goal
from sklearn.metrics.pairwise import cosine_similarity

# Initialize TF-IDF Vectorizer outside the function 
tfidf_vectorizer = TfidfVectorizer()

def search(request):
    query = request.GET.get('q')
    results = []

    if query and not query.isspace():  # Check for non-empty and non-whitespace query
        goals = Goal.objects.filter(
            Q(title__icontains=query) | Q(sub__icontains=query)
        )[:5]  # Limit results to 5

        if goals:
            # Preprocess the data using list comprehensions
            text_data = []
            for goal in goals:
                title = goal.title.lower()
                sub = goal.sub.lower() if goal.sub else ''
                text_data.append(title + ' ' + sub)

            # Transform the TF-IDF Vectorizer
            tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)

            # Transform user input using the same TF-IDF Vectorizer
            user_input = query.lower()
            user_tfidf = tfidf_vectorizer.transform([user_input])

            # Calculate cosine similarity between user input and all titles
            cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

            # Get indices of top N most similar goals
            top_indices = cosine_similarities.argsort()[-5:][::-1]

            # Top N recommended goals
            results = [goal for idx, goal in enumerate(goals) if idx in top_indices]

    return render(request, 'searchingApp/base.html', {'query': query, 'results': results})





def goal_list(request):
    goals = Goal.objects.all()
    return render(request, 'searchingApp/goal.html', {'goals': goals})