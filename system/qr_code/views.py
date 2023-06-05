from django.shortcuts import render
from pyzbar import pyzbar
import cv2
import base64
import numpy as np

def qr_code_reader(request):
    if request.method == 'POST':
        if 'image_upload' in request.POST: # Handle file upload
            # Access the uploaded image file
            image_file = request.FILES['image']

            # Read the image using OpenCV
            image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Use pyzbar to scan the QR code
            decoded_objects = pyzbar.decode(gray_image)

            # Process the decoded objects (QR codes)
            qr_code_data = ""
            for obj in decoded_objects:
                qr_code_data += obj.data.decode("utf-8") + "\n"

            # Render the result in the template
            return render(request, 'qr_code_result.html', {'qr_code_data': qr_code_data})
        
        elif 'take_photo' in request.POST: # Handle taking a photo
            # Access the base64-encoded image data
            image_data = request.POST['image_data']

            # Decode the base64-encoded image data
            image_data_decoded = base64.b64decode(image_data)

            # Create a temporary file to store the image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_file.write(image_data_decoded)
                temp_file.close()

                # Read the image using OpenCV
                image = cv2.imread(temp_file.name)

                # Convert the image to grayscale
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Use pyzbar to scan the QR code
                decoded_objects = pyzbar.decode(gray_image)

                # Process the decoded objects (QR codes)
                qr_code_data = ""
                for obj in decoded_objects:
                    qr_code_data += obj.data.decode("utf-8") + "\n"

                # Render the result in the template
                return render(request, 'qr_code_result.html', {'qr_code_data': qr_code_data})

    return render(request, 'qr_code_reader.html')

