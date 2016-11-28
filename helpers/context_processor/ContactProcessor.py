from main_app.models import Contact


def get_contacts(request):
    social_contact = Contact.objects.filter(contact_type=1)
    other_contact = Contact.objects.filter(contact_type=2)
    context = {
        'social_contact': social_contact,
        'other_contact': other_contact
    }

    return context
