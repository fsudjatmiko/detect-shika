import cv2
import numpy as np
import pygame
import os

# Function to load and resize images
def load_and_resize_image(image_path, target_width, target_height):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (target_width, target_height))
    return image, image_resized

# Function to perform color detection
def perform_color_detection(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    shirt_lower = np.array([0, 0, 200])  # White color range
    shirt_upper = np.array([180, 50, 255])

    bottom_lower = np.array([100, 150, 0])  # Blue color range
    bottom_upper = np.array([140, 255, 255])

    skin_lower = np.array([0, 30, 60])  # Adjusted skin color range
    skin_upper = np.array([20, 150, 255])

    background_lower = np.array([0, 50, 50])  # Red color range
    background_upper = np.array([10, 255, 255])

    shirt_mask = cv2.inRange(hsv_image, shirt_lower, shirt_upper)
    bottom_mask = cv2.inRange(hsv_image, bottom_lower, bottom_upper)
    skin_mask = cv2.inRange(hsv_image, skin_lower, skin_upper)
    background_mask = cv2.inRange(hsv_image, background_lower, background_upper)

    background_mask = cv2.bitwise_and(background_mask, cv2.bitwise_not(skin_mask))

    black_background = np.zeros_like(image)

    red_shirt = cv2.bitwise_and(black_background, black_background, mask=shirt_mask)
    red_shirt[:, :, 2] = cv2.bitwise_or(red_shirt[:, :, 2], shirt_mask)

    blue_bottom = cv2.bitwise_and(black_background, black_background, mask=bottom_mask)
    blue_bottom[:, :, 0] = cv2.bitwise_or(blue_bottom[:, :, 0], bottom_mask)

    green_skin = cv2.bitwise_and(black_background, black_background, mask=skin_mask)
    green_skin[:, :, 1] = cv2.bitwise_or(green_skin[:, :, 1], skin_mask)

    final_image = cv2.addWeighted(red_shirt, 1, blue_bottom, 1, 0)
    final_image = cv2.addWeighted(final_image, 1, green_skin, 1, 0)

    final_image[background_mask > 0] = [0, 0, 0]

    final_image_rgb = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
    return final_image_rgb

# Function to display the main menu
def display_main_menu(screen, thumbnails):
    screen.fill((255, 255, 255))
    for i, (image_file, thumbnail) in enumerate(thumbnails):
        screen.blit(thumbnail, (i * 150, 50))
    pygame.display.flip()

# Function to display the images side by side
def display_images(screen, original_surface, processed_surface, image_width, retry_button):
    screen.fill((255, 255, 255))
    screen.blit(original_surface, (0, 0))
    screen.blit(processed_surface, (image_width, 0))
    screen.blit(retry_button, (screen.get_width() // 2 - retry_button.get_width() // 2, screen.get_height() - retry_button.get_height() - 10))
    pygame.display.flip()

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Image Selection')

# Load images from the images folder
images_folder = './images'
image_files = [f for f in os.listdir(images_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
thumbnails = []
for image_file in image_files:
    image_path = os.path.join(images_folder, image_file)
    _, image_resized = load_and_resize_image(image_path, 120, 120)
    thumbnails.append((image_file, pygame.surfarray.make_surface(image_resized)))

# Main loop
running = True
while running:
    # Main loop for image selection
    selected_image = None
    while selected_image is None and running:
        display_main_menu(screen, thumbnails)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, (image_file, thumbnail) in enumerate(thumbnails):
                    thumbnail_rect = thumbnail.get_rect(topleft=(i * 150, 50))
                    if thumbnail_rect.collidepoint(x, y):
                        selected_image = image_file

    if selected_image:
        # Load the selected image
        image_path = os.path.join(images_folder, selected_image)
        target_width = screen_width // 2
        target_height = screen_height  # Leave space for the retry button
        image, image_resized = load_and_resize_image(image_path, target_width, target_height)
        final_image_rgb = perform_color_detection(image)
        final_image_resized = cv2.resize(final_image_rgb, (target_width, target_height))

        # Set up the display for showing the original and processed images
        window_width = target_width * 2
        window_height = target_height + 50  # Include space for the retry button
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('Original and Processed Images')

        # Convert the images to Pygame surfaces
        original_surface = pygame.surfarray.make_surface(image_resized)
        processed_surface = pygame.surfarray.make_surface(final_image_resized)

        # Create the retry button
        font = pygame.font.Font(None, 36)
        retry_button = font.render('Retry', True, (255, 255, 255), (0, 0, 0))
        retry_button_rect = retry_button.get_rect(center=(window_width // 2, window_height - 25))

        # Main loop for displaying the images
        displaying_images = True
        while displaying_images:
            display_images(window, original_surface, processed_surface, target_width, retry_button)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    displaying_images = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button_rect.collidepoint(event.pos):
                        displaying_images = False

# Quit Pygame
pygame.quit()
