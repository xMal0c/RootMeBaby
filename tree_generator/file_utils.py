import os

def is_hidden(filename):
    """Check if a file or directory is hidden."""
    return filename.startswith('.') or \
           filename.startswith('__') or \
           filename in {'.git', '.svn', '.hg', '.idea', '__pycache__'}