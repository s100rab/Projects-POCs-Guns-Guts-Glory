from fpdf import FPDF
from PIL import Image
import cv2
import os
from skimage.metrics import structural_similarity as ssim
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def extract_unique_frames(video_path, output_folder, similarity_threshold=0.95):
    """
    Extracts unique frames from a video file based on structural similarity.
    
    Parameters:
        video_path (str): Path to the video file.
        output_folder (str): Directory to save the extracted images.
        similarity_threshold (float): Threshold for similarity between frames (0-1).
        
    Returns:
        List of paths to the unique image frames.
    """
    video_capture = cv2.VideoCapture(video_path)
    success, frame = video_capture.read()
    count = 0
    unique_images = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    while success:
        frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
        
        if count > 0:
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            score, _ = ssim(prev_gray, curr_gray, full=True)
            
            if score >= similarity_threshold:
                logging.info(f"Duplicate frame {count} detected (similarity {score:.2f}). Skipping...")
                success, frame = video_capture.read()
                count += 1
                continue
        
        cv2.imwrite(frame_path, frame)
        unique_images.append(frame_path)
        logging.info(f"Unique frame {count} saved: {frame_path}")
        
        prev_frame = frame
        success, frame = video_capture.read()
        count += 1

    video_capture.release()
    return unique_images

def create_pdf_from_images(image_paths, pdf_path):
    """
    Create a PDF from a list of image paths in landscape mode.
    
    Parameters:
        image_paths (list of str): Paths to images to be added to the PDF.
        pdf_path (str): Path where the PDF should be saved.
    """
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    
    for image_path in image_paths:
        image = Image.open(image_path)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Get the size of A4 page in landscape in mm
        a4_width_mm = 297
        a4_height_mm = 210

        # Add image as a new page, scaled to fit A4 landscape
        pdf.add_page()
        pdf.image(image_path, x=0, y=0, w=a4_width_mm, h=a4_height_mm)
    
    pdf.output(pdf_path, "F")
    logging.info(f"PDF created successfully: {pdf_path}")

def main(video_path, output_folder, pdf_path):
    # Step 1: Extract unique frames from the video
    logging.info("Starting to extract unique frames from the video...")
    unique_image_paths = extract_unique_frames(video_path, output_folder)
    
    # Step 2: Create PDF from unique images
    logging.info("Creating PDF from unique images...")
    create_pdf_from_images(unique_image_paths, pdf_path)

    logging.info("Process completed successfully!")

# Set paths
video_path = "Z:\\IMPORTANT\\local H\\GENERAL STUDY\\ONLINE LEARNING MODULE\\HCL_CERTIFICATE_ONBOARD\\SNOWFLAKE TRAINING\\lms_notes\\video_to_pdf\\lms_snow_v4.mp4"
output_folder = "extracted_images_v4"
pdf_path = "output_lms_v4.pdf"

# Run the main function
main(video_path, output_folder, pdf_path)
