from django.db.models import Q


STATUS = (
    ("Pending", "Pending"),
    ("Active", "Active"),
    ("Disabled", "Disabled")
)

WORKING_STATUS = (
    ("Looking for job", "Looking for job"),
    ("Internship", "Internship"),
    ("Working", "Working")
)


USER_TYPE = (
    ("superAdmin", "superAdmin"),
    ("admin", "admin"),
    ("graduate", "graduate"),
    ("volunteer", "volunteer"),
    ("host business", "host business")
)

SALARY_STATUS = (
    ("Paid", "Paid"),
    ("Unpaid", "Unpaid")
)

