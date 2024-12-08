from machine import I2C, Pin, PWM
from time import sleep
from pico_i2c_lcd import I2cLcd
from dht import DHT22

# Configuración I2C y LCD
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Configuración DHT22
dht = DHT22(Pin(22))

# Configuración PWM
pwm_pin = PWM(Pin(0))  # Usa el pin GPIO 0
pwm_frequency = 10
pwm_pin.freq(pwm_frequency)

# Mapeo de duty cycles
duty_cycle_map = {
    1: 25,  # 1 corresponde a 25% de duty cycle
    2: 50,  # 2 corresponde a 50% de duty cycle
    3: 60   # 3 corresponde a 60% de duty cycle
}

# Función para enviar señal PWM
def send_pwm_signal(value):
    if value not in duty_cycle_map:
        print(f"Valor {value} no válido. Use 1, 2 o 3.")
        return

    duty_percent = duty_cycle_map[value]
    duty_cycle = int(65536 * (duty_percent / 100))
    pwm_pin.duty_u16(duty_cycle)
    print(f"Señal enviada con {duty_percent}% duty cycle para el valor {value}")
    
    sleep(1)
    pwm_pin.duty_u16(0)
    print("Señal detenida, esperando 1 segundo")

# Bucle principal
while True:
    # Leer datos del DHT22
    dht.measure()
    temp = dht.temperature()
    hum = dht.humidity()
    print(f"Temperature: {temp}°C   Humidity: {hum:.1f}%")

    # Mostrar datos en el LCD
    lcd.clear()
    lcd.putstr('Temp: ' + str(temp) + " C")
    lcd.move_to(0,1)
    lcd.putstr('Hum: ' + str(hum) + "%")
    
    # Enviar señales PWM (por ejemplo, valores 1, 2, 3)
    for value in [1, 2, 3]:
        send_pwm_signal(value)
        sleep(1)  # Esperar 1 segundo entre señales
    
    # Esperar antes de la siguiente lectura
    sleep(2)
