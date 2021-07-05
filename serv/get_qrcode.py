import qrcode
from flask import Blueprint, request, send_file

from setting import RET

qr = Blueprint('qrcode', __name__)


@qr.route("/qrcode", methods=["GET"])
def get_qr():
    text = request.args.get("text")
    if text:
        img = qrcode.make(data=text)
        filename = 'qr_'+text + '.png'

        with open(filename, 'wb') as f:
            img.save(f)
        RET['code'] = 0
        RET['msg'] = "生成二维码"
        RET['data'] = img

    else:
        filename = 'qr_nowords.png'
        RET['code'] = -1
        RET['msg'] = "生成二维码"
        RET['data'] = text

    return send_file(filename)
