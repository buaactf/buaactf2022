from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def logic_encrypt(img,X0,u):
    x,y = img.size
    img = np.array(img).flatten()
    num = len(img)
    
    for i in range(100):
        X0 = u * X0 * (1-X0)
        
    E = np.zeros(num)
    E[0] = X0
    for i in range(0,num-1):
        E[i+1] = u * E[i] * (1-E[i])
    E = np.round(E*255).astype(np.uint8)

    img = np.bitwise_xor(E,img)
    img = img.reshape(x,y,-1)
    img = np.squeeze(img)
    img = Image.fromarray(img)
    
    return img

def img_hist(img):
    img = np.array(img)
    plt.hist(im.flatten(),bins = 256)

# 加密flag.jpg，设定参数
img = Image.open("flag.jpg")
X0 = 0.66
u = 3.97

img_en = logic_encrypt(img,X0,u)
img_en.save('secret.jpg')
img_en.show()


#解密secret.jpg，加解密过程相同，调用加密函数即可
img_en = Image.open("secret.jpg")
X0 = 0.66
u = 3.97

img_de = logic_encrypt(img_en,X0,u)
img_de.save('out.jpg')
img_de.show()

