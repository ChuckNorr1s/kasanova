import subprocess
import os

def run_poetry_script(script_name: str, *args, cwd: str = None):
    """
    Run a Poetry script via subprocess.
    
    :param script_name: The name of the script registered in pyproject.toml.
    :param args: Any arguments you want to pass to the script.
    :param cwd: The working directory where pyproject.toml is located.
    """
    # If no working directory is provided, assume this file is in a subdirectory,
    # and set cwd to its parent directory (where pyproject.toml is located).
    if cwd is None:
        cwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
        
    command = ["poetry", "run", script_name] + list(args)
    result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
    return result.stdout, result.stderr

if __name__ == "__main__":
    # Initialize the starting input and a container to store each iteration's result.
    initial_input = "What is life?"
    outrage_amplifiers = "3"
    results = []
    
    # Set the input for the first run.
    current_input = initial_input
    
    # Run the script 3 times, each time passing the previous output as the next input.
    for i in range(3):
        output, error = run_poetry_script("generate-counter-response", current_input, outrage_amplifiers)
        
        # Save the result for this iteration.
        iteration_result = {
            "iteration": i + 1,
            "input": current_input,
            "output": output.strip(),
            "error": error.strip() if error else None,
        }
        results.append(iteration_result)
        
        # Use the output as the input for the next iteration.
        current_input = output.strip()
    
    # Print the collected results.
    print("Collected Results:")
    for result in results:
        print(result.get("output"))
