import re
import os

def sanitize_filename(name):
    """Remove characters that are invalid for file systems."""
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()


def create_structure_from_markdown(markdown_content, root_dir='.'):
    """Parses markdown outline and creates folders and files."""
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    current_h2_dir = ''
    current_h3_dir = ''
    atomic_notes = []

    for line in markdown_content.split('\n'):
        line = line.strip()
        if not line:
            continue

        # H2 -> Top-level folder
        if line.startswith('## '):
            # Before starting a new h2, process the last h3 section
            if current_h3_dir and atomic_notes:
                create_moc_file(current_h3_dir, os.path.basename(current_h3_dir), atomic_notes)
                atomic_notes = []

            h2_title = sanitize_filename(line[3:])
            current_h2_dir = os.path.join(root_dir, h2_title)
            if not os.path.exists(current_h2_dir):
                os.makedirs(current_h2_dir)
            current_h3_dir = '' # Reset h3 dir

        # H3 -> Sub-folder
        elif line.startswith('### ') and current_h2_dir:
             # Before starting a new h3, process the previous one
            if current_h3_dir and atomic_notes:
                create_moc_file(current_h3_dir, os.path.basename(current_h3_dir), atomic_notes)
                atomic_notes = []

            h3_title = sanitize_filename(line[4:])
            current_h3_dir = os.path.join(current_h2_dir, h3_title)
            if not os.path.exists(current_h3_dir):
                os.makedirs(current_h3_dir)

        # List item -> Atomic note
        elif line.startswith('- ') and current_h3_dir:
            note_title = sanitize_filename(line[2:].split(' ')[0]) # Take the part before numbers
            if not note_title:
                continue
            atomic_notes.append(note_title)
            note_path = os.path.join(current_h3_dir, f"{note_title}.md")
            if not os.path.exists(note_path):
                with open(note_path, 'w', encoding='utf-8') as f:
                    pass # Create empty file

    # Create MOC for the very last section
    if current_h3_dir and atomic_notes:
        create_moc_file(current_h3_dir, os.path.basename(current_h3_dir), atomic_notes)

def create_moc_file(parent_dir, moc_name, notes):
    """Creates and populates a MOC file."""
    moc_filename = f"{moc_name} MOC.md"
    moc_path = os.path.join(parent_dir, moc_filename)
    with open(moc_path, 'w', encoding='utf-8') as f:
        for note in notes:
            f.write(f"- [[{note}]]\n")

if __name__ == "__main__":
    try:
        with open('易经和梅花易数.md', 'r', encoding='utf-8') as f:
            outline = f.read()
        create_structure_from_markdown(outline, 'Obsidian_KnowledgeBase')
        print("Obsidian knowledge base structure created successfully in 'Obsidian_KnowledgeBase' folder.")
    except FileNotFoundError:
        print("Error: '易经和梅花易数.md' not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")