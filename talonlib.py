from hashlib import sha512 # больше бит - сложнее взломать
from datetime import datetime
from psutil import cpu_count, cpu_freq, virtual_memory
from uuid import getnode
from time import time


class info:
  LICENSE = 'GNU GPL v3'
  VERSION = '1.3.1.beta' # где доплата 2 млрд по статье "непредвиденных расходов"? обновление - это непредвиденный расход! я хотел забить болт на первой версии!

class base32: # как указано в ТЗ, с использованием ООП-кода и импортозамещением в целях повышения безопасности (моя первая кастомная кодировка, работает идеально)
  
  @staticmethod 
  def encode( # кастомный отечественный base32, ожидаем 5 млрд рублей финансирования, в противном случае - иск
      binary: str,
      alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
      force_len = 0, # принудительное расширение вывода до указанного числа букв (обрезаться вывод не будет!), 0 для отключения
      separator = ' ', # кастомный разделитель
      block_size = 4 # размер блока данных, в символах (0 для отключения разделения)
      ):

    if len(alphabet) != 32: raise ValueError('Alphabet must be 32 symbols length')
    result = ''
    if len(binary) % 5:
      binary = '0' * (5 - (len(binary) % 5)) + binary
    for i in range(0, len(binary), 5): # ПОЖАЛУЙСТА, НЕ ТРОГАЙТЕ ТУТ НИЧЕГО! ОНО РАБОТАЕТ И СЛАВА БОГУ! ВЫ ЭТО УЖЕ НИКОГДА НЕ ПОЧИНИТЕ БЕЗ БЕКАПА!!
      result += alphabet[int(binary[i:i+5],base=2)] # лучше ничего не трогайте во всей это функции
    if force_len: result = f'{result:А>{force_len}}'
    if block_size:
      for i in range(block_size, int(len(result) * (1 + 1 / block_size)), block_size + 1):
        result = result[:i] + separator + result[i:]
    return result

  @staticmethod
  def decode( # деплой после 1 млрд допфинансирования, изначально не входило в смету, а деньги уже распилены (пропиты)
    encoded,
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
    force_len = 0 # принудительное расширение вывода до указанного числа бит (обрезаться вывод не будет!), 0 для отключения
    ):

    if len(alphabet) != 32: raise ValueError('Alphabet must be 32 symbols length')
    result = ''
    for i in encoded.upper():
      if i in alphabet:
        result += f'{bin(alphabet.index(i))[2:]:0>5}' # сам не понял, как работает, не трогайте эту строку
    if force_len: result = f'{result:0>{force_len}}'
    return result

class security:

  @staticmethod
  def hwid( # получаем идентификатор на основе данных о железе
    hardware_list = (
      'MAC',
      'CPU_CORES',
      'CPU_MAX_FREQ',
      'CPU_MIN_FREQ',
      'RAM'
      ),
    separator = ''
    ):
    
    methods = { # перечень доступных методов
      'MAC' : getnode(),
      'CPU_CORES': cpu_count(),
      'CPU_MAX_FREQ': cpu_freq().max,
      'CPU_MIN_FREQ': cpu_freq().min,
      'RAM': virtual_memory().total
      }
    hardware = ''
    for item in hardware_list:
        hardware += str(methods[item]) + separator
    if separator: return sha512(hardware[:-1].encode('utf8')).hexdigest().upper()
    return sha512(hardware.encode('utf8')).hexdigest().upper()

  @staticmethod
  def generate( # генерируем талончик
    text,
    use_hwid = True,
    use_date = True,
    rounds = 8,
    return_all_rounds = True
    ):
    data = text
    if use_date: data = f'[{datetime.now().date()}] {data}'
    if use_hwid: data = f'[{security.hwid()}] {data}'
    result = ''
    for i in range(rounds):
      data = sha512(data.encode('utf8')).hexdigest()
      if return_all_rounds: result += base32.encode(bin(int(data, base=16))[2:]) + '\n'
    if not return_all_rounds: return base32.encode(bin(int(data, base=16))[2:])
    return result[:-1]

'''
либка написана Morozoff_
тг @mrzff1
этот комментарий можно убрать, если код не будет лежать на гитхабе
а если он не будет лежать на гитхабе, это нарушение лицензии (см. строку 9)
'''
