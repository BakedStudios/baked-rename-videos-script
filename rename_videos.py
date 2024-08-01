import os
import subprocess
from PIL import Image

def extract_frame(video_path, output_image_path):
    subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'select=eq(n\,0)', '-q:v', '3', output_image_path])

def crop_image(input_image_path, output_image_path, crop_area):
    with Image.open(input_image_path) as img:
        cropped_img = img.crop(crop_area)
        cropped_img.save(output_image_path)

def extract_text_from_image(image_path):
    result = subprocess.run(['tesseract', image_path, 'stdout'], capture_output=True, text=True)
    return result.stdout.strip()

def rename_file(old_path, new_name):
    new_path = os.path.join(os.path.dirname(old_path), new_name + os.path.splitext(old_path)[1])
    os.rename(old_path, new_path)

def process_videos(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(directory, filename)
            frame_path = os.path.join(directory, f'frame_{filename}.png')
            cropped_frame_path = os.path.join(directory, f'cropped_frame_{filename}.png')
            
            extract_frame(video_path, frame_path)
            
            # Crop to the top left corner (adjust the values as needed)
            crop_area = (0, 0, 500, 100)  # (left, top, right, bottom)
            crop_image(frame_path, cropped_frame_path, crop_area)
            
            text = extract_text_from_image(cropped_frame_path)
            if text:
                rename_file(video_path, text)
            
            # Clean up temporary files
            os.remove(frame_path)
            os.remove(cropped_frame_path)

if __name__ == "__main__":
    video_directory = '/path/to/your/videos'  # Change this to your actual directory
    process_videos(video_directory)