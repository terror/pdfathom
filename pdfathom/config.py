import json
import os
from dataclasses import dataclass

@dataclass
class Config:
  openai_api_key: str

  @staticmethod
  def load(config_path: str):
    """Load configuration data from a file or prompt the user for the API key."""

    path = os.path.expanduser(config_path)

    if not os.path.exists(path):
      if (api_key := input("Please enter your OpenAI API key: ")):
        with open(path, "w+") as file:
          file.write(json.dumps({"openai_api_key": api_key}))

    with open(path, "r") as config_file:
      config_data = json.load(config_file)

    return Config(**config_data)
