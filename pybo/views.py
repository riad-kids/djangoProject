from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import UpdateView, ListView, CreateView, DetailView, DeleteView, View
from django.urls import reverse_lazy

from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm


"""
def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)
"""


class IndexListView(ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'pybo/question_list.html'
    paginate_by = 10

    def get_queryset(self):
        question_list = Question.objects.order_by('-create_date')
        kw = self.request.GET.get('kw', '')
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw) |
                Q(author__username__icontains=kw) |
                Q(answer__author__username__icontains=kw)
            ).distinct()
        return question_list


"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
"""


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'pybo/question_detail.html'
    pk_url_kwarg = 'question_id'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['question'] = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
    #     return context


# question
"""
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
"""


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/question_form.html'

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.create_date = timezone.now()
        question.save()
        return redirect('pybo:index')


"""
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
"""


class QuestionUpdateView(UpdateView):
    model = Question
    fields = {'subject', 'content'}
    template_name = 'pybo/question_form.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        question = form.save(commit=False)
        question.modify_date = timezone.now()
        question.save()
        return redirect('pybo:detail', question_id=question.id)


"""
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
"""


class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = reverse_lazy('pybo:index')
    pk_url_kwarg = 'question_id'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


# answer
"""
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
"""


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/question_detail.html'

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.author = self.request.user
        answer.create_date = timezone.now()
        answer.question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        answer.save()
        return redirect(
            '{}#answer_{}'.format(resolve_url('pybo:detail', question_id=self.kwargs.get('question_id')), answer.id))


"""
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect(
                '{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)
"""


class AnswerUpdateView(UpdateView):
    model = Answer
    fields = {'content'}
    template_name = 'pybo/answer_form.html'
    context_object_name = 'answer'
    pk_url_kwarg = 'answer_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.modify_date = timezone.now()
        answer.save()
        return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))


"""
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
"""


class AnswerDeleteView(DeleteView):
    model = Answer
    context_object_name = 'answer'
    pk_url_kwarg = 'answer_id'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        answer = get_object_or_404(Answer, pk=self.kwargs.get('answer_id'))
        return reverse_lazy('pybo:detail', kwargs={'question_id': answer.question.id})


# comment question
"""
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect(
                '{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
"""


class CommentQuestionCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'pybo/comment_form.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.create_date = timezone.now()
        comment.question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        comment.save()
        return redirect(
            '{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))

"""
@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect(
                '{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
"""


class CommentQuestionUpdateView(UpdateView):
    model = Comment
    fields = {'content'}
    template_name = 'pybo/comment_form.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.modify_date = timezone.now()
        comment.save()
        return redirect(
            '{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))


"""
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)
"""


class CommentQuestionDeleteView(DeleteView):
    model = Comment
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('comment_id'))
        return reverse_lazy('pybo:detail', kwargs={'question_id': comment.question.id})


"""
# comment answer
@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
"""


class CommentAnswerCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'pybo/comment_form.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.create_date = timezone.now()
        comment.answer = get_object_or_404(Answer, pk=self.kwargs.get('answer_id'))
        comment.save()
        return redirect(
            '{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))


"""
@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
"""


class CommentAnswerUpdateView(UpdateView):
    model = Comment
    fields = {'content'}
    template_name = 'pybo/comment_form.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.modify_date = timezone.now()
        comment.save()
        return redirect(
            '{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))


"""
@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)
"""


class CommentAnswerDeleteView(DeleteView):
    model = Comment
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('comment_id'))
        return reverse_lazy('pybo:detail', kwargs={'question_id': comment.answer.question.id})


# vote
"""
@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id=answer.question.id)
"""

class VoteQuestionView(View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        if self.request.user == question.author:
            messages.error(self.request, '본인이 작성한 글은 추천할수 없습니다')
        else:
            question.voter.add(self.request.user)
        return redirect('pybo:detail', question_id=question.id)


class VoteAnswerView(View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        answer = get_object_or_404(Answer, pk=self.kwargs.get('answer_id'))
        if self.request.user == answer.author:
            messages.error(self.request, '본인이 작성한 글은 추천할수 없습니다')
        else:
            answer.voter.add(self.request.user)
        return redirect('pybo:detail', question_id=answer.question.id)

