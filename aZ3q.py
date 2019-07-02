import requests
import cv2 as cv
import os
import matplotlib.pyplot as plt
import numpy as np
import random

card_images = []
cards = []
players = []
marks = ['ハート', 'スペード', 'ダイヤ', 'クローバー']
display_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
numbers = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def load_image():
  global card_images
  image_name = 'cards.jpg'
  vsplit_number = 4
  hsplit_number = 13
  
  if not os.path.isfile(image_name):
    response = requests.get('http://3156.bz/techgym/cards.jpg', allow_redirects=False)
    with open(image_name, 'wb') as image:
      image.write(response.content)
   
  img = cv.imread('./cards.jpg')
  img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
 
  h, w = img.shape[:2]
  crop_img = img[:h // vsplit_number * vsplit_number, :w // hsplit_number * hsplit_number]
  
  card_images = []
  for h_image in np.vsplit(crop_img, vsplit_number):
    for v_image in np.hsplit(h_image, hsplit_number):
      card_images.append(v_image)
  card_images = np.array(card_images)

class Card:
  def __init__(self, mark, display_name, number, image):
    self.mark = mark
    self.display_name = display_name
    self.number = number
    self.image = image
    self.is_dealt = False

class Player:
  def __init__(self, name):
    self.name = name
    self.cards = []
    self.total_number = 0

class Human(Player):
  def __init__(self, name):
    super().__init__(name)

class Computer(Player):
  def __init__(self, name):
    super().__init__(name)

def create_cards():
  global cards
  for i, mark in enumerate(marks):
    for j, number in enumerate(numbers):
      cards.append( Card(mark, display_names[j], number, card_images[i*len(numbers)+j]) )

def show_cards(cards):
  for i, card in enumerate(cards):
    print(f"{card.mark}{card.display_name}")
    plt.subplot(1, 6, i + 1)
    plt.axis('off')
    plt.imshow(card.image)
  plt.show()

def deal_card(player):
  card_number = random.randint( 0, len(marks) * len(numbers) - 1 )
  while cards[card_number].is_dealt:
    card_number = random.randint( 0, len(marks) * len(numbers) - 1 )
  player.cards.append( cards[card_number] )
  player.total_number += cards[card_number].number
  cards[card_number].is_dealt = True

def win():
  print('勝ち')

def lose():
  print('負け')

def choice():
  message = 'スタンド[1] or ヒット[2]'
  choice_key = input(message)
  while not enable_choice(choice_key):
    choice_key = input(message)
  return int(choice_key)

def enable_choice(string):
  if string.isdigit():
    number = int(string)
    if number >= 1 and number <= 2:
      return True
    else:
      return False

def play_once():
  deal_card( players[0] )
  deal_card( players[1] )
  deal_card( players[0] )
  show_cards( players[0].cards )
  if is_blackjack():
    win()
  else:
    choice_key = choice()
    if choice_key == 1:
      stand()

def is_blackjack(): 
  if(players[0].total_number == 21):
    return True
  else:
    return False

def is_burst(): 
  if(players[0].total_number >= 22):
    return True
  else:
    return False

def stand():
  deal_card( players[0] )
  show_cards( players[0].cards )
  if is_blackjack():
    win()
  elif is_burst():
    lose()
  else:
    choice_key = choice()
    if choice_key == 1:
      stand()

def play():
  print('デバッグログ：play()')
  load_image()
  create_cards()
  players.append( Human('自分') )
  players.append( Computer('コンピューター') )

  play_once()

play()
