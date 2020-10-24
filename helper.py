import copy

def findClosestFood(data):
  
  food = data['board']['food']
  head = data['you']['head']
  distance = 100
  closest = food[0]
  for i in food:
    temp = (abs(i['x'] - head['x']) + abs(i['y'] - head['y']))
    if(temp <= distance):
      distance = temp
      closest = i

  return closest

def impossibleMoves(data):

  surrounding = []
  cantMove = []
  for i in range(4):
      temp = copy.copy(data['you']['head'])
      if (i == 1):
          temp['y'] -= 1
          if (temp['y'] < 0):
              cantMove.append("up")
      elif (i == 2):
          temp['x'] += 1
          if (temp['x'] > 10):
              cantMove.append("right")
      elif (i == 3):
          temp['y'] += 1
          if (temp['y'] > 10):
              cantMove.append("down")
      else:
          temp['x'] -= 1
          if (temp['x'] < 0):
              cantMove.append("left")

      surrounding.append(temp)

  for snake in data['board']['snakes']:
      for i in range(4):
          if (surrounding[i] in snake['body']):
              if (i == 1):
                  if ("up" not in cantMove):
                      cantMove.append("up")
              elif (i == 2):
                  if ("right" not in cantMove):
                      cantMove.append("right")
              elif (i == 3):
                  if ("down" not in cantMove):
                      cantMove.append("down")
              else:
                  if ("left" not in cantMove):
                      cantMove.append("left")
  return cantMove


def nextMove(data, foodX, foodY):

  headX = data['you']['head']['x']
  headY = data['you']['head']['y']

  if (headX <= foodX and headY <= foodY):
    if (headX == foodX):
        move = "down"
    else:
        move = "right"
  elif (headX <= foodX and headY >= foodY):
    if (headX == foodX):
        move = "up"
    else:
        move = "right"
  elif (headX >= foodX and headY >= foodY):
    if (headX == foodX):
        move = "up"
    else:
        move = "left"
  else:
    if (headX == foodX):
        move = "down"
    else:
        move = "left"
  
  return move