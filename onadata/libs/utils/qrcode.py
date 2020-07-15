# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import

import io
from base64 import b64encode
from elaphe import barcode


def generate_qrcode(message, stream=None,
                    eclevel='M', margin=10,
                    data_mode='8bits', format='PNG', scale=2.5):
    """Generate a QRCode, settings options and output."""
    if stream is None:
        stream = io.BytesIO()

    img = barcode('qrcode', message,
                  options=dict(version=9, eclevel=eclevel),
                  margin=margin, data_mode=data_mode, scale=scale)

    img.save(stream, format)
    datauri = "data:image/png;base64,{}".format(
        b64encode(stream.getvalue()).decode())
    stream.close()

    return datauri
