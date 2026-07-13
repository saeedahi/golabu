from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from articles_module.forms import ArticleCommentForm
from utils.for_blogs import generate_toc
from utils.http_service import get_client_ip
from articles_module.models import ArticleModel, ArticleVisit, ArticleComments, CommentLike, ArticleCategory


# Create your views here.

class ArticleListView(ListView):
    template_name = 'articles_module/articles.html'
    model = ArticleModel
    context_object_name = 'article_list'
    paginate_by = 12


    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data()
        categories = ArticleCategory.objects.all()
        context['categories'] = categories
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        tag = self.kwargs.get('tag')
        if tag:
            query = query.filter(tag__in_url__icontains=tag)
        return query.order_by('-created_at')


# def articles(request):
#     return render(request, 'articles_module/articles.html', {})

class ArticleDetailView(DetailView):
    template_name = "articles_module/article_detail.html"
    model = ArticleModel
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = self.object
        toc = generate_toc(article.content)
        context['toc'] = toc
        comments = ArticleComments.objects.filter(article_id=article.id, parent=None).order_by('-create_date').prefetch_related('articlecomments_set', 'commentlike_set')
        context['comments'] = comments
        context['comments_count'] = ArticleComments.objects.filter(article_id=article.id).count()
        context['comment_form'] = ArticleCommentForm()
        user_ip = get_client_ip(self.request)
        has_been_visited = ArticleVisit.objects.filter(ip__iexact=user_ip, article_id=article.id).exists()
        if not has_been_visited:
            if self.request.user.is_authenticated:
                new_visit = ArticleVisit(ip=user_ip, article=article, user=self.request.user)
            else:
                new_visit = ArticleVisit(ip=user_ip, article=article)
            new_visit.save()

        context['other_articles_author'] = ArticleModel.objects.filter(author_id=article.author.id).exclude(id=article.id)

        # print(article.content)
        return context


@login_required
def add_comment(request: HttpRequest):
    if request.method == 'POST':
        comment_form = ArticleCommentForm(request.POST)
        article_id = request.POST.get('articleOrProduct_id')
        parent_id = request.POST.get('parent_id')
        comment = request.POST.get('articleComment')
        # print(article_id, parent_id, comment)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = request.user.id
            new_comment.article_id = article_id
            if parent_id:
                new_comment.parent_id = parent_id
            new_comment.save()

        # print(comment_form.errors)
        # return HttpResponse('hello')
        context = {
            'comments': ArticleComments.objects.filter(article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articlecomments_set'),
            'comments_count': ArticleComments.objects.filter(article_id=article_id).count(),
            'comment_form': comment_form,
        }
        return render(request, 'articles_module/includes/article_comment_partial.html', context)


@login_required
def like_comment(request: HttpRequest):
    if request.method == 'POST':
        like_user_id = request.user.id
        comment = get_object_or_404(ArticleComments, id=request.POST.get('comment_id'))
        comment_like = CommentLike.objects.filter(comment_id=comment.id, user_id=like_user_id).first()
        if comment_like:
            comment_like.delete()
        else:
            CommentLike.objects.create(comment_id=comment.id, user_id=like_user_id)

        return JsonResponse({
            'count': comment.commentlike_set.count(),
        })
        # return render(request, 'articles_module/includes/comment_like.html', {
        #     'comment': comment,
        # })
        # return HttpResponse('really')
