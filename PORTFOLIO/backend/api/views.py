from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            full_message = f"From: {name} <{email}>\n\n{message}"

            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=full_message,
                from_email=os.environ.get('EMAIL_HOST_USER'),
                recipient_list=[os.environ.get('EMAIL_RECEIVER')],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Email sent successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
