# diagonal-color-sampler

Calculates and displays the average color along an image's main diagonal.

This Python script processes a static image, computes the average BGR color of pixels lying on its main diagonal (top-left to bottom-right), and then overlays this numerical value and a filled color swatch onto the image. The final image with the overlays is saved to a file, suitable for headless server environments.

## How to Run

1.  **Clone the repository (or save the `main.py` and `requirements.txt` files):**
    ```bash
    git clone https://github.com/your-username/diagonal-color-sampler.git
    cd diagonal-color-sampler
    ```
    (Note: This is a placeholder; you would create your own repository.)

2.  **Install dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## Output

Upon successful execution, the script will generate an image file named `diagonal_average_color_output.png` in the same directory. This image will be the original synthetic image with the calculated average BGR value and a square filled with that average color overlaid in the top-left corner.