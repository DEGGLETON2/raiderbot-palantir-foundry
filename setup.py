
from setuptools import setup, find_packages

setup(
    name="raiderbot-container-transforms",
    version="1.0.0",
    description="RaiderBot Email Intelligence Container Transforms for Foundry",
    packages=find_packages(),
    entry_points={
        "palantir.transforms": [
            "raiderbot_email_container_transform = foundry_container_transform:raiderbot_email_container_transform",
            "raiderbot_container_test_transform = foundry_container_transform:raiderbot_container_test_transform",
        ]
    },
    install_requires=[
        "pandas",
        "palantir-models",
    ]
)
