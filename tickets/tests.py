from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Ticket
from teams.models import Profile

class TicketModelTest(TestCase):
    """
    Unit tests for the Ticket model itself.
    """
    # Unit Test (Scenario 1)
    def test_ticket_status_defaults_to_todo(self):
        user = User.objects.create(username='reporter')
        ticket = Ticket.objects.create(title='Test Ticket', description='A test.', reported_by=user)
        self.assertEqual(ticket.status, Ticket.Status.TO_DO)

class TicketAssignmentTest(TestCase):
    """
    Integration tests for relationships between Users and Tickets.
    """
    def setUp(self):
        self.reporter = User.objects.create_user(username='reporter', password='password123')
        self.developer = User.objects.create_user(username='developer', password='password123')
        self.developer.profile.role = Profile.Role.DEVELOPER
        self.developer.profile.save()

    # Integration Test (Scenario 2)
    def test_assignment_logic(self):
        ticket1 = Ticket.objects.create(title='Ticket 1', description='Desc 1', reported_by=self.reporter, assigned_to=self.developer)
        ticket2 = Ticket.objects.create(title='Ticket 2', description='Desc 2', reported_by=self.reporter)
        
        developer_tickets = self.developer.assigned_tickets.all()
        self.assertEqual(developer_tickets.count(), 1)
        self.assertIn(ticket1, developer_tickets)
        self.assertNotIn(ticket2, developer_tickets)

class PermissionsAndStatusUpdateTest(TestCase):
    """
    Functional tests for view permissions and the ticket update workflow.
    This replaces the conceptual test with a real implementation test.
    """
    def setUp(self):
        # Create users with different roles
        self.reporter = User.objects.create_user(username='reporter', password='password123')
        self.developer1 = User.objects.create_user(username='dev1', password='password123')
        self.developer1.profile.role = Profile.Role.DEVELOPER
        self.developer1.profile.save()
        self.developer2 = User.objects.create_user(username='dev2', password='password123')
        self.developer2.profile.role = Profile.Role.DEVELOPER
        self.developer2.profile.save()

        # Create a ticket assigned to developer1
        self.ticket = Ticket.objects.create(
            title='Test Ticket for Permissions',
            description='A test.',
            reported_by=self.reporter,
            assigned_to=self.developer1
        )
        self.update_url = reverse('update_ticket_status', args=[self.ticket.pk])

    # Functional Test (Scenario 3 - Real Implementation)
    def test_reporter_cannot_update_status(self):
        """
        A user with the 'Reporter' role attempts to update a ticket's status.
        Expected Result: The view should return an HTTP 403 Forbidden response.
        """
        self.client.login(username='reporter', password='password123')
        response = self.client.post(self.update_url, {'status': Ticket.Status.IN_PROGRESS})
        self.assertEqual(response.status_code, 403) # 403 is PermissionDenied

    def test_unassigned_developer_cannot_update_status(self):
        """
        A developer who is NOT assigned to the ticket attempts to update it.
        Expected Result: The view should return an HTTP 403 Forbidden response.
        """
        self.client.login(username='dev2', password='password123')
        response = self.client.post(self.update_url, {'status': Ticket.Status.IN_PROGRESS})
        self.assertEqual(response.status_code, 403)

    def test_assigned_developer_can_update_status(self):
        """
        The assigned developer attempts to update the status.
        Expected Result: The action succeeds, the status is updated, and the user is redirected.
        """
        self.client.login(username='dev1', password='password123')
        response = self.client.post(self.update_url, {'status': Ticket.Status.RESOLVED})
        
        # Check for a successful redirect
        self.assertEqual(response.status_code, 302)
        
        # Check the database to confirm the status was actually changed
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.RESOLVED)

class CSRFTest(TestCase):
    """
    Security tests for Cross-Site Request Forgery protection.
    """
    def setUp(self):
        # Create a client that enforces CSRF checks for this specific test
        self.client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    # Security Test (Scenario 6)
    def test_csrf_protection_on_new_ticket_form(self):
        """
        A malicious user attempts to submit the New Ticket form from an external site.
        Expected Result: The form submission should fail with a CSRF token error (403).
        """
        response = self.client.post(reverse('create_ticket'), {
            'title': 'CSRF Test', 
            'description': 'This should fail'
        })
        self.assertEqual(response.status_code, 403) # Forbidden due to missing CSRF token