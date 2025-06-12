#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from linkedin_profile_finder.crew import LinkedinProfileFinder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI and LLMs',
    }
    
    try:
        LinkedinProfileFinder().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

