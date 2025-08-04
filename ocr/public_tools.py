import re
import json
from typing import List, Dict, Any, Tuple


def extract_toc_from_json(json_data: Dict[str, Any], indent_size: int = 2) -> str:
    """
    Extract markdown headings from JSON and create a table of contents tree with indentation.
    
    Args:
        json_data: Dictionary containing OCR output with 'pages' key
        indent_size: Number of spaces per indentation level (default: 2)
    
    Returns:
        String containing the formatted TOC tree
    """
    headings = []
    
    # Extract markdown content from all pages
    if 'pages' not in json_data:
        raise ValueError("JSON data must contain 'pages' key")
    
    for page in json_data['pages']:
        if 'markdown' in page:
            page_headings = _extract_headings_from_markdown(page['markdown'], page.get('page_index', 0))
            headings.extend(page_headings)
    
    # Sort headings by page index to maintain order
    headings.sort(key=lambda x: x[2])  # Sort by page_index
    
    # Build TOC tree with indentation
    toc_lines = []
    for level, title, page_index in headings:
        indent = ' ' * ((level - 1) * indent_size)
        toc_lines.append(f"{indent}- {title}")
    
    return '\n'.join(toc_lines)


def _extract_headings_from_markdown(markdown_content: str, page_index: int = 0) -> List[Tuple[int, str, int]]:
    """
    Extract headings from markdown content.
    
    Args:
        markdown_content: Markdown text content
        page_index: Page number for ordering
    
    Returns:
        List of tuples (level, title, page_index)
    """
    headings = []
    
    # Regex pattern to match markdown headings (# ## ### ####)
    heading_pattern = r'^(#{1,4})\s+(.+)$'
    
    lines = markdown_content.split('\n')
    for line in lines:
        match = re.match(heading_pattern, line.strip())
        if match:
            level = len(match.group(1))  # Count the number of '#' characters
            title = match.group(2).strip()
            
            # Clean up title (remove extra spaces, formatting)
            title = re.sub(r'\s+', ' ', title)
            title = title.strip()
            
            if title:  # Only add non-empty titles
                headings.append((level, title, page_index))
    
    return headings


def extract_toc_from_file(file_path: str, indent_size: int = 2) -> str:
    """
    Extract TOC from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        indent_size: Number of spaces per indentation level
    
    Returns:
        String containing the formatted TOC tree
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return extract_toc_from_json(json_data, indent_size)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

# Example usage:
if __name__ == "__main__":
    # Example JSON data structure
    json_file_path = 'ocr_outputs/json/The Diffusion Duality_ocr.json'
    # json_file_path = 'traj/page_list_final.json'
    # json_file_path = 'ocr_outputs/json/deepseek_ocr.json'
    # json_file_path = 'traj/page_list_final.json'
    with open(json_file_path, 'r') as f:
        example_json = json.load(f)
    
    # Generate TOC
    toc = extract_toc_from_json(example_json)
    print(toc)