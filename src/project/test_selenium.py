import logging
from dataclasses import dataclass
from enum import Enum

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from django.utils.translation import gettext as _

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

    # IMPORTANT, ABOUT TRANSLATIONS:
    If you assert strings, i.e. like this:
        assert Strings.ADMIN_TITLE.value in self.selenium.title
    You need to be using 'gettext', NOT gettext_lazy.

    If for some reason you need to switch to gettext_lazy, these assertions will
    fail. In this case you should change all the assertions to something like
    this:
        assert str(Strings.ADMIN_TITLE.value) in self.selenium.title

    That way, the str() will force the resolution of the translation, instead of
    sending an object.

    """

    MENU_LOGIN = _("Log in")
    MENU_ADMIN = _("Administration panel")
    ADMIN_TITLE = _("Administració del lloc | Lloc administratiu de Django")
    LOGOUT = _("Log out")
    SIGNUP_TITLE = _("Projecte App | Registrar-se")
    SEND = _("Send")


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

    def burger_menu_action(self):
        burger_menu = self.selenium.find_element(
            By.ID,
            "burger_button",
        )
        burger_menu.click()

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

        # Fer login amb el compte d'admin que crea per defecte.
        # Verifica que al menú de l'app apareix el botó per anar a l'admin.
        self._admin_login()
        logging.info("Test Login finished.")

        # Crea un nou usuari.
        # Verifica que al menú de l'app apareix el botó per crear un usuari new.
        self._admin_signup()
        logging.info("Test Signup finished.")

        self._admin_verify_email()
        logging.info("Test Verify email finished.")

        logging.info("############################")
        logging.info("#### All tests finished ####")
        logging.info("############################")

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

    def _login(self, user, password):
        self.selenium.get(self.live_server_url)
        # The home page will probably be the login page, but to make sure that
        # we reach the login page, we open de burger menu and navigate to
        # sign-in.
        self.burger_menu_action()
        login_menu_option = self.selenium.find_element(By.ID, "menu_login")
        login_menu_option.click()
        logging.info(f"Opened: {self.selenium.current_url}")
        logging.info(f"Title: {self.selenium.title}")

        login_user = self.selenium.find_element(By.ID, "id_username")
        login_password = self.selenium.find_element(By.ID, "id_password")

        login_user.send_keys(user)
        login_password.send_keys(password)
        login_password.send_keys(Keys.RETURN)

    def _admin_login(self):
        self._login(
            settings.DJANGO_SUPERUSER_EMAIL,
            settings.DJANGO_SUPERUSER_PASSWORD,
        )
        self.burger_menu_action()
        admin_menu = self.select_element_by_text(Strings.MENU_ADMIN.value)
        admin_menu.click()
        logging.info(self.selenium.current_url)
        logging.info(self.selenium.title)
        assert Strings.ADMIN_TITLE.value in self.selenium.title
        logging.info("Logged in to admin with initial superuser.")

    def _signup(self):
        # Log out to return to the home page
        admin_menu = self.select_element_by_text(Strings.LOGOUT.value)
        admin_menu.click()

        # Open the main menu to select the Sign Up option.
        self.burger_menu_action()

        signup_menu_option = self.selenium.find_element(By.ID, "menu_signup")
        signup_menu_option.click()
        logging.info(f"Opened: {self.selenium.current_url}")
        logging.info(f"Title: {self.selenium.title}")

        signup_name = self.selenium.find_element(By.ID, "id_name")
        signup_surnames = self.selenium.find_element(By.ID, "id_surnames")
        signup_password1 = self.selenium.find_element(By.ID, "id_password1")
        signup_password2 = self.selenium.find_element(By.ID, "id_password2")
        signup_email = self.selenium.find_element(By.ID, "id_email")
        signup_accept_conditions = self.selenium.find_element(By.ID,
                                                              "id_accept_conditions")

        signup_name.send_keys("test_name")
        signup_surnames.send_keys("test_surnames")
        signup_password1.send_keys("test_password1")
        signup_password2.send_keys("test_password2")
        signup_email.send_keys("test@email.com")
        signup_accept_conditions.click()
        signup_password2.send_keys(Keys.RETURN)

    def _admin_signup(self):
        self._signup()
        logging.info(self.selenium.current_url)
        logging.info(self.selenium.title)
        assert Strings.SIGNUP_TITLE.value in self.selenium.title
        logging.info("Sign up to admin.")

    def _verify_email(self):
        # Verify email
        button_alert = self.selenium.find_element(By.ID, "id_verify_email")
        button_alert.click()

        logging.info(f"Opened: {self.selenium.current_url}")
        logging.info(f"Title: {self.selenium.title}")

        send_button = self.select_element_by_text(Strings.SEND.value)
        send_button.click()

    def _admin_verify_email(self):
        self._verify_email()
        logging.info(self.selenium.current_url)
        logging.info(self.selenium.title)

        logging.info("Verified email.")
