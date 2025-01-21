import os
from .file_utils import is_hidden

class DirectoryTreeGenerator:
    def __init__(self):
        self.indent_char = "│   "
        self.branch_char = "├── "
        self.last_branch_char = "└── "
        
    def generate_tree(self, root_path):
        """Generate a tree representation of the directory structure."""
        if not os.path.exists(root_path):
            raise ValueError("Invalid directory path")
            
        tree_content = [os.path.basename(root_path) + "\n"]
        self._generate_tree_recursive(root_path, "", tree_content)
        return "".join(tree_content)
        
    def _generate_tree_recursive(self, path, prefix, tree_content):
        """Recursively generate tree structure."""
        entries = self._get_sorted_entries(path)
        
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            entry_path = os.path.join(path, entry)
            
            # Determine current line's prefix
            current_prefix = prefix + (self.last_branch_char if is_last else self.branch_char)
            
            # Add current entry to tree
            tree_content.append(f"{current_prefix}{entry}\n")
            
            # If directory, process its contents
            if os.path.isdir(entry_path):
                next_prefix = prefix + ("    " if is_last else self.indent_char)
                self._generate_tree_recursive(entry_path, next_prefix, tree_content)
    
    def _get_sorted_entries(self, path):
        """Get sorted list of non-hidden entries in directory."""
        entries = []
        for entry in os.listdir(path):
            if not is_hidden(entry):
                entries.append(entry)
        return sorted(entries, key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))