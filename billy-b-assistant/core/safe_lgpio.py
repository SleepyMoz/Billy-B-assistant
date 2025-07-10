import os
USE_REAL_GPIO = os.getenv("USE_REAL_GPIO", "0") == "1"

if USE_REAL_GPIO:
    import lgpio as _lgpio
else:
    class _MockLGPIO:
        def gpiochip_open(self, chip): return 0
        def gpio_claim_output(self, h, pin): pass
        def gpio_write(self, h, pin, value): pass
        def tx_pwm(self, h, pin, freq, duty): pass
        def gpio_read(self, h, pin): return 0
    _lgpio = _MockLGPIO()

gpiochip_open = _lgpio.gpiochip_open
gpio_claim_output = _lgpio.gpio_claim_output
gpio_write = _lgpio.gpio_write
tx_pwm = _lgpio.tx_pwm
gpio_read = _lgpio.gpio_read
