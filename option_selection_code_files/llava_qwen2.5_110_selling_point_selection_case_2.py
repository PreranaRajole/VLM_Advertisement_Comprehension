import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from PIL import Image
import os
import pandas as pd

# Set the device to GPU 1
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

# The prompt template for option selection
OPTION_SELECTION_PROMPT = """
This is the advertisement for {product_name} in the {category_name} category. Help me the right option of selling points.
What is a Selling Point? A selling point is any text that is highlighting product features, price advantages or quality assurances. It appeals to the customer's emotions, logic and persuades them to buy the product being advertised.

IMPORTANT: Selling points are extracted ONLY from advertisement text, separated with semicolons. No explanations, quotations marks, or repetitions. Addresses, phone numbers, emails, and terms/conditions are NOT selling points. 

Which of the following options contains the most accurate list of selling points for this product?

Option 1: {option_1}

Option 2: {option_2}

Option 3: {option_3}

Option 4: {option_4}

Option 5: {option_5}

Select ONLY ONE option by number. Your answer should be formatted as:
"Selected Option: [option number]"
"""

# Load the Excel file containing the product, category, and options
excel_file_path = '/home/prajole/inputs/file_b_case2.xlsx'  # Update with your actual file path
df = pd.read_excel(excel_file_path)

# Images path
images_folder = '/home/prajole/inputs/AD_IMAGES_110/'  # Update with your actual images folder

# Output folder path
output_folder = "/home/prajole/outputs_option_selection/qwen2.5_case_2"
os.makedirs(output_folder, exist_ok=True)

#Loading the model
model_name = "Qwen/Qwen2.5-VL-7B-Instruct"
model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", torch_dtype=torch.float16, low_cpu_mem_usage=True, device_map="cuda:1")
processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

# Move the model to GPU
model = model.to(device)

# Helper function to find a row in the dataframe based on filename without extension
def find_row_by_filename(filename_without_ext, dataframe):
    matching_rows = dataframe[dataframe['File Name'] == filename_without_ext]
    if len(matching_rows) == 0:
        print("No data")
        return None
    return matching_rows.iloc[0]

# Results tracking
results = []

try:
    # Iterate through the image folder
    for filename in os.listdir(images_folder):
        # Get file path and check if it's an image
        image_file_path = os.path.join(images_folder, filename)
            
        # Extract filename without extension
        file_name = os.path.splitext(filename)[0]
        
        # Find the corresponding row in the Excel file
        row = find_row_by_filename(file_name, df)
        if row is None:
            print(f"No matching data found for image: {filename}")
            continue
            
        # Open the image
        image = Image.open(image_file_path)
        
        # Get data from the row
        product_name = row['Product']
        category_name = row['Category']
        
        # Get the options
        option_1 = row['SP_1']
        option_2 = row['SP_2']
        option_3 = row['SP_3']
        option_4 = row['SP_4']
        option_5 = row['SP_5']
        
        # Format the prompt
        formatted_prompt = OPTION_SELECTION_PROMPT.format(
            product_name=product_name,
            category_name=category_name,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            option_5=option_5
        )
        
        # Create conversation for LLaVA-Next
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": formatted_prompt},
                    {"type": "image"},
                ],
            },
        ]

        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt")
        inputs = prompt.to("cuda:1", torch.float16)
            
        # Move inputs to GPU 1
        output  = model.generate(**inputs, max_new_tokens=5000)
        op_text = processor.decode(output[0], skip_special_tokens=True)
            
        # Save the output to a text file
        file_name = file_name + ".txt"
        with open(os.path.join(output_folder, file_name), 'a', encoding="utf-8") as f:
            f.write(op_text + "\n") 
        
        print(f"Processed: {file_name}")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    torch.cuda.empty_cache()
    print("GPU cache cleared.")