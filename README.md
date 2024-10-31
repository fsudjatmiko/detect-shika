# SHIKANOKONOKONOKONOKOKOSHITANTAN

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fsudjatmiko/detect-shika.git
    cd your-repo-name
    ```

2. Create a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Place your images in the `images/` directory.

2. Run the main script:
    ```sh
    python src/main.py
    ```

3. Follow the on-screen instructions to load and process images.

## Features

- **Load and Resize Images**: Load images from a specified path and resize them to the desired dimensions.
  ```python
  image, image_resized = load_and_resize_image(image_path, target_width, target_height)