from io import BytesIO

from flask import g, request, Flask, current_app, jsonify, render_template, session
import jwt
from jwt import exceptions
import functools
import datetime
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='
headers = {'typ': 'jwt', 'alg': 'HS256'}

# 密钥
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


def create_validate_code(size=(120, 30),
                         chars=init_chars,
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(230, 230, 230),
                         fg_color=(18, 18, 18),
                         font_size=20,
                         font_type='./static/DejaVuSans-Bold.ttf',
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance=1):
    '''
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体的详细路径，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''

    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''绘制验证码字符'''
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3), strs, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100, float(random.randint(1, 2)) / 500, 0.001, float(random.randint(1, 2)) / 500]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return img, strs


def create_token(username, code):
    payload = {
        'username': username,
        'code': code,  # 自定义用户ID
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    return result



@app.route('/code')
def get_code():
    username = session['username']
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    base64_str = b64encode(buf_str)
    prefix = bytes('data:image/jpeg;base64,'.encode('utf-8'))
    response = app.make_response(prefix + base64_str)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Authorization'] = create_token(username, strs)
    session['img'] = strs.upper()
    return response


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get("username")
        password = data.get("password")
        session['username'] = username
        session['random'] = random.randint(0, 65536)
        session['score'] = 0
        return {"code": 200, "message": "success"}


@app.route('/pdd', methods=['GET', 'POST'])
def game():
    if 'username' not in session:
        return {"code": 200, "message": "Please Login First!"}
    if request.method == "POST":
        if session.get('img') == request.form.get('code').upper():
            session['score'] += 1
            return {"code": 200, "message": "you score is " + str(session['score'])}
        else:
            return {"code": 200, "message": "you wrong!"}
    score = session['score']
    if score >= 1000:
        return {"code": 200, "flag": "flag{you win!}"}

    return render_template("game.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
