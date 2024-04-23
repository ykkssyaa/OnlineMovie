from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from movies.models import Film
from reviews.forms import ReviewForm, MarkForm
from reviews.models import Review, Mark


@login_required
def add_review(request, film_id):
    film = get_object_or_404(Film, pk=film_id)

    review = Review.objects.filter(movie=film, user=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_inst = form.save(commit=False)
            if review is not None:
                review.text = review_inst.text
                review.save()
            else:
                review_inst.user = request.user
                review_inst.movie = film
                review_inst.save()

    return redirect('movies:detail', pk=film_id)


@login_required
def add_mark(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    user = request.user

    mark = Mark.objects.filter(movie=film, user=user).first()

    if request.method == 'POST':
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            if mark is None:
                mark = form.save(commit=False)

            mark.movie = film
            mark.user = user

            mark.save()

    return redirect('movies:detail', pk=film_id)


def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.user.pk == review.user.pk:
        review.delete()

    return redirect('movies:detail', pk=review.movie.pk)
