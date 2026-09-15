from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from sheds.models import Shed, Tool

SHEDS = [
    ("Caversham Community Shed", "Caversham", "Dunedin"),
    ("St Kilda Tool Library", "St Kilda", "Dunedin"),
    ("North East Valley Shed", "North East Valley", "Dunedin"),
    ("Mosgiel Makers Shed", "Mosgiel", "Dunedin"),
    ("Riccarton Repair Hub", "Riccarton", "Christchurch"),
]

TOOLS = [
    ("Cordless drill", "18V, two batteries, charger in the case."),
    ("Circular saw", "185mm blade. Goggles required."),
    ("Wheelbarrow", "Steel tray, pneumatic tyre."),
    ("Extension ladder", "Extends to 4.2m."),
    ("Hedge trimmer", "Petrol. Bring your own fuel."),
    ("Post hole borer", "Two-person operation only."),
]


class Command(BaseCommand):
    help = "Populates the database with sheds and tools for local development."

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(username="ana")
        owner.set_password("toolshed123")
        owner.save()

        other, _ = User.objects.get_or_create(username="ben")
        other.set_password("toolshed123")
        other.save()

        staff, _ = User.objects.get_or_create(username="admin", is_staff=True)
        staff.set_password("toolshed123")
        staff.save()

        Tool.objects.all().delete()
        Shed.objects.all().delete()

        for index, (name, suburb, city) in enumerate(SHEDS):
            shed = Shed.objects.create(
                name=name,
                suburb=suburb,
                city=city,
                owner=owner if index % 2 == 0 else other,
            )
            for tool_name, description in TOOLS[: 2 + (index % 3)]:
                Tool.objects.create(
                    shed=shed, name=tool_name, description=description
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded %d sheds and %d tools."
                % (Shed.objects.count(), Tool.objects.count())
            )
        )