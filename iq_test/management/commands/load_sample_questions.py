"""
Management command to load sample IQ test questions.
O'zbek tilida mantiqiy savollar.
"""

from django.core.management.base import BaseCommand
from iq_test.models import Question


SAMPLE_QUESTIONS = [
    {
        'text': '2, 4, 6, 8, ? - Ketma-ketlikda keyingi son qaysi?',
        'option_a': '9',
        'option_b': '10',
        'option_c': '11',
        'option_d': '12',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': 'Agar barcha gulqo\'ng\'izlar qora va bu hayvon gulqo\'ng\'iz bo\'lsa, bu hayvon qora. Bu qanday xulosa?',
        'option_a': 'Noto\'g\'ri',
        'option_b': 'To\'g\'ri',
        'option_c': 'Aniqlashtirib bo\'lmaydi',
        'option_d': 'Chalkash',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': '5 + 3 × 2 = ?',
        'option_a': '16',
        'option_b': '11',
        'option_c': '13',
        'option_d': '10',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': 'Bir haftada necha kun bor?',
        'option_a': '5',
        'option_b': '6',
        'option_c': '7',
        'option_d': '8',
        'correct_answer': 'c',
        'difficulty': 'easy',
    },
    {
        'text': '1, 1, 2, 3, 5, 8, ? - Fibonachchi ketma-ketligida keyingi son?',
        'option_a': '11',
        'option_b': '12',
        'option_c': '13',
        'option_d': '14',
        'correct_answer': 'c',
        'difficulty': 'medium',
    },
    {
        'text': 'Agar B dan katta, B esa C dan katta bo\'lsa, A C dan qanday?',
        'option_a': 'Kichik',
        'option_b': 'Katta',
        'option_c': 'Teng',
        'option_d': 'Aniqlab bo\'lmaydi',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': 'OT - 2 harf, KITOB - 5 harf. NIMA - nechta harf?',
        'option_a': '3',
        'option_b': '4',
        'option_c': '2',
        'option_d': '5',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': '3, 6, 12, 24, ? - Keyingi son qaysi?',
        'option_a': '36',
        'option_b': '48',
        'option_c': '42',
        'option_d': '30',
        'correct_answer': 'b',
        'difficulty': 'medium',
    },
    {
        'text': 'Kun botguncha qayerda bo\'ladi?',
        'option_a': 'Sharqda',
        'option_b': 'G\'arbda',
        'option_c': 'Janubda',
        'option_d': 'Shimolda',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': '1, 4, 9, 16, 25, ? - Keyingi son?',
        'option_a': '30',
        'option_b': '32',
        'option_c': '36',
        'option_d': '40',
        'correct_answer': 'c',
        'difficulty': 'medium',
    },
    {
        'text': 'Hammasi odamlar o\'ladi. Sokrates odam. Demak...',
        'option_a': 'Sokrates o\'lmaydi',
        'option_b': 'Sokrates o\'ladi',
        'option_c': 'Ma\'lum emas',
        'option_d': 'Barcha odamlar Sokrates',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': '2, 3, 5, 7, 11, ? - Keyingi tub son?',
        'option_a': '12',
        'option_b': '13',
        'option_c': '14',
        'option_d': '15',
        'correct_answer': 'b',
        'difficulty': 'medium',
    },
    {
        'text': 'Agar hamma sigirlar sut beradi va Masha sigir bo\'lmasa, Masha sut beradimi?',
        'option_a': 'Ha',
        'option_b': 'Yo\'q',
        'option_c': 'Balki',
        'option_d': 'Ma\'lum emas',
        'correct_answer': 'b',
        'difficulty': 'medium',
    },
    {
        'text': 'O\'zbekiston poytaxti qayerda?',
        'option_a': 'Samarqand',
        'option_b': 'Buxoro',
        'option_c': 'Toshkent',
        'option_d': 'Andijon',
        'correct_answer': 'c',
        'difficulty': 'easy',
    },
    {
        'text': 'A, C, E, G, ? - Keyingi harf?',
        'option_a': 'H',
        'option_b': 'I',
        'option_c': 'J',
        'option_d': 'K',
        'correct_answer': 'b',
        'difficulty': 'medium',
    },
    {
        'text': '10 - 2 × 3 + 4 = ?',
        'option_a': '8',
        'option_b': '28',
        'option_c': '20',
        'option_d': '16',
        'correct_answer': 'a',
        'difficulty': 'medium',
    },
    {
        'text': 'Bir yilda necha oy bor?',
        'option_a': '10',
        'option_b': '11',
        'option_c': '12',
        'option_d': '13',
        'correct_answer': 'c',
        'difficulty': 'easy',
    },
    {
        'text': '1, 2, 4, 8, 16, ? - Keyingi son?',
        'option_a': '24',
        'option_b': '28',
        'option_c': '32',
        'option_d': '36',
        'correct_answer': 'c',
        'difficulty': 'medium',
    },
    {
        'text': 'Agar bugun payshanba bo\'lsa, 4 kun keyin qaysi kun?',
        'option_a': 'Yakshanba',
        'option_b': 'Dushanba',
        'option_c': 'Seshanba',
        'option_d': 'Shanba',
        'correct_answer': 'b',
        'difficulty': 'easy',
    },
    {
        'text': '5 × (3 + 2) - 4 = ?',
        'option_a': '21',
        'option_b': '19',
        'option_c': '25',
        'option_d': '15',
        'correct_answer': 'a',
        'difficulty': 'medium',
    },
]


class Command(BaseCommand):
    help = 'Sample IQ savollarini yuklash'

    def handle(self, *args, **options):
        created = 0
        for q_data in SAMPLE_QUESTIONS:
            _, is_new = Question.objects.get_or_create(
                text=q_data['text'],
                defaults={
                    'option_a': q_data['option_a'],
                    'option_b': q_data['option_b'],
                    'option_c': q_data['option_c'],
                    'option_d': q_data['option_d'],
                    'correct_answer': q_data['correct_answer'],
                    'difficulty': q_data['difficulty'],
                    'is_active': True,
                }
            )
            if is_new:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'{created} ta yangi savol qo\'shildi. Jami: {Question.objects.count()} ta savol.'))
