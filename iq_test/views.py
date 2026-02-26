"""
Views for Geeks Andijan IQ Test.
Educational MVP - Barcha foydalanuvchilar uchun umumiy platforma.
"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.utils import timezone

from .models import Question, UserResult, TestSession
from .forms import StudentInfoForm
from .telegram_utils import send_result_to_telegram


# ==================== STUDENT SIDE ====================

def landing(request):
    """Landing page with hero, stats, and CTA."""
    total_attempts = UserResult.objects.count()
    avg_score = UserResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
    top_3 = UserResult.objects.order_by('-score', '-created_at')[:3]
    return render(request, 'iq_test/landing.html', {
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'top_3': top_3,
    })


def student_info(request):
    """Student info form - step 1."""
    if request.method == 'POST':
        form = StudentInfoForm(request.POST)
        if form.is_valid():
            info = {
                'name': form.cleaned_data['name'],
                'age': form.cleaned_data['age'],
                'phone': form.cleaned_data['phone'],
            }
            # Store in session for use after test
            request.session['student_info'] = info
            return redirect('iq_test:start_test')
    else:
        form = StudentInfoForm()

    return render(request, 'iq_test/student_info.html', {'form': form})


def start_test(request):
    """Redirect to test - ensures student info exists."""
    if 'student_info' not in request.session:
        return redirect('iq_test:student_info')
    return render(request, 'iq_test/test.html')


def get_questions(request):
    """API: Return active questions as JSON for test (text, raven, abstract, visual)."""
    qs = Question.objects.filter(is_active=True)
    questions = []
    for q in qs:
        opts = []
        for letter in 'abcdefgh':
            text = (getattr(q, f'option_{letter}') or '').strip()
            img = getattr(q, f'option_{letter}_image', None)
            if text or (img and img.name):
                opts.append({
                    'letter': letter,
                    'text': text or None,
                    'image': img.url if img and img.name else None,
                })
        questions.append({
            'id': q.id,
            'question_type': q.question_type,
            'text': q.text or '',
            'image': q.image.url if q.image and q.image.name else None,
            'options': opts,
        })
    return JsonResponse({'questions': questions})


@require_POST
def submit_test(request):
    """Submit test answers and calculate score."""
    if 'student_info' not in request.session:
        return JsonResponse({'error': 'Ma\'lumot topilmadi'}, status=400)

    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        time_spent = data.get('time_spent', 0)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Noto\'g\'ri ma\'lumot'}, status=400)

    # Calculate score - total = all active questions, unanswered = wrong
    all_questions = Question.objects.filter(is_active=True)
    total = all_questions.count()
    correct = 0

    try:
        q_ids = [int(k) for k in answers.keys()]
    except (ValueError, TypeError):
        q_ids = []

    for q in all_questions:
        if str(q.id) in answers and answers[str(q.id)] == q.correct_answer:
            correct += 1

    # Score: 0-100 based on correct/total (skipped = wrong)
    score = round((correct / total * 100)) if total > 0 else 0

    # Save result
    info = request.session['student_info']
    result = UserResult.objects.create(
        name=info['name'],
        age=info['age'],
        gender=info.get('gender', 'M'),
        phone=info['phone'],
        score=score,
        correct_count=correct,
        total_questions=total,
    )

    # Optional: create TestSession
    TestSession.objects.create(
        user_result=result,
        finished_at=timezone.now(),
        time_spent=time_spent
    )

    # Telegram guruhiga natija yuborish (ism, yosh, telefon, ball)
    send_result_to_telegram(info, result)

    # Store result id for results page
    request.session['last_result_id'] = result.id

    return JsonResponse({
        'success': True,
        'result_id': result.id,
        'score': score,
        'correct': correct,
        'total': total,
    })


def results(request, result_id=None):
    """Show test results with badge and category."""
    rid = result_id or request.session.get('last_result_id')
    if not rid:
        return redirect('iq_test:landing')

    result = get_object_or_404(UserResult, id=rid)

    # Determine category and badge
    if result.score < 40:
        category = 'low'
        badge = 'Bronza'
        badge_emoji = '🥉'
        message = 'Yaxshilab mashq qiling, keyingi safar yaxshiroq natija olasiz!'
    elif result.score < 70:
        category = 'average'
        badge = 'Kumush'
        badge_emoji = '🥈'
        message = 'Yaxshi natija! Bir oz ko\'proq harakat qilsangiz, eng yaxshi natijani olasiz.'
    else:
        category = 'high'
        badge = 'Oltin'
        badge_emoji = '🥇'
        message = 'Ajoyib! Sizning mantiqiy fikrlash qobiliyatingiz juda yuqori!'

    # Top 3 for leaderboard preview
    top3 = UserResult.objects.order_by('-score', '-created_at')[:3]

    return render(request, 'iq_test/results.html', {
        'result': result,
        'category': category,
        'badge': badge,
        'badge_emoji': badge_emoji,
        'message': message,
        'top3': top3,
    })


def certificate(request, result_id):
    """Certificate page — print/save as PDF (no server-side file)."""
    result = get_object_or_404(UserResult, id=result_id)

    if result.score < 40:
        badge = 'Bronza'
        badge_emoji = '🥉'
        message = 'Siz Geeks Andijan IQ testida qatnashdingiz. Yaxshilab mashq qiling — keyingi safar yanada yaxshi natija sizni kutadi!'
    elif result.score < 70:
        badge = 'Kumush'
        badge_emoji = '🥈'
        message = 'Siz Geeks Andijan IQ testida yaxshi natija ko\'rsatdingiz. Davom eting — sizning potensialingiz katta!'
    else:
        badge = 'Oltin'
        badge_emoji = '🥇'
        message = 'Siz Geeks Andijan IQ testida a\'lo natija ko\'rsatdingiz. Mantiqiy fikrlash qobiliyatingiz bilan davom eting!'

    return render(request, 'iq_test/certificate.html', {
        'result': result,
        'badge': badge,
        'badge_emoji': badge_emoji,
        'message': message,
    })


# ==================== ERROR PAGES ====================

def page_not_found_view(request, exception=None):
    """404 — sahifa topilmadi."""
    return render(request, 'iq_test/404.html', status=404)


def server_error_view(request):
    """500 — server xatosi."""
    return render(request, 'iq_test/500.html', status=500)


