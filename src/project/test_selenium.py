import logging
from dataclasses import dataclass
from enum import Enum

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from django.utils.translation import gettext_lazy as _

from apps.users.models import User

logging.basicConfig(level=logging.INFO)


@dataclass
class SampleUser:
    email: str
    password: str
    name: str
    surnames: str
    organization_name: str


class Strings(Enum):
    """
    Collect all the strings that you plan to use to find elements in the code
    that are susceptible to translation here.
    That way it will be easier to maintain the right version of the string
    whenever some text is changed.

    Also, during development we might only have english versions of the strings,
    but when applying the translations, all of them will need to be updated
    here.
    """

    SUPERUSER_EMAIL = "hola@codi.coop"
    SUPERUSER_PASSWORD = "<PASSWORD>"
    MENU_LOGIN = _("Iniciar sessió")
    MENU_ADMIN = _("Panell d'administració")
    ADMIN_TITLE = _("Administració del lloc | Grappelli")


@override_settings(
    ALLOWED_HOSTS=["*"],
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    POST_OFFICE={
        "BACKENDS": {
            "default": "django.core.mail.backends.locmem.EmailBackend",
        },
        "DEFAULT_PRIORITY": "now",
    },
)
class MySeleniumTests(StaticLiveServerTestCase):
    """
    STATICFILES_STORAGE + StaticLiveServerTestCase vs LiveServerTestCase:
    Just using LiveServerTestCase it will not work because the tests run with
    debug disabled, meaning that it will trigger Whitenoise's static files
    indexation.
    For that to work, the static files need to be there, therefore, the tests
    will only work if you run `collectstatic` before running the tests.

    We can avoid Whitenoise to crash by overriding the setting STATICFILES_STORAGE
    to the default that Django uses.

    But then, Django will still try to serve the static files, so we need to
    extend StaticLiveServerTestCase because this class overrides the static
    serving behaviour to do the same that it does with DEBUG enabled - that is,
    to serve the files without any need to `collectstatic` first.
    """

    host = "boilerplate-app"
    # Uncomment this code if you want Selenium to connect to the actual web
    # service instead of the test one. Is assuming that Gunicorn is starting
    # it at the port 8000, because you have to use the internal port and
    # not the one that Docker is exposing outside.
    #
    # Beware that Selenium will be using the database in the state that you
    # have it now, but those tests are designed to work only with a fresh
    # database, and also that the override_settings is only affecting the test
    # server that you will not be using.
    # live_server_url = 'http://{}:8000'.format(
    #     socket.gethostbyname(socket.gethostname())
    # )
    obj_user1 = None
    obj_user2 = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # Disable sandboxing for Docker
        cls.selenium = webdriver.Remote(
            command_executor="http://boilerplate-selenium:4444/wd/hub", options=options
        )
        cls.selenium.implicitly_wait(10)  # Set implicit wait time
        cls.sample_data = {
            "first_user": SampleUser(
                email="hola+usuari1@codi.coop",
                password="0pl,9okm8ijn",
                name="Primer usuari",
                surnames="Cognoms usuari 1",
                organization_name="Organització de prova",
            ),
            "second_user": SampleUser(
                email="hola+usuari2@codi.coop",
                password="0pl,9okm8ijn",
                name="Segon usuari",
                surnames="Cognoms usuari 2",
                organization_name="Organització de prova",
            ),
            "third_user": SampleUser(
                email="hola+usuari3@codi.coop",
                password="0pl,9okm8ijn",
                name="Tercer usuari",
                surnames="Cognoms usuari 3",
                organization_name="Organització de prova",
            ),
        }

    @classmethod
    def tearDownClass(cls):
        # Close the Selenium WebDriver
        cls.selenium.quit()
        super().tearDownClass()

    def reverse_absolute_url(self, reverse_string):
        return self.absolute_url_of_path(reverse(reverse_string))

    def absolute_url_of_path(self, path):
        return f"{self.live_server_url}{path}"

    def click_non_interactable_element(self, element):
        # Checkboxes are not rendered as is, but hidden by CSS and replaced with
        # other elements, with the purpose of styling them better.
        # Because of that, you cannot send a click() or interact with the
        # checkbox directly from Selenium; it'll throw the error:
        # selenium.common.exceptions.ElementNotInteractableException: Message:
        # element not interactable
        # The simplest solution is to send the click via JS:
        self.selenium.execute_script("arguments[0].click();", element)

    def select_element_by_text(self, text):
        """
        Select an element by its text
        """
        elements = self.selenium.find_elements(
            By.XPATH,
            f"//*[contains(text(), '{text}')]",
        )
        return elements[0] if elements else None

    def test_selenium(self):
        """
        Selenium tests controller

        We need the Selenium flow to follow a specific order, because each action
        will probably depend on the data and changes produced by previous ones.

        If we do that in different tests, we cannot ensure this order and also
        the principle is to make tests that are standalone.

        Because of that, we're using a single test method and splitting it
        in other private methods to make it more organized.
        """

        # Preparations
        self._resize()
        self._create_superuser()

        # Fer login amb el compte d'admin que crea per defecte.
        # Verifica que al menú de l'app apareix el botó per anar a l'admin.
        self._admin_login()

        logging.info("Test finished.")

    def _resize(self):
        """
        Elements need to be in viewport to be interactable.
        For instance, we cannot send a click() to a checkbox if it's not
        visible, so we either resize the browser window to make everything
        visible or we have to be scrolling to each element when that happens.
        """
        self.selenium.get(self.live_server_url)
        logging.info(f"Opened: {self.live_server_url}")
        logging.info(f"Title: {self.selenium.title}")
        self.selenium.set_window_size(500, 2000)

    def _create_superuser(self):
        User.objects.create_superuser(
            email=str(Strings.SUPERUSER_EMAIL),
            password=str(Strings.SUPERUSER_PASSWORD),
        )

    def _login(self, user, password):
        self.selenium.get(self.live_server_url)
        # The home page will probably be the login page, but to make sure that
        # we reach the login page, we open de burger menu and navigate to
        # sign-in.
        burguer_menu = self.selenium.find_element(
            By.ID,
            "burger_button",
        )
        burguer_menu.click()
        login_menu_option = self.select_element_by_text(str(Strings.MENU_LOGIN))
        login_menu_option.click()
        logging.info(f"Opened: {self.selenium.current_url}")
        logging.info(f"Title: {self.selenium.title}")

        login_user = self.selenium.find_element(By.ID, "username_id")
        login_password = self.selenium.find_element(By.ID, "password_id")

        login_user.send_keys(user)
        login_password.send_keys(password)
        login_password.send_keys(Keys.RETURN)

    def _admin_login(self):
        self._login(str(Strings.SUPERUSER_EMAIL), str(Strings.SUPERUSER_PASSWORD))
        burguer_menu = self.selenium.find_element(
            By.ID,
            "burger_button",
        )
        burguer_menu.click()
        admin_menu = self.select_element_by_text(str(Strings.MENU_ADMIN))
        admin_menu.click()
        logging.info(self.selenium.current_url)
        logging.info(self.selenium.title)
        assert str(Strings.ADMIN_TITLE) in self.selenium.title
        logging.info("Logged in to admin with initial superuser.")
