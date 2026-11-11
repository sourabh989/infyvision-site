"""Current centre address. Change this file if the institute moves.

Visible uses of ADDRESS are limited to the contact page, footer and
Organization schema PostalAddress (plus the map query and the FAQ
'Where is Infinity Vision?' answer). Marketing copy should stay generic.
"""
from urllib.parse import quote

ADDRESS = 'E-2, 359 Arera Colony Bhopal'
ADDRESS_STREET = 'E-2, 359 Arera Colony'
ADDRESS_LOCALITY = 'Bhopal'
ADDRESS_REGION = 'Madhya Pradesh'
ADDRESS_COUNTRY = 'IN'
MAP_Q = f'{ADDRESS_STREET}, {ADDRESS_LOCALITY}, {ADDRESS_REGION}'
MAP_EMBED = 'https://www.google.com/maps?q=' + quote(MAP_Q) + '&output=embed'
MAP_LINK = 'https://www.google.com/maps/search/?api=1&query=' + quote(MAP_Q)
