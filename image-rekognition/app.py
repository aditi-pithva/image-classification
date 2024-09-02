from flask import Flask, render_template, send_file
import boto3
from io import BytesIO
import pandas as pd

app = Flask(__name__)

# Enable logging for boto3
boto3.set_stream_logger('')

# AWS S3 Configuration
REGION_NAME = 'us-east-1'
BUCKET_NAME = 'train-images-bucket'

# Initialize boto3 client for S3 and Rekognition
s3_client = boto3.client(
    's3',
    region_name=REGION_NAME
)

rekognition_client = boto3.client(
    'rekognition',
    region_name=REGION_NAME
)

@app.route('/')
def index():
    # List all objects (images) in the S3 bucket
    objects = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    image_files = [obj['Key'] for obj in objects.get('Contents', [])]

        # Initialize an empty list to store results
    results = []

    # Iterate over each image in the S3 bucket
    for image_name in image_files:
        try:
            # Call Rekognition to detect labels and image quality
            rekognition_response = rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': BUCKET_NAME,
                        'Name': image_name
                    }
                },
                MaxLabels=10,
                MinConfidence=80,
                Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"]
            )

            print(rekognition_response)

            # Extract image quality from the response
            if "ImageProperties" in rekognition_response:
                image_properties = rekognition_response["ImageProperties"]

                # Extract overall quality
                overall_quality = image_properties.get('Quality', {})
                overall_brightness = overall_quality.get('Brightness', None)
                overall_sharpness = overall_quality.get('Sharpness', None)
                overall_contrast = overall_quality.get('Contrast', None)

                # Extract foreground quality
                foreground_quality = image_properties.get('Foreground', {}).get('Quality', {})
                foreground_brightness = foreground_quality.get('Brightness', None)
                foreground_sharpness = foreground_quality.get('Sharpness', None)
                foreground_contrast = foreground_quality.get('Contrast', None)

                # Extract background quality
                background_quality = image_properties.get('Background', {}).get('Quality', {})
                background_brightness = background_quality.get('Brightness', None)
                background_sharpness = background_quality.get('Sharpness', None)
                background_contrast = background_quality.get('Contrast', None)
            else:
                overall_brightness = overall_sharpness = overall_contrast = None
                foreground_brightness = foreground_sharpness = foreground_contrast = None
                background_brightness = background_sharpness = background_contrast = None

            # Structure the final response for this image
            result = {
                "Image": image_name,
                "Overall_Brightness": overall_brightness,
                "Overall_Sharpness": overall_sharpness,
                "Overall_Contrast": overall_contrast,
                "Foreground_Brightness": foreground_brightness,
                "Foreground_Sharpness": foreground_sharpness,
                "Foreground_Contrast": foreground_contrast,
                "Background_Brightness": background_brightness,
                "Background_Sharpness": background_sharpness,
                "Background_Contrast": background_contrast,
            }

            # Append the response to the results list
            results.append(result)

        except Exception as e:
            print(f"Error processing image {image_name}: {e}")

    # Convert the results to a DataFrame
    df = pd.DataFrame(results)

    # Optionally save the DataFrame to a CSV file
    df.to_csv('image_analysis_results.csv', index=False)

    # Display the DataFrame
    print(df)

    return render_template('index.html', images=image_files)

@app.route('/image/<filename>')
def get_image(filename):
    # Retrieve the image from S3
    file_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return send_file(BytesIO(file_obj['Body'].read()), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
