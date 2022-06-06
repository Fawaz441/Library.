from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from books.models import Book, BookBorrowRequest, PENDING, REJECTED, APPROVED

logger = get_task_logger(__name__)


@shared_task(name='reject_day_old_pending_requests')
def clean_old_pending_requests():
    a_day_ago = timezone.now() - timezone.timedelta(days=1)
    pending_requests = BookBorrowRequest.objects.filter(
        status=PENDING, created__lte=a_day_ago)
    pending_requests.update(status=REJECTED)
    return 'Rejected Day Old Pending Borrow Requests.'


@shared_task(name='suspend-students')
def suspend_students():
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    borrow_requests = BookBorrowRequest.objects.filter(
        student__is_active=True,
        status=APPROVED,
        book__current_borrower__isnull=False,
        approved_date__lte=three_days_ago,
        book_returned=False
    ).select_related('book')
    for request in borrow_requests:
        if request.student == request.book.current_borrower:
            request.student.is_active = False
            request.student.save()
        continue
    return 'Suspended Defaulting Students.'
