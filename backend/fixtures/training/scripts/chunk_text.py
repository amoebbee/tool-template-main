#!/usr/bin/env python3
"""
Text chunking utility for creating overlapping chunks for parsing training data.
"""

import os
import json
from pathlib import Path

def chunk_text(filepath, output_dir, chunk_size=500, overlap=50):
    """
    Divide text into overlapping chunks for processing.
    
    Args:
        filepath: Path to input text file
        output_dir: Directory to save chunks
        chunk_size: Lines per chunk
        overlap: Lines to overlap between chunks
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    chunks = []
    step = chunk_size - overlap
    
    for i in range(0, len(lines), step):
        chunk_lines = lines[i:i + chunk_size]
        if len(chunk_lines) < 100:  # Skip very small final chunks
            if chunks:
                # Add remaining lines to last chunk
                chunks[-1]['lines'].extend(chunk_lines)
                chunks[-1]['end_line'] = min(i + len(chunk_lines), len(lines))
        else:
            chunk = {
                'number': len(chunks) + 1,
                'start_line': i + 1,  # 1-indexed for readability
                'end_line': min(i + chunk_size, len(lines)),
                'lines': chunk_lines,
                'line_count': len(chunk_lines)
            }
            chunks.append(chunk)
    
    # Save chunks
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for chunk in chunks:
        # Save text
        chunk_file = Path(output_dir) / f"chunk_{chunk['number']:02d}.txt"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.writelines(chunk['lines'])
        
        # Save metadata
        meta_file = Path(output_dir) / f"chunk_{chunk['number']:02d}_meta.json"
        meta = {
            'chunk_number': chunk['number'],
            'start_line': chunk['start_line'],
            'end_line': chunk['end_line'],
            'line_count': chunk['line_count'],
            'file': str(chunk_file.name)
        }
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)
    
    # Save summary
    summary_file = Path(output_dir) / "chunks_summary.json"
    summary = {
        'source_file': str(filepath),
        'total_lines': len(lines),
        'chunk_size': chunk_size,
        'overlap': overlap,
        'total_chunks': len(chunks),
        'chunks': [
            {
                'number': c['number'],
                'start_line': c['start_line'],
                'end_line': c['end_line'],
                'line_count': c['line_count']
            }
            for c in chunks
        ]
    }
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Created {len(chunks)} chunks from {filepath}")
    print(f"Saved to {output_dir}")
    return chunks

if __name__ == "__main__":
    # Process Hyperion
    hyperion_chunks = chunk_text(
        "ow_parse_examples/hyperion.txt",
        "backend/fixtures/training/hyperion/source_chunks",
        chunk_size=500,
        overlap=50
    )
    
    # Process The Wager
    wager_chunks = chunk_text(
        "ow_parse_examples/wager.txt",
        "backend/fixtures/training/wager/source_chunks",
        chunk_size=500,
        overlap=50
    )