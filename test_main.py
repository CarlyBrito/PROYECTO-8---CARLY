import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from time import sleep

import data
from data import urban_routes_url


driver = webdriver.Chrome()


def retrieve_phone_code(driver) -> str:
    # Recupera el código de confirmación del teléfono desde los logs de red del navegador.
    code = None
    for _ in range(10):
        try:
            logs = [
                log["message"] for log in driver.get_log('performance')
                if log.get("message") and 'api/v1/number?number' in log.get("message")
            ]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
                break
        except WebDriverException:
            # Espera 10 segundos antes de intentar nuevamente
            time.sleep(10)
            continue

    if not code:
        raise Exception('No se encontró el código de confirmación del teléfono. \n'
                        'Utiliza "phone_code" solo después de haber solicitado el código en tu aplicación.')

    return code


class UrbanRoutesPage:
    # Localizadores para los elementos en la página Urban Routes
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    book_a_taxi_button = (By.XPATH, "//button[@class='button round' and text()='Pedir un taxi']")
    comfort_fare_button = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_input_box = (By.CLASS_NAME, "np-button")
    phone_popup_window_input_box = (By.ID, "phone")
    phone_popup_window_input_box_next = (By.XPATH, "(//button[@type='submit'])[1]")
    code_field = (By.ID, "code")
    code_confirm_button = (By.XPATH, "(//button[@type='submit'])[2]")
    payment_method_box = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]")
    add_cc_button = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[3]/div")
    cc_number_field = (By.ID, "number")
    cc_code_field = (By.XPATH, "(//input[@id='code'])[2]")
    add_cc_confirm_button = (By.XPATH, "//button[text()='Agregar']")
    exit_payment_popup_button = (By.XPATH, "(//button[@class='close-button section-close'])[3]")
    message_to_driver_field = (By.ID, 'comment')
    blanket_and_scarves_toggle = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
    ice_cream_counter = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
    book_service_button = (By.XPATH, "(//button[@type='button']//span)[1]")
    travel_requirements_section = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]")
    botton_go_taxi = (By.XPATH, "//*[@id='root']/div/div[3]/div[4]")
    window_popup_body_order = (By.XPATH, "//*[@id='root']/div/div[5]/div[2]")
    window_popup_go_taxi = (By.XPATH, "//*[@id='root']/div/div[5]/div[2]")


    def __init__(self, driver):
        # Inicializa la clase con el controlador de Selenium
        self.driver = driver

    def set_from(self, from_address):
        # Establece la dirección de 'Desde' en el campo correspondiente
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        # Establece la dirección de 'Hasta' en el campo correspondiente
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        # Obtiene el valor actual del campo 'Desde'
        return self.driver.find_element(*self.from_field).get_property('value')

    def set_route(self, from_address, to_address):
        # Establece la ruta ingresando las direcciones de 'Desde' y 'Hasta'
        self.set_from(from_address)
        self.set_to(to_address)

    def click_book_a_taxi_button(self):
        # Hace clic en el botón 'Pedir un taxi'
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.book_a_taxi_button))
        self.driver.find_element(*self.book_a_taxi_button).click()

    def select_comfort_fare(self):
        # Selecciona la tarifa 'Comfort'
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.comfort_fare_button))
        self.driver.find_element(*self.comfort_fare_button).click()

    def select_phone_number_field(self):
        # Espera a que la ventana emergente esté visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.phone_input_box))
        # Haz clic en el campo de entrada para asegurarte de que esté seleccionado
        self.driver.find_element(*self.phone_input_box).click()

    def enter_phone_number(self, phone_number):
        # Ingresa el número de teléfono en la ventana emergente
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.phone_popup_window_input_box))
        self.driver.find_element(*self.phone_popup_window_input_box).send_keys(phone_number)
        self.driver.find_element(*self.phone_popup_window_input_box_next).click()

    def add_payment_method(self, card_number, card_code):
        # Agrega un método de pago ingresando los detalles de la tarjeta
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.payment_method_box))
        self.driver.find_element(*self.payment_method_box).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_cc_button))
        self.driver.find_element(*self.add_cc_button).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.cc_number_field))
        self.driver.find_element(*self.cc_number_field).send_keys(card_number)

        self.driver.find_element(*self.cc_code_field).send_keys(card_code)
        self.driver.find_element(*self.cc_code_field).send_keys(Keys.TAB)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_cc_confirm_button))
        self.driver.find_element(*self.add_cc_confirm_button).click()

    def exit_payment_popup(self):
        # Cierra la ventana emergente del método de pago
        self.driver.find_element(*self.exit_payment_popup_button).click()

    def message_to_driver(self, message):
        # Envía un mensaje al conductor
        self.driver.find_element(*self.message_to_driver_field).send_keys(message)

    def select_blanket_and_scarves(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.blanket_and_scarves_toggle))
        # Encuentra el toggle switch dentro de la sección de requisitos del viaje
        self.driver.find_element(*self.blanket_and_scarves_toggle).click()

    def select_two_ice_creams(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ice_cream_counter))
        # Encuentra el toggle switch dentro de la sección de requisitos del viaje
        self.driver.find_element(*self.ice_cream_counter).click()
        self.driver.find_element(*self.ice_cream_counter).click()

    def click_for_taxi_modal(self):
        # Hace clic en el botón de pedir un taxi
        self.driver.find_element(*self.botton_go_taxi).click()

        # Espera implícita de 300 segundos
        driver.implicitly_wait(300)

        # Espera hasta que  finalice el cronograma
        WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located(self.window_popup_body_order))

        # Obtiene la confirma la solicitud del taxi
        popup_text = self.driver.find_element(*self.window_popup_go_taxi).text

        # Devuelve el popup que confirma la solicitud del taxi
        return popup_text

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # Configura el entorno de prueba, incluyendo las capacidades del navegador
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_complete_taxi_booking(self):
        # Prueba completa que simula el proceso de reserva de un taxi
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Establecer dirección
        routes_page.set_route(data.address_from, data.address_to)

        # Pedir taxi
        routes_page.click_book_a_taxi_button()

        # Seleccionar tarifa Comfort
        routes_page.select_comfort_fare()

        # Seleccionar número de teléfono
        routes_page.select_phone_number_field()

        # Ingresar número de teléfono
        routes_page.enter_phone_number(data.phone_number)

        # Recuperar e ingresar código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        routes_page.driver.find_element(By.ID, 'code').send_keys(confirmation_code)
        routes_page.driver.find_element(*routes_page.code_confirm_button).click()

        # Agregar tarjeta de crédito
        routes_page.add_payment_method(data.card_number, data.card_code)

        # Salir de la ventana emergente de método de pago
        routes_page.exit_payment_popup()

        # Enviar mensaje al conductor
        routes_page.message_to_driver("Hola, coloca musica")

        # Seleccionar requisitos del viaje
        routes_page.select_blanket_and_scarves()
        routes_page.select_two_ice_creams()

        # Seleccionar el botón para pedir un taxi
        routes_page.click_for_taxi_modal()

    @classmethod
    def teardown_class(cls):
        # Cierra el navegador y limpia los recursos
        cls.driver.quit()