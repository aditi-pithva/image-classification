# Image Classification Project

Welcome to the Image Classification project! This project is part of my learning journey in Artificial Intelligence, where I explore various image features to classify images effectively.

## Project Overview

This project focuses on classifying images based on several key features, including:

- **Composition**
- **Exposure**
- **Color-Contrast**
- **Focus**
- **Sharpness**
- **Brightness**

### Current Progress

1. **AWS Rekognition**: 
   - I have utilized the AWS Rekognition DetectLabels API to extract crucial image attributes such as overall image brightness, sharpness, and contrast.
   - Additionally, I have extracted brightness and sharpness metrics specifically for the foreground and background of the images.

2. **Saliency Detection Models**:
   - I am currently exploring Saliency Detection Models, with a particular focus on enhancing the analysis of image composition.

### Next Steps

- Continue refining the Saliency Detection Model to improve the accuracy of composition-based classification.
- Integrate additional image features to enhance the classification model.

## Getting Started

### Prerequisites

- AWS account with access to Rekognition and S3 services.
- Python 3.x installed.
- Necessary Python packages (can be installed via `requirements.txt`).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aditi-pithva/image-classification.git
