import random
import os
import torch
import pandas as pd
import csv
from tqdm import tqdm
from diffusers import HunyuanDiTPipeline

# Define all placeholder options by category
SPACES = {
    "Electronics": ["Modern home office", "Minimalist studio", "Professional workspace", "Tech showroom"],
    "Services": ["Professional workspace", "Urban cafe", "Corporate office", "Client meeting space"],
    "Travel & Tourism": ["Coastal beach scene", "Mountain landscape", "Historic cityscape", "Luxury resort"],
    "Home Appliances": ["Luxury apartment", "Modern home"],
    "Food and Beverages": ["Urban cafe", "Minimalist studio", "Gourmet kitchen", "Outdoor dining setting"],
    "Self Care And Wellness": ["Stylish bathroom", "Natural outdoor setting", "Spa environment", "Peaceful retreat"],
    "Automobiles": ["Urban street", "Natural outdoor setting", "Mountain road", "Sleek showroom"],
    "Finance": ["Financial marketplace", "Banking environment", "Money Management Space"],
    "Clothes": ["Minimalist studio", "High-end retail space", "Urban street", "Fashion runway"],
    "Accessories": ["Minimalist studio", "High-end retail space", "Fashion editorial setting"],
    "Home Essentials": ["Luxury apartment", "Designer living space", "Contemporary home"]
}

VIBE_AESTHETICS = {
    "Electronics": ["Bold futuristic", "Clean editorial", "Sleek minimalist", "High-tech modern"],
    "Services": ["Professional corporate", "Vibrant contemporary", "Trusted expert", "Approachable business"],
    "Travel & Tourism": ["Peaceful natural", "Vibrant contemporary", "Adventurous explorer", "Luxurious escape"],
    "Home Appliances": ["Elegant minimalist", "Calm Scandinavian", "Modern domestic", "Sleek contemporary"],
    "Food and Beverages": ["Warm rustic", "Clean editorial", "Indulgent gourmet", "Vibrant fresh"],
    "Self Care And Wellness": ["Calm Scandinavian", "Peaceful natural", "Serene minimalist", "Rejuvenating spa"],
    "Automobiles": ["Bold futuristic", "Luxurious modern", "Dynamic performance", "Elegant precision"],
    "Finance": ["Professional corporate", "Elegant minimalist", "Trusted authority", "Secure modern"],
    "Clothes": ["Clean editorial", "Energetic urban", "Luxurious fashion", "Trendy contemporary"],
    "Accessories": ["Elegant minimalist", "Luxurious modern", "Fashion forward", "Timeless classic"],
    "Home Essentials": ["Calm Scandinavian", "Warm rustic", "Cozy contemporary", "Elegant comfort"]
}

LIGHTING = {
    "Electronics": ["Crisp product lighting", "Cool blue hour ambiance", "High-tech LED accents", "Clean studio setup"],
    "Services": ["Soft natural daylight", "Ambient environmental light", "Warm inviting glow", "Professional diffused"],
    "Travel & Tourism": ["Warm golden hour glow", "Cinematic lighting setup", "Natural sunlight", "Dramatic sunset"],
    "Home Appliances": ["Diffused window light", "Bright high-key lighting", "Soft domestic ambiance", "Clean product spotlight"],
    "Food and Beverages": ["Soft natural daylight", "Dramatic studio lighting", "Warm ambient glow", "Rich contrasting shadows"],
    "Self Care And Wellness": ["Soft natural daylight", "Diffused window light", "Gentle ambient glow", "Calming low contrast"],
    "Automobiles": ["Dramatic studio lighting", "Cool blue hour ambiance", "Dynamic spotlights", "Moody contrast"],
    "Finance": ["Diffused window light", "Ambient environmental light", "Professional office lighting", "Soft business setting"],
    "Clothes": ["High-contrast directional", "Atmospheric backlight", "Fashion editorial lighting", "Dramatic shadows"],
    "Accessories": ["Crisp product lighting", "Dramatic studio lighting", "Jewelry showcase lighting", "Soft diffused glow"],
    "Home Essentials": ["Soft natural daylight", "Diffused window light", "Warm home ambiance", "Cozy evening glow"]
}

CAMERA_ANGLES = {
    "Electronics": ["Close-up detail shot", "Three-quarter view", "Hero product angle"],
    "Services": ["Lifestyle wide angle", "Eye-level perspective", "Service in action"],
    "Travel & Tourism": ["Wide angle perspective", "Immersive POV", "Aerial overview"],
    "Home Appliances": ["Overhead flat lay", "Straight-on product shot", "In-context usage angle"],
    "Food and Beverages": ["Overhead flat lay", "Close-up detail shot", "45-degree hero angle", "In-scene lifestyle view"],
    "Self Care And Wellness": ["Close-up detail shot", "Shallow depth of field focus", "Lifestyle usage angle", "Serene wide shot"],
    "Automobiles": ["Dramatic low angle", "Three-quarter view", "Dynamic motion shot", "Hero front angle"],
    "Finance": ["Lifestyle wide angle", "Eye-level perspective", "Professional interaction", "Symbolic composition"],
    "Clothes": ["Three-quarter view", "Dynamic action angle", "Fashion editorial pose", "Lifestyle context view"],
    "Accessories": ["Close-up detail shot", "Overhead flat lay", "Wrist/body placement shot", "Feature highlight angle"],
    "Home Essentials": ["Lifestyle wide angle", "Overhead flat lay", "In-context usage view", "Feature demonstration angle"]
}

# Configuration - Update these paths
excel_file_path = '/home/prajole/inputs/selling_points_category_350.xlsx'  # Update with your actual file path
output_dir = '/home/prajole/outputs_generated_images/hunyuandit/350_generated_hunyuandit'  # Update with your output directory
csv_log_path = os.path.join(output_dir, '/home/prajole/outputs_generated_images/hunyuandit/350_generated_hunyuandit/image_details.csv')  # Path for the CSV log file

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the product list
df = pd.read_excel(excel_file_path)

# Check if required columns exist
required_columns = ['File Name', 'Category', 'Product', 'Selling Points']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns in Excel file: {missing_columns}")

# Initialize the model
print("Loading hunyuandit model...")
model_name = "hunyuandit"

pipeline = HunyuanDiTPipeline.from_pretrained("Tencent-Hunyuan/HunyuanDiT-Diffusers", torch_dtype=torch.float16).to("cuda:1")
pipeline.transformer.to(memory_format=torch.channels_last)
pipeline.vae.to(memory_format=torch.channels_last)
pipeline.transformer = torch.compile(pipeline.transformer, mode="max-autotune", fullgraph=True)
pipeline.vae.decode = torch.compile(pipeline.vae.decode, mode="max-autotune", fullgraph=True)


def generate_prompt(row, selected_elements):
    """Generate an advertisement prompt based on product data and store selected elements"""
    product_name = row['Product']
    category_name = row['Category']
    selling_points = row['Selling Points']
    
    # Check if category exists in our templates
    if category_name not in SPACES:
        print(f"Warning: Category '{category_name}' not found in templates. Using Electronics as default.")
        category_name = "Electronics"
    
    # Select random elements from each template category and store them
    space = random.choice(SPACES[category_name])
    vibe = random.choice(VIBE_AESTHETICS[category_name])
    lighting = random.choice(LIGHTING[category_name])
    camera_angle = random.choice(CAMERA_ANGLES[category_name])
    
    # Store selected elements for CSV
    selected_elements['space'] = space
    selected_elements['vibe'] = vibe
    selected_elements['lighting'] = lighting
    selected_elements['camera_angle'] = camera_angle
    
    # Build the prompt
    prompt = f"Generate an advertisement poster for {product_name} in the {category_name} category, "
    prompt += f"showcased in a {space} environment with a {vibe} aesthetic. "
    # Add category-specific instructions
    if category_name == "Finance" and product_name == "bank services":
        prompt += f"Include an ATM machine or piggy banks or Credit/Debit Cards."
    elif category_name == "Automobiles":
        prompt += f"Ensure the car body, wheels, and windows are properly formed and anatomically correct. "
    elif category_name == "Electronics":
        # Check for screen-based devices
        if any(device in product_name.lower() for device in ["laptop", "television", "mobile"]):
            prompt += f"The screen should show a clean, appropriate interface or image. "
    elif category_name == "Services":
        prompt += f"Make the service offering the central focus of the advertisement. "
    elif category_name == "Travel & Tourism":
        # Check for airplane-related products
        if any(term in product_name.lower() for term in ["airline"]):
            prompt += f"Show the airplane with correct proportions and realistic appearance with properly shaped wings, fuselage, and tail. "
    prompt += f"The selling points are: {selling_points}. "
    prompt += f"The product is captured with {camera_angle} perspective and {lighting}. "
    print(prompt)
    
    return prompt

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(csv_log_path):
    with open(csv_log_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['file_name', 'space', 'vibe', 'lighting', 'camera_angle'])
    print(f"Created tracking CSV file at: {csv_log_path}")
else:
    print(f"Using existing tracking CSV file at: {csv_log_path}")

# Load existing entries from CSV to avoid duplicates
existing_files = set()
if os.path.exists(csv_log_path):
    with open(csv_log_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Skip header
        for row in csv_reader:
            if row:  # Make sure the row is not empty
                existing_files.add(row[0])
    print(f"Found {len(existing_files)} existing entries in CSV log.")

# Process each product and generate images
print(f"Starting image generation for {len(df)} products...")

try:
    # Use tqdm for progress bar
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Generating Images"):
        file_name = row['File Name']
        output_file = f"{file_name}_{model_name}.png"
        output_path = os.path.join(output_dir, output_file)
        
        # Dictionary to store selected elements for CSV
        selected_elements = {}
        
        # Generate prompt and store selected elements
        prompt_text = generate_prompt(row, selected_elements)
        
        # Print prompt for reference
        print(f"\nGenerating: {output_file}")
        
        # Generate the image
        image = pipeline(prompt=prompt_text).images[0]
        
        # Save the image
        image.save(output_path)
        
        # Log details to CSV
        with open(csv_log_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                output_file,
                selected_elements.get('space', ''),
                selected_elements.get('vibe', ''),
                selected_elements.get('lighting', ''),
                selected_elements.get('camera_angle', '')
            ])
            
        # Add to existing files set
        existing_files.add(output_file)

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Clean up
    torch.cuda.empty_cache()
    print("GPU cache cleared.")
    print(f"Completed {len(existing_files)} out of {len(df)} images.")
    print(f"Output directory: {output_dir}")
    print(f"Image details logged to: {csv_log_path}")