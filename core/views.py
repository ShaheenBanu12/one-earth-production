from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Blog, ContactMessage
from .forms import ContactForm


# ======================================================
# HOME (Contact + Blog Preview)
# ======================================================

def home(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            message = form.save()

            try:
                # Admin Notification
                send_mail(
                    subject=f"New Contact Message from {message.name}",
                    message=f"""
New enquiry received:

Name: {message.name}
Email: {message.email}
Company: {message.company}

Message:
{message.message}
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["hello@oneearth.co.uk"],
                    fail_silently=False,
                )

                # User Auto-Reply
                send_mail(
                    subject="We've received your message – One Earth",
                    message=f"""
Hi {message.name},

Thank you for contacting One Earth.

We’ve received your enquiry and will respond within 24 hours.

If your matter is urgent, please email:
hello@oneearth.co.uk

Best regards,
One Earth
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[message.email],
                    fail_silently=False,
                )

            except Exception:
                # Prevent crash if email fails
                messages.warning(
                    request,
                    "Your message was saved, but email delivery failed."
                )

            messages.success(
                request,
                "Thank you for contacting us. We will respond within 24 hours."
            )

            return redirect("home")  # Prevent form resubmission

    else:
        form = ContactForm()

    return render(request, "home.html", {
        "blogs": blogs,
        "form": form,
    })


# ======================================================
# BLOG LIST (With Pagination)
# ======================================================

def blog_list(request):
    blog_queryset = Blog.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(blog_queryset, 6)

    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    return render(request, "blog_list.html", {
        "blogs": blogs
    })


# ======================================================
# BLOG DETAIL
# ======================================================

def blog_detail(request, slug):
    blog = get_object_or_404(
        Blog,
        slug=slug,
        is_published=True
    )

    return render(request, "blog_detail.html", {
        "blog": blog
    })
