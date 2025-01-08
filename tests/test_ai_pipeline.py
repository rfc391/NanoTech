
import pytest
from hypothesis import given, strategies as st
import cv2
import numpy as np

# Hypothesis test for OpenCV image processing
@given(image_data=st.lists(st.lists(st.integers(min_value=0, max_value=255), min_size=10, max_size=10), min_size=10, max_size=10))
def test_opencv_processing(image_data):
    # Convert the generated data into a NumPy array
    image_array = np.array(image_data, dtype=np.uint8)
    
    # Ensure the input array is treated as a grayscale image
    processed_image = cv2.GaussianBlur(image_array, (5, 5), 0)
    
    # Validate that the processed image has the same shape as input
    assert processed_image.shape == image_array.shape

# Hypothesis test for explainability with XAITK
@given(values=st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=10, max_size=10))
def test_explainability(values):
    from xaitk.saliency import PerturbImage
    # Convert the values into a 2D array to simulate an image
    image = np.array(values, dtype=np.float32).reshape(10, 10)
    
    # Instantiate PerturbImage and apply it
    perturb = PerturbImage()
    saliency_map = perturb(image)
    
    # Validate that a saliency map is generated
    assert saliency_map is not None
