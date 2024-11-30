from django.shortcuts import render
import openai
from django.core.exceptions import ObjectDoesNotExist

from .models import Questions, Responses as Answer

from django.http import JsonResponse
# Create your views here.

openai.api_key = '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'

def generate_question(request):
    topic = request.GET.get('topic', 'electrician vocational education')
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that generates questions for electricians in vocational education."},
            {"role": "user", "content": f"Generate a detailed question related to {topic}."},
        ]
    )
    question_text = response['choices'][0]['message']['content'].strip()
    # Use the correct field name
    question = Questions.objects.create(content=question_text, difficulty_level="medium", topic=topic)
    return JsonResponse({'question': question.content})


def submit_answer(request):
    try:
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer')

        # Validate that the question exists
        question = Questions.objects.get(id=question_id)

        # Save the answer
        answer = Answer.objects.create(question=question, text=answer_text)

        return JsonResponse({'message': 'Answer submitted successfully!', 'answer_id': answer.id})

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Question does not exist!'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)