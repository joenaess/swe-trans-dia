import requests


def test_transcribe_invalid_file_type():
    """
    Tests that the /transcribe/ endpoint returns a 400 status code
    and the correct error message when an invalid file type is provided.
    """
    url = "http://localhost:8000/transcribe/"  # Adjust if your API runs on a different port

    # Send a POST request with a text file
    files = {"file": ("test.txt", b"This is a text file")}  # 'b' denotes bytes
    response = requests.post(url, files=files)

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type. Only .wav, .mp3, and .ogg are supported."}

# You can add more test functions here to test other scenarios
# For example:
#   - Valid file type upload
#   - Handling of min/max speakers parameters
#   - Server errors
