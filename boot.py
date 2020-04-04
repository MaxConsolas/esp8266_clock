from time import sleep_msfrom machine import I2C, Pin, freq, RTC, Timerfrom esp8266_i2c_lcd import I2cLcdfrom webrepl import startfrom gc import collect, enablefrom ntptime import timefrom utime import localtimefrom network import WLAN, STA_IFSSID = "WayFay" # Имя Wi-Fi сетиPASS = "23071976igor" # Пароль от Wi-Fi  сетиATTEMPTS_LIMIT = 75 # 5 = 1 second; default timeout 15sprint("\n------------------") # Для комфорта в консолиfreq(160000000) # Адский разгон до 160MHzenable()  # Активация сборщика мусора# Подключаем lcdi2c = I2C(scl=Pin(2), sda=Pin(0), freq=400000) # GPIO2 scl; GPIO0 sda;lcd = I2cLcd(i2c, 0x27, 2, 16) # Адрес I2C 0x27 или 39lcd.clear() # Вывод статуса на lcdlcd.putstr("Loading...")lcd.move_to(0, 1)lcd.putstr("Setup Wi-Fi")# Активация Wi-Fi модуляwifi = WLAN(STA_IF)wifi.active(True)wifi.connect(SSID, PASS)attempt=0while not wifi.isconnected():    if attempt>=ATTEMPTS_LIMIT:        break    sleep_ms(200)    attempt+=1start() # Запуск Web-REPL# Вывод информации о Wi-Fi сетиlcd.clear()if wifi.isconnected():    lcd.putstr("WiFi connected!")    lcd.move_to(0, 1)    lcd.putstr("IP:"+wifi.ifconfig()[0])else:    lcd.putstr("CONNECTION ERROR")    lcd.move_to(0, 1)    lcd.putstr("................")# Функция синхронизации времениdef parseTime():    try:        curtime = time()    except:        parseTime()    else:              if curtime is None:            parseTime()        curtime = curtime + 5*60*60        tm = localtime(curtime)        RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))        timePrint("Time sync complete!")    def timePrint(text):    print("["+str(RTC().datetime()[4])+":"+str(RTC().datetime()[5])+":"+str(RTC().datetime()[6])+"] "+text)parseTime()sleep_ms(200)