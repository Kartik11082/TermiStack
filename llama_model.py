import json
import os
import signal
import subprocess
import sys

import requests


class LlamaModel:
    """
    A class to interact with the Llama3.2 model, including starting, stopping the server,
    querying, and managing session variables.
    """

    def __init__(
        self, model_url="http://127.0.0.1:11434/api/generate", model_name="llama3.2"
    ):
        """
        Initialize the LlamaModel with the given model URL and model name.
        """
        self.model_url = model_url
        self.model_name = model_name
        self.session_variables = {}
        self.llama_process = None

    def start_server(self):
        """
        Starts the Llama3.2 server in a subprocess.
        """
        if self.llama_process is None:
            self.llama_process = subprocess.Popen(
                ["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            print(f"Llama3.2 server started with PID: {self.llama_process.pid}")
        else:
            print("Llama3.2 server is already running.")

    def stop_server(self):
        """
        Stops the Llama3.2 server and releases resources.
        """
        try:
            if self.llama_process:
                print("Stopping Llama3.2 server...")
                self.llama_process.terminate()
                self.llama_process.wait()
                self.llama_process = None
                print("Llama3.2 server stopped.")
            else:
                print("Llama3.2 server is not running.")
        except Exception as e:
            print("Error:", type(e).__name__, __file__, e.__traceback__.tb_lineno)

    def parse_json_responses(self, json_string):
        """
        Parses a string containing multiple JSON objects and extracts the 'response' field to form a sentence.

        Args:
            json_string (str): A string containing JSON objects separated by newlines.

        Returns:
            str: The combined sentence formed from the 'response' fields.
        """
        try:
            sentences = []
            # Split the string by newlines
            lines = json_string.split("\n")

            for line in lines:
                if line.strip():  # Skip empty lines
                    try:
                        # Parse the JSON object
                        json_obj = json.loads(line)
                        # Extract the 'response' field and add to the sentence
                        if "response" in json_obj:
                            sentences.append(json_obj["response"])
                    except Exception as e:
                        # Skip invalid JSON lines
                        print(
                            "Error:",
                            type(e).__name__,
                            __file__,
                            e.__traceback__.tb_lineno,
                        )
                        continue

            # Join all the sentences to form the full output
            return "".join(sentences)
        except Exception as e:
            print("Error:", type(e).__name__, __file__, e.__traceback__.tb_lineno)

    def send_request(self, payload):
        """
        Sends a POST request to the Llama3.2 API and returns the response as JSON.

        Parameters:
            payload (dict): The data to be sent in the POST request.

        Returns:
            dict: The JSON response from the Llama3.2 API.
        """
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Python-requests/2.31.0",
        }

        try:
            response = requests.post(self.model_url, json=payload, headers=headers)
            response.raise_for_status()
            response = self.parse_json_responses(response.text)
            return response
        except requests.exceptions.RequestException as e:
            print("Error:", type(e).__name__, __file__, e.__traceback__.tb_lineno)
            return None

    def format_response(self, response_data):
        """
        Reconstructs the response text from partial responses.

        Parameters:
            response_data (list): A list of responses that form the full sentence.

        Returns:
            str: The full sentence formed from the partial responses.
        """
        sentence = ""
        for part in response_data:
            part_data = part.get("response", "")
            sentence += part_data
        return sentence.strip()

    def ask_question(self, question):
        """
        Asks a question to the Llama3.2 model and returns the response.

        Parameters:
            question (str): The question to ask to the Llama3.2 model.

        Returns:
            str: The model's response to the question.
        """
        try:
            payload = {"model": self.model_name, "prompt": question}
            response_data = self.send_request(payload)
            if response_data:
                return response_data
                # return self.format_response(response_data["context"])
            return "Error: No response received."
        except Exception as e:
            print("Error:", type(e).__name__, __file__, e.__traceback__.tb_lineno)

    def set_session_variable(self, variable, value):
        """
        Sets a session variable for the Llama3.2 model.

        Parameters:
            variable (str): The name of the session variable.
            value (str): The value to assign to the session variable.
        """
        self.session_variables[variable] = value
        print(f"Session variable '{variable}' set to: {value}")

    def show_model_info(self):
        """
        Fetches and returns information about the current model.

        Returns:
            str: The model's information.
        """
        payload = {"model": self.model_name, "prompt": "/show"}
        response_data = self.send_request(payload)
        if response_data:
            return response_data.get("response", "No model information found.")
        return "Error: No model information received."

    def load_model(self, model_name):
        """
        Loads a specific model for the session.

        Parameters:
            model_name (str): The name of the model to load.

        Returns:
            str: Confirmation message or error message.
        """
        payload = {"model": self.model_name, "prompt": f"/load {model_name}"}
        response_data = self.send_request(payload)
        if response_data:
            return response_data.get(
                "response", f"Model '{model_name}' loaded successfully."
            )
        return f"Error: Unable to load model '{model_name}'."

    def save_model(self, model_name):
        """
        Saves the current model session.

        Parameters:
            model_name (str): The name of the model to save.

        Returns:
            str: Confirmation message or error message.
        """
        payload = {"model": self.model_name, "prompt": f"/save {model_name}"}
        response_data = self.send_request(payload)
        if response_data:
            return response_data.get(
                "response", f"Model '{model_name}' saved successfully."
            )
        return f"Error: Unable to save model '{model_name}'."

    def clear_session(self):
        """
        Clears the current session context.

        Returns:
            str: Confirmation message or error message.
        """
        payload = {"model": self.model_name, "prompt": "/clear"}
        response_data = self.send_request(payload)
        if response_data:
            return "Session context cleared."
        return "Error: Unable to clear session."


# ================================
# Example Usage in Another Project
# ================================


def main():
    # Initialize the Llama model object
    llama_model = LlamaModel()

    # Start the server (you can call this in your main project as well)
    llama_model.start_server()

    # Ask a question (this can be reused in any project)
    question = "What is the capital of India?"
    answer = llama_model.ask_question(question)
    print(f"Answer: {answer}")

    # Optionally, set a session variable
    llama_model.set_session_variable("language", "English")

    # Show model information
    model_info = llama_model.show_model_info()
    print(f"Model Info: {model_info}")

    # Stop the server when done
    llama_model.stop_server()


if __name__ == "__main__":
    main()
