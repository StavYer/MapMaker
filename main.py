import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
pygame.init()  # Initialize pygame

# Create a resizable window of size 1920 x 1080, with faster rendering on screen
window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)

# Set size of game scene to be that of our image
image = pygame.image.load("image.png")
renderWidth , renderHeight = image.get_size()

running = True

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # First, if user wants to quit
            running = False
            break
        elif event.type == pygame.KEYDOWN: # Else, if user pressed keyboard
            # User wants to quit game
            if event.key == pygame.K_ESCAPE:
                running = False
                break
    # Rendering
    # Render our scene in a surface of the size we chose previously
    renderSurface = Surface((renderWidth, renderHeight))
    renderSurface.blit(image, (0, 0))

    # Scale rendering when resizing window
    windowWidth, windowHeight = window.get_size()
    renderRatio = renderWidth / renderHeight # Compute aspect ratios of window and scene surfaces
    windowRatio = windowWidth / windowHeight

    if windowRatio <= renderRatio: # We can use full window width but not height
        rescaledSurfaceWidth, rescaledSurfaceHeight = windowWidth, (windowWidth // renderRatio)
        rescaledSurfaceX = 0  # Compute coordinates of rescaled surface
        rescaledSurfaceY = (windowHeight - rescaledSurfaceHeight) // 2
    else: # We can use full window height but not width
        rescaledSurfaceWidth, rescaledSurfaceHeight = int (windowHeight * renderRatio), windowHeight
        rescaledSurfaceX = (windowWidth - rescaledSurfaceWidth) // 2 # Compute coordinates again
        rescaledSurfaceY = 0

    # Scale the rendering to the window/screen size
    rescaledSurface = pygame.transform.scale(renderSurface, (rescaledSurfaceWidth, rescaledSurfaceHeight))
    window.blit(rescaledSurface, (rescaledSurfaceX, rescaledSurfaceY))
    pygame.display.update()

pygame.quit()