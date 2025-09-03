# Image Folder

This folder contains generated images from the OpenAI DALL-E API.

## Image Categories

### Basic Generation
- `majestic_dragon.png` - A majestic dragon flying over a medieval castle at sunset

### Creative Examples
- `futuristic_city.png` - A futuristic cityscape with flying cars and neon lights
- `mountain_sunset.png` - A serene mountain landscape at sunset with a crystal clear lake
- `robot_cat.png` - A cute robot playing with a cat in a cozy living room
- `underwater_scene.png` - An underwater scene with colorful coral reefs and tropical fish

### Style Variations
- `garden_vivid.png` - A beautiful garden with flowers and butterflies (vivid style)
- `garden_natural.png` - A beautiful garden with flowers and butterflies (natural style)

### Size Variations
- `coffee_cup_1024_1024.png` - A minimalist coffee cup on a wooden table (1024x1024)
- `coffee_cup_1792_1024.png` - A minimalist coffee cup on a wooden table (1792x1024)
- `coffee_cup_1024_1792.png` - A minimalist coffee cup on a wooden table (1024x1792)

## Image Generation Features

### Available Models
- **DALL-E 3**: High-quality image generation with detailed prompts

### Available Sizes
- **1024x1024**: Square format (default)
- **1792x1024**: Landscape format
- **1024x1792**: Portrait format

### Available Styles
- **vivid**: More dramatic and vibrant colors
- **natural**: More realistic and natural appearance

### Available Qualities
- **standard**: Standard quality (faster generation)
- **hd**: High definition quality (slower generation)

## Usage

All images are automatically saved to this `img/` folder when running the `05_image_generation.py` script. The script includes:

1. **Basic image generation** with custom prompts
2. **Creative examples** showcasing different artistic styles
3. **Style variations** demonstrating vivid vs natural styles
4. **Size variations** showing different aspect ratios

## File Organization

Images are organized by:
- **Content type**: Basic, creative, style variations, size variations
- **Naming convention**: Descriptive names with relevant parameters
- **Format**: All images are saved as PNG files for high quality

## Running the Script

To generate all example images:

```bash
python 05_image_generation.py
```

This will create all the example images and save them in this folder with appropriate filenames.
