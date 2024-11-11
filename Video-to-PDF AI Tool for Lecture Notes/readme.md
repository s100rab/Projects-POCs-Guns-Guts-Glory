# 🎬 Video-to-PDF AI Tool for Lecture Notes 📄

Transform video lectures into a clean, readable PDF format by automatically extracting unique slides! This Python-based tool leverages computer vision to identify unique frames, helping students and professionals organize video content into easy-to-review PDF notes.

![Process GIF](link-to-your-gif.gif) *(Add a GIF here if you have one)*

---

## 🚀 Project Overview

### 🔍 Problem Statement
When studying from video lectures, accessing specific slides or notes for later review is often a hassle. Manually capturing and organizing lecture slides from videos can be time-consuming and repetitive.

### 🎯 Objective
To create a tool that:
- Extracts **unique frames** (slides) from video lectures by removing duplicates.
- Compiles these unique slides into a **PDF document** for easy offline access and study.

---

## 💡 Features
- **Automatic Slide Extraction**: Uses **Structural Similarity Index (SSIM)** to identify and save only unique frames, eliminating repetitive frames.
- **PDF Compilation**: Generates a **landscape-oriented PDF** with slides perfectly scaled to fit, ensuring readability.
- **High Efficiency**: Reduces clutter and storage usage by discarding duplicate frames.
- **Logging**: Provides real-time progress updates during frame extraction and PDF creation.

---

## 🛠️ Tech Stack
- **Python**: Core programming language
- **OpenCV**: For video frame extraction and processing
- **scikit-image**: To calculate similarity between frames
- **FPDF**: For creating a PDF document from extracted images
- **Pillow (PIL)**: To handle image conversions

---

## 📋 Project Workflow

1. **Frame Extraction**:
   - The video is read frame-by-frame using OpenCV.
   - Structural similarity (SSIM) is calculated between consecutive frames to detect and discard duplicates.
   
2. **PDF Creation**:
   - Unique frames are saved as images.
   - Each image is scaled to fit an A4 landscape page in the PDF, which is then saved.

3. **Real-Time Logging**:
   - Logging messages provide feedback on the number of frames processed, duplicates detected, and the status of PDF generation.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following libraries installed:
```bash
pip install opencv-python scikit-image fpdf pillow
```

### Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/s100rab/Video-to-PDF-AI-Tool.git
   cd Video-to-PDF-AI-Tool
   ```

2. **Run the Script**:
   ```bash
   python video_to_pdf.py
   ```
   - Update `video_path` and `output_folder` variables in the script to match your input video and desired output directory.

3. **Outputs**:
   - A folder containing unique images extracted from the video.
   - A PDF file (`output.pdf`) with all unique slides.

---

## 🎉 Example Results

Here’s a snapshot of the results:
![Example PDF](link-to-your-example-image.png) *(Insert an example image here)*

1. **Original Video**: A lecture video with multiple slides.
2. **Output PDF**: A well-organized PDF document containing only the unique slides from the lecture video.

---

## 📈 Performance

- **Speed**: Processes a video frame-by-frame, making it efficient on large videos.
- **Storage Optimization**: Only unique frames are saved, minimizing disk usage.
- **Readability**: Landscape orientation and scaling ensure that slides are clear and easy to read.

---

## 📄 Project Structure

```bash
Video-to-PDF-AI-Tool/
├── extracted_images/     # Directory for unique frame images
├── video_to_pdf.py       # Main script
└── README.md             # Project documentation
```

---

## 🌟 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check out the [issues page](https://github.com/s100rab/Video-to-PDF-AI-Tool/issues).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Connect & Follow
If you liked this project, consider giving it a ⭐️ and connecting with me on [LinkedIn](http://www.linkedin.com/in/100rablakhera)!