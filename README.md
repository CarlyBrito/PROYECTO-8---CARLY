# Automatización de Pruebas de la Aplicación Web

# Introducción a la Automatización de Pruebas

# Descripción del Proyecto
# Este proyecto se centra en la automatización de pruebas para una aplicación web de rutas urbanas utilizando Selenium y Python.
# Su objetivo es validar el flujo completo de reserva de un taxi, desde la selección de la ruta hasta la confirmación de la reserva.

# Instalación
# Para instalar y configurar el proyecto, sigue estos pasos:

# 1. Instala Python 3.12 desde python.org.

# 2. Instala las dependencias necesarias:
# ```bash
# pip install selenium pytest
# ```

# 3. Configura el controlador del navegador:
# - Descarga el ChromeDriver (o el controlador correspondiente para tu navegador).
# - Asegúrate de que el controlador esté en tu PATH o especifica su ubicación en el código.

# 4. Ejecuta las pruebas con el siguiente comando en la terminal:
# ```bash
# pytest test_main.py
# ```

# Uso
# El proyecto incluye varias funciones y pruebas para validar la funcionalidad de la aplicación.
# Aquí hay un resumen de las funciones principales y cómo se utilizan:

# Funciones en UrbanRoutesPage
# - `set_from(from_address)`: Establece la dirección de 'Desde' en el campo correspondiente.
# - `set_to(to_address)`: Establece la dirección de 'Hasta' en el campo correspondiente.
# - `get_from()`: Obtiene el valor actual del campo 'Desde'.
# - `set_route(from_address, to_address)`: Configura la ruta ingresando las direcciones de 'Desde' y 'Hasta'.
# - `click_book_a_taxi_button()`: Hace clic en el botón 'Pedir un taxi'.
# - `select_comfort_fare()`: Selecciona la tarifa 'Comfort'.
# - `select_phone_number_field()`: Selecciona el campo de entrada de número de teléfono en la ventana emergente.
# - `enter_phone_number(phone_number)`: Ingresa el número de teléfono en la ventana emergente.
# - `add_payment_method(card_number, card_code)`: Agrega un método de pago ingresando los detalles de la tarjeta.
# - `exit_payment_popup()`: Cierra la ventana emergente del método de pago.
# - `message_to_driver(message)`: Envía un mensaje al conductor.
# - `select_blanket_and_scarves()`: Selecciona una manta y pañuelos.
# - `select_two_ice_creams()`: Selecciona dos helados.
# - `click_for_taxi_modal()`: Hace clic en el botón para pedir un taxi y obtiene el texto del popup de confirmación.

# Pruebas
# - `test_complete_taxi_booking()`: Simula el proceso completo de reserva de un taxi, incluyendo la configuración de la ruta, selección de la tarifa, ingreso del número de teléfono y código de confirmación, adición de tarjeta de crédito, y selección de requisitos adicionales.

# Contribución
# Actualmente, el proyecto podría beneficiarse de:
# - Corrección de errores: Revisa y soluciona cualquier error conocido en el proyecto.
# - Mejora de pruebas: Añade nuevas pruebas para cubrir casos adicionales o mejorar la cobertura de pruebas existente.
# - Documentación: Mejora la documentación para mayor claridad y comprensión.

# Para contribuir, realiza un fork del repositorio y envía un pull request con tus mejoras.

# Licencia
# Este proyecto está bajo la licencia TripleTen.

# Autores
# Carly Brito
