import random
MAX_LEVEL = 128
fl4gs = ['hahahahahahahahahahahahahh',
         '8D:BD:A6:77:7D:4E',
         '', 
         'flag{wh1ch_WORD_do_you_ch00se_fir5t_mostly?}']
temp = [int(i,16) for i in fl4gs[1].split(':')]
mac = int(''.join([bin(i).replace('0b','').zfill(8) for i in temp]), 2)
random.seed(mac) 
temp = list(fl4gs[3])
random.shuffle(temp)
fl4gs[2] = ''.join(temp)
def award(mode, level):
    fl4g = fl4gs[mode]
    leak = level * len(fl4g) // MAX_LEVEL
    return fl4g[:leak] + '*' * (len(fl4g) - leak)
