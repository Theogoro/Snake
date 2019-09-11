#
# Creator       : Theogoro - Theo Berta              /    Creador           : Theogoro - Theo Berta
# GitHub profile: https://github.com/Theogoro       /     Perfil en GitHub  : https://github.com/Theogoro
# Contact email : theoberta@gmail.com              /      Email de contacto : theoberta@gmail.com
#
#

import threading
from pynput import keyboard
import pynput
import os, sys
import numpy
import time
import datetime
import random
import pyautogui
import json

play = True
head_orientation = 'd'
score = 0
display_time = 0.08
food = {'x':0,'y':0}
food_char = 'O '

colors = { #Este diccionario contiene todos los codigos anci de color
    'Dark Gray' : '1;30;40m',
    'Red'       : '1;31;40m',
    'Green'     : '1;32;40m',
    'Yellow'    : '1;33;40m',
    'Blue'      : '1;34;40m',
    'Magenta'   : '1;35;40m',
    'Cyan'      : '1;36;40m'
}

#  Orientacion:
#  X avanza en el eje x
# -X retrocede en el eje x
#  y avanza en el eje y
# -y retrocede en el eje y
#
# Y  A
#    |
#    |
#    |
#    |
#    |
#   -|----------------> 
#                     X

def clear_console():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def main():
    input_thread = threading.Thread(target=start_input,name='Keyboard input')
    input_thread.start()
    snake_thread = threading.Thread(target=start_snake,name='Snake')
    snake_thread.start()
    
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)
    
def start_snake():
    s = snake()

def start_input():
    key_input()

class snake:
    def __init__(self):
        self.body = [
            {'x':1,'y':1}
        ]
        self.name = input('Your Name: ')
        self.head_char = '\033[' + colors["Green"] + '@ \033[0m'
        self.char = '\033[' + colors["Green"] + '* \033[0m'
        self.length = 1
        self.table = self.init_table()
        self.spawn_food()
        global play
        while play:
            self.draw_table()

    def snake_move(self):
        self.body.insert(0,{'x':self.body[0]['x'],'y':self.body[0]['y']} )
        global head_orientation
        if head_orientation == 'd':
            self.body[0]['y']+=1
            if(self.body[0]['y'] == 11):
                self.body[0]['y']-=10
        elif head_orientation == 'a':
            self.body[0]['y']-=1
            if(self.body[0]['y'] == 0):
                self.body[0]['y']+=10
        elif head_orientation == 'w':
            self.body[0]['x']-=1
            if self.body[0]['x'] == 0:
                self.body[0]['x']+=10
        elif head_orientation == 's':
            self.body[0]['x']+=1
            if self.body[0]['x'] == 11:
                self.body[0]['x']-=10
        self.body.pop()
        self.draw_snake()

    def draw_snake(self):
        for part in self.body:
            self.table[part['x']][part['y']] = self.char
        self.table[self.body[0]['x']][self.body[0]['y']] = self.head_char

    def draw_table(self):
        clear_console()
        global score
        print('Score:' + str(score))
        str_table = ''
        for line in self.table:
            str_line = ''
            for char in line:
                str_line = str_line + char
            str_table = str_table + str_line + '\n'
        print(str_table)
        time.sleep(display_time)
        self.table = self.init_table()
        self.collisions()
        self.snake_move()
        self.draw_food()

    def spawn_food(self):
        no_spawn = [] # Esta lista va a guarda las posiciones donde la comida no puede aparecer.
        for part in self.body:
            no_spawn.append({'x':part['x'],'y':part['y']})
        coincidence = True
        while coincidence:
            food['x']=random.randint(1,10)
            food['y']=random.randint(1,10)
            coincidence = False
            for coor in no_spawn:
                if coor == food:
                    coincidence=True 
            #Revisa las coordenas donde esta la serpiente, si esa coincide con la que se genero 
            #aleatoriamente de la comida, se generará otras coordenadas para la comida y se repitira el proceso.

    def draw_food(self):
        self.table[food['x']][food['y']] = food_char

    def collisions(self): # Este metodo se encargará de todas las coliciones con la comida
        if self.body[0]['x'] == food['x'] and self.body[0]['y'] == food['y']:
            self.snake_grow()
            global score, display_time,color
            score+=1
            if score == 10:                  # Curva de dificultad
                display_time-= 0.02          
                self.head_char = '\033[' + colors['Blue'] + '@ \033[0m'
                self.char = '\033[' + colors['Blue'] + '* \033[0m'           
            if score == 50:                  
                display_time-= 0.03      
                self.head_char = '\033[' + colors['Cyan'] + '@ \033[0m'
                self.char = '\033[' + colors['Cyan'] + '* \033[0m'                     
            self.spawn_food()
        positions = []
        for part in self.body:
            positions.append(part)
        positions.pop(0)  # La cabeza no puede chocar con ella misma.
        coincidence = False
        for p in positions:
            if self.body[0] == p:
                coincidence = True
        if coincidence:
            pyautogui.press('esc')
            time.sleep(0.5)
            print('\033[' + colors['Red'] + 'You lose! \033[0m')
            time.sleep(1.5)
            self.save_score()
            self.see_scores()
            restart()

    def save_score(self):
        data = []
        with open('scores.json','r') as file:
            data = json.load(file)
        global score
        data.append({"name":self.name,"score":score})
        #str_data = str(data)

        with open('scores.json','w') as file:
            json_str = json.dumps(data)
            file.write(json_str)

    def see_scores(self):
        clear_console()
        data = []
        with open('scores.json','r') as file:
            data = json.load(file)
        print('Higher scores:')
        data = sorted(data, key = lambda i: i['score'])
        print('---> '+ data[0]['name'] +' --->  SCORE: ' + str(data[0]['score']))
        if len(data) > 2:
            print('---> '+ data[1]['name'] +'  SCORE: ' + str(data[1]['score']))
        if len(data) > 3:
            print('---> '+ data[2]['name'] +'  SCORE: ' + str(data[2]['score']))
        time.sleep(10)
    def snake_grow(self):
        self.body.append({'x':0,'y':0})

    def init_table(self): # Este metodo dibuja la tabla vacia.
        #
        # border_v = '║'
        # border_h = '═'
        # bxy    = '╗'
        # bx_y   = '╝'
        # b_xy   = '╔'
        # b_x_y  = '╚'
        #
        #border x   y  = ╗
        #border x  -y  = ╝
        #border -x  y  = ╔
        #border -x -y  = ╚
        #
        # retornamos un array de arrays
        return numpy.array([['╔','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','╗'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['║','x ','x ','x ','x ','x ','x ','x ','x ','x ','x ','║'],
                        ['╚','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','═','╝']])
        
class key_input:
    def __init__(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
    def on_press(self,key):
        pass

    def on_release(self,key):
        if key == pynput.keyboard.Key.up:        # Funcion de cada tecla:
            self.update_orientation('w')         # W = subir
        elif key == pynput.keyboard.Key.down:   
            self.update_orientation('s')         # S = bajar
        elif key == pynput.keyboard.Key.left:    
            self.update_orientation('a')         # A = retroceder
        elif key == pynput.keyboard.Key.right:     
            self.update_orientation('d')         # D = avanzar
        elif key == pynput.keyboard.Key.esc:
            global play
            play = False
            time.sleep(1)
            print(" ---> FINAL SCORE: " +str(score) + " <--- ")
            return False # <-- Esto termina la tarea
    
    def update_orientation(self,o): # este metodo actualiza la fecha y la hora
        global display_time,head_orientation
        head_orientation = o
        time.sleep(display_time)


if __name__ == "__main__":
    main()