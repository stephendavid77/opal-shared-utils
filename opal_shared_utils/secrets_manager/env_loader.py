import os
from dotenv import load_dotenv

def load_environment_variables(env_path: str = None):
    """
    Loads environment variables from a .env file.

    Args:
        env_path (str, optional): The path to the .env file.
                                  If None, it looks for .env in the current directory
                                  and its parents.
    """
    if env_path:
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv() # Loads from current directory or parents

    print("Environment variables loaded.")

def get_secret(key: str, default: str = None) -> str:
    """
    Retrieves a secret from environment variables.

    Args:
        key (str): The name of the environment variable.
        default (str, optional): Default value if the key is not found.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the key is not found and no default is provided.
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable '{key}' not found and no default provided.")
    return value

if __name__ == "__main__":
    # Example usage:
    # Create a dummy .env file for testing
    with open(".env.test", "w") as f:
        f.write("TEST_VAR=HelloFromEnv\n")
        f.write("ANOTHER_VAR=12345\n")

    print("Loading .env.test...")
    load_environment_variables(env_path=".env.test")
    print(f"TEST_VAR: {get_secret('TEST_VAR')}")
    print(f"ANOTHER_VAR: {get_secret('ANOTHER_VAR')}")

    # Clean up dummy file
    os.remove(".env.test")

    print("\nAttempting to get a non-existent variable:")
    try:
        get_secret("NON_EXISTENT_VAR")
    except ValueError as e:
        print(e)
