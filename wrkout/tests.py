# "python manage.py test wrkout.tests" to run the tests.
# will be adding more tests as we go


import os
import re
import importlib
import warnings
import inspect
import tempfile

from django.urls import reverse, resolve
from django.test import TestCase
from django.conf import settings
import wrkout.models
from wrkout import forms
from django.db import models
from django.contrib.auth.models import User
from wrkout.models import Exercise, Workout
from populate_wrkout import populate
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Tests1(TestCase):
    
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.wrkout_templates_dir = os.path.join(self.templates_dir, 'wrkout')

    def test_templates_directory_exists(self):
        """
        Does the templates/ directory exist?
        """
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")

    def test_wrkout_templates_directory_exists(self):
        """
        Does the templates/wrkout/ directory exist?
        """
        directory_exists = os.path.isdir(self.wrkout_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The Wrkout templates directory does not exist.{FAILURE_FOOTER}")

    def test_template_dir_setting(self):
        """
        Does the TEMPLATE_DIR setting exist, and does it point to the right directory?
        """
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined!{FAILURE_FOOTER}")

        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")

    def test_template_lookup_path(self):
        """
        Does the TEMPLATE_DIR value appear within the lookup paths for templates?
        """
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False

        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)

            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True

        self.assertTrue(found_path, f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")

    def test_templates_exist(self):
        """
        Do templates exist?
        """
        base_path = os.path.join(self.wrkout_templates_dir, 'base.html')
        browse_path = os.path.join(self.wrkout_templates_dir, 'browse.html')
        login_path = os.path.join(self.wrkout_templates_dir, 'login.html')
        register_path = os.path.join(self.wrkout_templates_dir, 'register.html')
        workout_path = os.path.join(self.wrkout_templates_dir, 'workout.html')
        create_workout_path = os.path.join(self.wrkout_templates_dir, 'create_workout.html')
        create_exercise_path = os.path.join(self.wrkout_templates_dir, 'create_exercise.html')



        self.assertTrue(os.path.isfile(base_path), f"{FAILURE_HEADER}Your base.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(browse_path), f"{FAILURE_HEADER}Your browse.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(login_path), f"{FAILURE_HEADER}Your login.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(register_path), f"{FAILURE_HEADER}Your register.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        #self.assertTrue(os.path.isfile(workout_path), f"{FAILURE_HEADER}Your workout.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        #self.assertTrue(os.path.isfile(create_workout_path), f"{FAILURE_HEADER}Your create_workout.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        #self.assertTrue(os.path.isfile(create_exercise_path), f"{FAILURE_HEADER}Your create_exercise.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
    
    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')

        for line in f:
            line = line.strip()

            if line.startswith('db.sqlite3'):
                return True

        f.close()
        return False

    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist, and does it have a default configuration?
        """
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. Check the start of Chapter 5.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable. Check the start of Chapter 5.{FAILURE_FOOTER}")

    def test_gitignore_for_database(self):
        """
        If you are using a Git repository and have set up a .gitignore, checks to see whether the database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        if git_base_dir.startswith('fatal'):
            warnings.warn("You don't appear to be using a Git repository for your codebase. Although not strictly required, it's *highly recommended*. Skipping this test.")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')

            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3' -- you should exclude the database binary file from all commits to your Git repository.{FAILURE_FOOTER}")
            else:
                warnings.warn("You don't appear to have a .gitignore file in place in your repository. We ask that you consider this! Read the Don't git push your Database paragraph in Chapter 5.")

    def views_use_correct_templates(self):
        
        """
        Do views use templates? Are they the correct ones?
        """
        
        self.show_workout = self.client.get(reverse('wrkout:show_workout'))
        self.browse_popular_workouts = self.client.get(reverse('wrkout:browse_popular_workouts'))
        self.browse_popular_exercises = self.client.get(reverse('wrkout:browse_popular_exercises'))
        self.browse_newest_workouts = self.client.get(reverse('wrkout:browse_newest_workouts'))
        self.browse_newest_exercises = self.client.get(reverse('wrkout:browse_newest_exercises'))
        self.register = self.client.get(reverse('wrkout:register'))
        self.user_login = self.client.get(reverse('wrkout:browse_popular_workouts'))
        self.create_workout = self.client.get(reverse('wrkout:create_workout'))
        self.create_exercise = self.client.get(reverse('wrkout:create_exercise'))
        
        self.assertTemplateUsed(self.show_workout, 'wrkout/workout.html', f"{FAILURE_HEADER}Your show_workout() view does not use the expected wrkout/workout.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.browse_popular_workouts, 'wrkout/browse.html', f"{FAILURE_HEADER}Your browse_popular_workouts() view does not use the expected wrkout/workout.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.browse_popular_exercises, 'wrkout/browse.html', f"{FAILURE_HEADER}Your browse_popular_exercises() view does not use the expected wrkout/browse.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.browse_newest_workouts, 'wrkout/browse.html', f"{FAILURE_HEADER}Your browse_newest_workouts() view does not use the expected wrkout/browse.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.browse_newest_exercises, 'wrkout/browse.html', f"{FAILURE_HEADER}Your browse_newest_exercises view does not use the expected wrkout/browse.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.register, 'wrkout/register.html', f"{FAILURE_HEADER}Your register() view does not use the expected wrkout/register.htmll template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.user_login, 'wrkout/login.html', f"{FAILURE_HEADER}Your user_login() view does not use the expected wrkout/login.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.create_workout, 'wrkout/create_workout.html', f"{FAILURE_HEADER}Your create_workout() view does not use the expected wrkout/create_workout.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.create_exercise, 'wrkout/create_exercise.html', f"{FAILURE_HEADER}Your create_exercise() view does not use the expected wrkout/create_exercise.html template.{FAILURE_FOOTER}")

    def test_installed_apps(self):
        """
        Checks whether the 'django.contrib.auth' app has been included in INSTALLED_APPS.
        """
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)
        
    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in wrkout.models? If so, are all the required attributes present?
        Assertion fails if we can't assign values to all the fields required (i.e. one or more missing).
        """
        self.assertTrue('UserProfile' in dir(wrkout.models))

        user_profile = wrkout.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'UserID': 123,
            'Slug': 'whatever',
            'ProfilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'UserAccount': create_user_object(),
        }

        expected_types = {
            'UserID': models.AutoField,
            'Slug': models.SlugField,
            'ProfilePicture': models.ImageField,
            'UserAccount': models.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name
            

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        user_profile.save()
        
    def test_user_form(self):
        """
        Tests whether UserForm is in the correct place, and whether the correct fields have been specified for it.
        """
        self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserForm class in Wrkout's forms.py module. Did you create it in the right place?{FAILURE_FOOTER}")

        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}Your UserForm does not match up to the User model. Check your Meta definition of UserForm and try again.{FAILURE_FOOTER}")

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

    def test_user_profile_form(self):
    
        """
        Tests whether UserProfileForm is in the correct place, and whether the correct fields have been specified for it.
        """
        self.assertTrue('UserProfileForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserProfileForm class in Wrkout's forms.py module. Did you create it in the right place?{FAILURE_FOOTER}")

        user_profile_form = forms.UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), wrkout.models.UserProfile, f"{FAILURE_HEADER}Your UserProfileForm does not match up to the UserProfile model. Check your Meta definition of UserProfileForm and try again.{FAILURE_FOOTER}")

        fields = user_profile_form.fields

        expected_fields = {
            'ProfilePicture': django_fields.ImageField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserProfile form. Check you have complied with the specification, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

    """
    
    def test_login_functionality(self):
        
        #Tests the login functionality. A user should be able to log in, and should be redirected to the Wrkout homepage.
        
        user_object = create_user_object()

        response = self.client.post(reverse('wrkout:login'), {'username': 'testuser', 'password': 'testabc123'})

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead. Check your login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('wrkout:index'), f"{FAILURE_HEADER}We were not redirected to the Wrkout homepage after logging in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

    """ #activate test when index view exists/when login redirects do something else than index
    
    def test_bad_request(self):
        """
        Tries to access the create_workout view when not logged in.
        This should redirect the user to the login page.
        """
        response = self.client.get(reverse('wrkout:create_workout'))

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}We tried to access a restricted view when not logged in. We expected to be redirected, but were not. Check your restricted() view.{FAILURE_FOOTER}")
        self.assertTrue(response.url.startswith(reverse('wrkout:home')), f"{FAILURE_HEADER}We tried to access a restricted view when not logged in, and were expecting to be redirected to the home page. But we were not! Please check your create_workouts view.{FAILURE_FOOTER}")

"""
    def test_logged_in_links(self):
        
        #Checks for links that should only be displayed when the user is logged in.
        
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('wrkout:home')).content.decode()

        # These should be present.
        #self.assertTrue('href="/wrkout/workouts/create"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        #self.assertTrue('href="/wrkout/exercises/create"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        #self.assertTrue('href="/wrkout/logout/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")

        # These should not be present.
        self.assertTrue('href="/wrkout/login/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        self.assertTrue('href="/wrkout/register/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")

    def test_logged_out_links(self):
        
        #Checks for links that should only be displayed when the user is not logged in.
        
        content = self.client.get(reverse('wrkout:home')).content.decode()

        # These should be present.
        self.assertTrue('href="/wrkout/login/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        self.assertTrue('href="/wrkout/register/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")

        # These should not be present.
        #self.assertTrue('href="/wrkout/workouts/create"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        #self.assertTrue('href="/wrkout/exercises/create"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        #self.assertTrue('href="/wrkout/logout/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
""" #activate these when something uses the base.html
    
def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user   
    