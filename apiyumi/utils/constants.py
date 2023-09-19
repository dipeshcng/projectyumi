from django.db.models import Q


STATUS = (
    ("Pending", "Pending"),
    ("Active", "Active"),
    ("Disabled", "Disabled")
)

WORKING_STATUS = (
    (1, "Looking For Job"),
    (2, "Internship"),
    (3, "Working")
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

