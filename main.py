#Main runtime for simulation including pygame and pygame GUI

import pygame


# Define the background colour
# using RGB color coding.
background_colour = (234, 212, 252)
  
# Define the dimensions of
# screen object(width,height)
width, height = (720, 720)
screen = pygame.display.set_mode((width, height))
  
# Set the caption of the screen
pygame.display.set_caption('Boid simulation')
  
# Fill the background colour to the screen
screen.fill(background_colour)
  
# Update the display using flip
pygame.display.flip()
  
# Variable to keep our game loop running
running = True
  
# game loop
while running:
    
# for loop through the event queue  
    for event in pygame.event.get():
      
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
            
            
            
# Boid parameters (Tuna)
N_boids = 50 # number of boids 
r_CA = 5 # radius of cohesion and alignment
r_S = 5 # radius of separation
r_F = 5 # radius of food
v_boid = 2 # velocity
L = 100 # length of the simulation area

# predator parameters (Tiger shark)
N_predators = 1 # number of predators
r_B = 10 # radius of boid sensing
r_S = 2 # radius of separation
v_predator = 2 # velocity
