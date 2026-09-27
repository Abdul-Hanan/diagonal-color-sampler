import cv2
import numpy as np
import os

def generate_test_image(width=400, height=300):
    """
    Generates a synthetic image with distinct color quadrants for testing.
    The main diagonal (top-left to bottom-right) will cross different colors.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Define some distinct BGR colors
    blue = [255, 0, 0]
    green = [0, 255, 0]
    red = [0, 0, 255]
    yellow = [0, 255, 255]

    # Fill quadrants with different colors
    img[0:height//2, 0:width//2] = blue       # Top-left (BGR: 255,0,0)
    img[0:height//2, width//2:width] = green   # Top-right (BGR: 0,255,0)
    img[height//2:height, 0:width//2] = red   # Bottom-left (BGR: 0,0,255)
    img[height//2:height, width//2:width] = yellow # Bottom-right (BGR: 0,255,255)

    # For a 400x300 image, the diagonal (min(h,w)=300 pixels long) will mostly pass through:
    # (0,0) to (149,149) which is blue
    # (150,150) to (299,299) which is yellow
    # So the expected average color will be a mix of blue and yellow, approximately gray.
    # Avg([255,0,0] + [0,255,255]) = [127.5, 127.5, 127.5]

    return img

def main():
    print("Starting diagonal color sampler...")

    # 1. Generate a test image
    image = generate_test_image(width=400, height=300)
    height, width = image.shape[:2]
    print(f"Generated image of size: {width}x{height}")

    # Make a copy for overlaying information
    output_image = image.copy()

    # 2. Extract pixels along the main diagonal (top-left to bottom-right)
    # The diagonal length is limited by the smaller dimension
    diagonal_length = min(height, width)
    diagonal_pixels = []

    for i in range(diagonal_length):
        diagonal_pixels.append(image[i, i])

    # Convert list of pixels to a NumPy array for easier calculation
    if not diagonal_pixels:
        print("Warning: No diagonal pixels found (image might be too small). Exiting.")
        return

    diagonal_pixels_np = np.array(diagonal_pixels)

    # 3. Calculate the average BGR color
    avg_bgr_float = np.mean(diagonal_pixels_np, axis=0)
    # Convert to integers for display, rounding is implicit with int conversion
    avg_bgr_int = tuple(map(int, avg_bgr_float)) # (B, G, R)

    print(f"Average BGR color along the main diagonal: {avg_bgr_int}")

    # 4. Overlay the numerical average BGR values and a color square

    # Define text properties
    text = f"Avg BGR: {avg_bgr_int}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    text_color = (255, 255, 255) # White text

    # Calculate text size to create a background rectangle
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_padding = 10 # Padding around the text
    
    # Position for the text block (top-left corner)
    text_block_start_x = 10
    text_block_start_y = 10
    
    # Calculate dimensions for the black background rectangle
    text_bg_end_x = text_block_start_x + text_w + 2 * text_padding
    text_bg_end_y = text_block_start_y + text_h + baseline + 2 * text_padding

    # Draw a filled black rectangle as background for the text for readability
    cv2.rectangle(output_image, 
                  (text_block_start_x, text_block_start_y), 
                  (text_bg_end_x, text_bg_end_y), 
                  (0, 0, 0), # Black color
                  -1) # Filled rectangle

    # Put the text on top of the black background
    text_pos_x = text_block_start_x + text_padding
    text_pos_y = text_block_start_y + text_h + text_padding # Y-coordinate is baseline of the first line
    cv2.putText(output_image, text, (text_pos_x, text_pos_y), 
                font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    # Overlay the small square filled with the average color
    square_size = 50
    square_margin_top = 20 # Margin between text block and color square

    # Position the square below the text block, aligned with its left edge
    square_pos_x = text_block_start_x
    square_pos_y = text_bg_end_y + square_margin_top

    # Draw the filled square with the average BGR color
    cv2.rectangle(output_image, 
                  (square_pos_x, square_pos_y), 
                  (square_pos_x + square_size, square_pos_y + square_size), 
                  avg_bgr_int, # The calculated average BGR color
                  -1) # Filled rectangle
    
    # Add a thin black border to the square for better definition
    cv2.rectangle(output_image, 
                  (square_pos_x, square_pos_y), 
                  (square_pos_x + square_size, square_pos_y + square_size), 
                  (0, 0, 0), # Black border
                  1) # 1-pixel thickness

    # 5. Save the output image to a file
    output_filename = "diagonal_average_color_output.png"
    cv2.imwrite(output_filename, output_image)
    print(f"Output image saved as '{output_filename}'")
    print("Script finished successfully.")

if __name__ == "__main__":
    main()