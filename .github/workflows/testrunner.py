import os
import subprocess
import tempfile

def test_runner():
    # Create a temporary input file
    with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
        input_file_name = temp_input_file.name
        # Write test data to the input file
        test_data = b'This is a test string for encryption.'
        temp_input_file.write(test_data)

    # Define output file name and password
    temp_encrypted_file = tempfile.NamedTemporaryFile(delete=False).name
    password = 'securepassword111'

    try:
        # Call the runner executable to encrypt the file
        subprocess.run(['./runner', 'encrypt', input_file_name, temp_encrypted_file, password], check=True)

        # Read the original data
        with open(input_file_name, 'rb') as original_file:
            original_data = original_file.read()

        # Read the encrypted data
        with open(temp_encrypted_file, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Check if the contents of the input file and output file are identical
        assert original_data != encrypted_data, "Data should be encrypted and not match the original data."

        # Call the runner executable to decrypt the file
        temp_decrypted_file = tempfile.NamedTemporaryFile(delete=False).name
        subprocess.run(['./runner', 'decrypt', temp_encrypted_file, temp_decrypted_file, password], check=True)

        # Read the decrypted data
        with open(temp_decrypted_file, 'rb') as decrypted_file:
            decrypted_data = decrypted_file.read()

        # Validate that the decrypted data matches the original data
        assert original_data == decrypted_data, "Decrypted data does not match original data!"

        print("Test passed: Decrypted data matches original data.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the subprocess: {e}")
    except AssertionError as e:
        print(e)
    finally:
        # Clean up temporary files
        os.remove(input_file_name)
        os.remove(temp_encrypted_file)
        if os.path.exists(temp_decrypted_file):
            os.remove(temp_decrypted_file)

if __name__ == "__main__":
    test_runner()