"""
Views for Geeks Andijan IQ Test.
Educational MVP - Student and Teacher sides.
"""

import csv
import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count
from django.utils import timezone
from openpyxl import Workbook

from .models import Question, UserResult, TestSession
from .forms import StudentInfoForm


# ==================== STUDENT SIDE ====================

def landing(request):
    """Landing page with hero and CTA."""
    return render(request, 'iq_test/landing.html')


def student_info(request):
    """Student info form - step 1."""
    if request.method == 'POST':
        form = StudentInfoForm(request.POST)
        if form.is_valid():
            # Store in session for use after test
            request.session['student_info'] = {
                'name': form.cleaned_data['name'],
                'age': form.cleaned_data['age'],
                'gender': form.cleaned_data['gender'],
                'phone': form.cleaned_data['phone'],
            }
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
    """API: Return active questions as JSON for test."""
    questions = list(
        Question.objects.filter(is_active=True).values(
            'id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'
        )
    )
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

    # Calculate score (answers keys are question ids as strings)
    try:
        q_ids = [int(k) for k in answers.keys()]
    except (ValueError, TypeError):
        q_ids = []
    questions = Question.objects.filter(is_active=True, id__in=q_ids)
    correct = 0
    total = questions.count()

    for q in questions:
        if str(q.id) in answers and answers[str(q.id)] == q.correct_answer:
            correct += 1

    # Score: 0-100 based on correct/total
    score = round((correct / total * 100)) if total > 0 else 0

    # Save result
    info = request.session['student_info']
    result = UserResult.objects.create(
        name=info['name'],
        age=info['age'],
        gender=info['gender'],
        phone=info['phone'],
        score=score,
    )

    # Optional: create TestSession
    TestSession.objects.create(
        user_result=result,
        finished_at=timezone.now(),
        time_spent=time_spent
    )

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
    top3 = UserResult.objects.order_by('-score')[:3]

    return render(request, 'iq_test/results.html', {
        'result': result,
        'category': category,
        'badge': badge,
        'badge_emoji': badge_emoji,
        'message': message,
        'top3': top3,
    })


# ==================== TEACHER / ADMIN DASHBOARD ====================

def dashboard(request):
    """Teacher dashboard with analytics and charts."""
    # Basic stats
    total_attempts = UserResult.objects.count()
    avg_score = UserResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
    last_10 = UserResult.objects.all()[:10]
    top_3 = UserResult.objects.order_by('-score')[:3]
    leaderboard = UserResult.objects.order_by('-score')[:20]

    # By age
    by_age = list(
        UserResult.objects.values('age')
        .annotate(avg_score=Avg('score'), count=Count('id'))
        .order_by('age')
    )
    age_labels = [str(x['age']) for x in by_age]
    age_scores = [round(x['avg_score'] or 0) for x in by_age]

    # By gender
    by_gender = list(
        UserResult.objects.values('gender')
        .annotate(avg_score=Avg('score'), count=Count('id'))
    )
    gender_map = {'M': 'Erkak', 'F': 'Ayol'}
    gender_labels = [gender_map.get(x['gender'], x['gender']) for x in by_gender]
    gender_scores = [round(x['avg_score'] or 0) for x in by_gender]

    # Score distribution (buckets)
    buckets = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}
    for r in UserResult.objects.values_list('score', flat=True):
        if r <= 20:
            buckets['0-20'] += 1
        elif r <= 40:
            buckets['21-40'] += 1
        elif r <= 60:
            buckets['41-60'] += 1
        elif r <= 80:
            buckets['61-80'] += 1
        else:
            buckets['81-100'] += 1

    dist_labels = list(buckets.keys())
    dist_values = list(buckets.values())

    return render(request, 'iq_test/dashboard.html', {
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'last_10': last_10,
        'top_3': top_3,
        'leaderboard': leaderboard,
        'age_labels': json.dumps(age_labels),
        'age_scores': json.dumps(age_scores),
        'gender_labels': json.dumps(gender_labels),
        'gender_scores': json.dumps(gender_scores),
        'dist_labels': json.dumps(dist_labels),
        'dist_values': json.dumps(dist_values),
    })


def export_csv(request):
    """Export all results to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iq_results.csv"'
    response.write('\ufeff')  # BOM for Excel UTF-8

    writer = csv.writer(response)
    writer.writerow(['Ism', 'Yosh', 'Jinsi', 'Telefon', 'Ball', 'Sana'])

    gender_map = {'M': 'Erkak', 'F': 'Ayol'}
    for r in UserResult.objects.all():
        writer.writerow([
            r.name, r.age, gender_map.get(r.gender, r.gender),
            r.phone, r.score, r.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response


def export_excel(request):
    """Export all results to Excel."""
    wb = Workbook()
    ws = wb.active
    ws.title = 'IQ Natijalari'

    headers = ['Ism', 'Yosh', 'Jinsi', 'Telefon', 'Ball', 'Sana']
    ws.append(headers)

    gender_map = {'M': 'Erkak', 'F': 'Ayol'}
    for r in UserResult.objects.all():
        ws.append([
            r.name, r.age, gender_map.get(r.gender, r.gender),
            r.phone, r.score, r.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="iq_results.xlsx"'
    wb.save(response)
    return response
