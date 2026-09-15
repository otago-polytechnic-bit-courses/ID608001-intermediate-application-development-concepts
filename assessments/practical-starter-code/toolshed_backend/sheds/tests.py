from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Shed, Tool


class ToolShedBehaviourTests(APITestCase):
    def setUp(self):
        self.ana = User.objects.create_user(username="ana", password="pw-ana")
        self.ben = User.objects.create_user(username="ben", password="pw-ben")
        self.admin = User.objects.create_user(
            username="admin", password="pw-admin", is_staff=True
        )

        self.caversham = Shed.objects.create(
            name="Caversham Community Shed",
            suburb="Caversham",
            city="Dunedin",
            owner=self.ana,
        )
        self.riccarton = Shed.objects.create(
            name="Riccarton Repair Hub",
            suburb="Riccarton",
            city="Christchurch",
            owner=self.ben,
        )

        Tool.objects.create(
            shed=self.caversham, name="Cordless drill", description="18V."
        )
        Tool.objects.create(
            shed=self.caversham, name="Circular saw", description="185mm blade."
        )
        Tool.objects.create(
            shed=self.riccarton, name="Wheelbarrow", description="Steel tray."
        )

    def authenticate(self, username, password):
        response = self.client.post(
            "/api/login/",
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response.data["access"]
        )

    # ------------------------------------------------------------------
    # Listing sheds
    # ------------------------------------------------------------------

    def test_shed_list_is_public(self):
        response = self.client.get("/api/sheds/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_shed_list_item_has_exactly_these_fields(self):
        response = self.client.get("/api/sheds/")
        item = response.data[0]
        self.assertEqual(
            sorted(item.keys()),
            ["city", "id", "name", "suburb", "tool_count"],
        )

    def test_shed_list_reports_tool_counts(self):
        response = self.client.get("/api/sheds/")
        counts = {item["name"]: item["tool_count"] for item in response.data}
        self.assertEqual(counts["Caversham Community Shed"], 2)
        self.assertEqual(counts["Riccarton Repair Hub"], 1)

    def test_shed_list_can_be_filtered_by_city(self):
        response = self.client.get("/api/sheds/?city=Christchurch")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Riccarton Repair Hub")

    # ------------------------------------------------------------------
    # A single shed
    # ------------------------------------------------------------------

    def test_shed_detail_is_public(self):
        response = self.client.get("/api/sheds/%d/" % self.caversham.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Caversham Community Shed")

    def test_shed_detail_nests_its_tools(self):
        response = self.client.get("/api/sheds/%d/" % self.caversham.id)
        names = sorted(tool["name"] for tool in response.data["tools"])
        self.assertEqual(names, ["Circular saw", "Cordless drill"])

    def test_nested_tool_carries_id_name_and_description(self):
        response = self.client.get("/api/sheds/%d/" % self.caversham.id)
        tool = response.data["tools"][0]
        for field in ("id", "name", "description"):
            self.assertIn(field, tool)

    def test_shed_detail_includes_a_created_at_string(self):
        response = self.client.get("/api/sheds/%d/" % self.caversham.id)
        self.assertIn("created_at", response.data)
        self.assertIsInstance(str(response.data["created_at"]), str)

    def test_missing_shed_returns_404(self):
        response = self.client.get("/api/sheds/99999/")
        self.assertEqual(response.status_code, 404)

    def test_tools_endpoint_lists_tools_for_a_shed(self):
        response = self.client.get("/api/sheds/%d/tools/" % self.caversham.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    # ------------------------------------------------------------------
    # Creating a shed
    # ------------------------------------------------------------------

    def test_create_requires_authentication(self):
        response = self.client.post(
            "/api/sheds/",
            {"name": "Anywhere", "suburb": "Anywhere", "city": "Dunedin"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_create_returns_201_for_an_authenticated_user(self):
        self.authenticate("ana", "pw-ana")
        response = self.client.post(
            "/api/sheds/",
            {"name": "Green Island Shed", "suburb": "Green Island", "city": "Dunedin"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Green Island Shed")

    def test_create_assigns_the_requesting_user_as_owner(self):
        self.authenticate("ana", "pw-ana")
        self.client.post(
            "/api/sheds/",
            {"name": "Green Island Shed", "suburb": "Green Island", "city": "Dunedin"},
            format="json",
        )
        created = Shed.objects.get(name="Green Island Shed")
        self.assertEqual(created.owner, self.ana)

    def test_create_rejects_a_blank_name(self):
        self.authenticate("ana", "pw-ana")
        response = self.client.post(
            "/api/sheds/",
            {"name": "", "suburb": "Green Island", "city": "Dunedin"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    # ------------------------------------------------------------------
    # Updating a shed
    # ------------------------------------------------------------------

    def test_update_requires_authentication(self):
        response = self.client.put(
            "/api/sheds/%d/" % self.caversham.id,
            {"name": "Renamed"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_update_is_refused_for_a_non_owner(self):
        self.authenticate("ben", "pw-ben")
        response = self.client.put(
            "/api/sheds/%d/" % self.caversham.id,
            {"name": "Renamed"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_update_is_allowed_for_the_owner(self):
        self.authenticate("ana", "pw-ana")
        response = self.client.put(
            "/api/sheds/%d/" % self.caversham.id,
            {"name": "Caversham Tool Library"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.caversham.refresh_from_db()
        self.assertEqual(self.caversham.name, "Caversham Tool Library")

    def test_update_rejects_a_blank_name(self):
        self.authenticate("ana", "pw-ana")
        response = self.client.put(
            "/api/sheds/%d/" % self.caversham.id,
            {"name": ""},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    # ------------------------------------------------------------------
    # Deleting a shed
    # ------------------------------------------------------------------

    def test_delete_requires_authentication(self):
        response = self.client.delete("/api/sheds/%d/" % self.caversham.id)
        self.assertEqual(response.status_code, 401)

    def test_delete_is_refused_for_a_non_owner(self):
        self.authenticate("ben", "pw-ben")
        response = self.client.delete("/api/sheds/%d/" % self.caversham.id)
        self.assertEqual(response.status_code, 403)

    def test_delete_is_allowed_for_the_owner(self):
        self.authenticate("ana", "pw-ana")
        response = self.client.delete("/api/sheds/%d/" % self.caversham.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Shed.objects.filter(id=self.caversham.id).exists())

    def test_delete_is_allowed_for_staff_who_do_not_own_the_shed(self):
        self.authenticate("admin", "pw-admin")
        response = self.client.delete("/api/sheds/%d/" % self.caversham.id)
        self.assertEqual(response.status_code, 204)

    def test_deleting_a_shed_removes_its_tools(self):
        self.authenticate("ana", "pw-ana")
        self.client.delete("/api/sheds/%d/" % self.caversham.id)
        self.assertEqual(Tool.objects.filter(shed_id=self.caversham.id).count(), 0)

    # ------------------------------------------------------------------
    # Logging in
    # ------------------------------------------------------------------

    def test_login_returns_an_access_and_refresh_token(self):
        response = self.client.post(
            "/api/login/",
            {"username": "ana", "password": "pw-ana"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_rejects_a_wrong_password(self):
        response = self.client.post(
            "/api/login/",
            {"username": "ana", "password": "not-the-password"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)