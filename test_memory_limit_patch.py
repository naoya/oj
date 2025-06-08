#!/usr/bin/env python3
"""
Test script for AtCoder memory limit parsing patch
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'onlinejudge_command'))

from onlinejudge_command.atcoder_memory_limit_patch import _patched_parse_memory_limit_from_html

# Test cases representing different AtCoder HTML formats
test_cases = [
    # Case 1: Standard table format
    '''
    <table>
        <tr><th>Time Limit</th><td>2 sec</td></tr>
        <tr><th>Memory Limit</th><td>1024 MB</td></tr>
    </table>
    ''',
    
    # Case 2: Japanese format
    '''
    <table>
        <tr><th>実行時間制限</th><td>2 sec</td></tr>
        <tr><th>メモリ制限</th><td>512 MB</td></tr>
    </table>
    ''',
    
    # Case 3: Alternative spacing
    '''
    <div>Memory Limit: 256 MB</div>
    ''',
    
    # Case 4: Different units
    '''
    <tr><th>Memory Limit</th><td>2 GB</td></tr>
    ''',
    
    # Case 5: No memory limit found
    '''
    <div>Some other content without memory info</div>
    ''',
    
    # Case 6: Multiple memory values (should pick first reasonable one)
    '''
    <div>Memory: 1024 MB for submissions</div>
    <div>Stack: 8 MB</div>
    '''
]

expected_results = [
    "1024 MB",
    "512 MB", 
    "256 MB",
    "2 GB",
    None,
    "1024 MB"
]

def run_tests():
    print("Testing AtCoder memory limit parsing patch...")
    
    for i, (html, expected) in enumerate(zip(test_cases, expected_results)):
        result = _patched_parse_memory_limit_from_html(html)
        status = "✓" if result == expected else "✗"
        print(f"Test {i+1}: {status} Expected: {expected}, Got: {result}")
        if result != expected:
            print(f"  HTML: {html.strip()}")
    
    print("\nPatch logic test completed.")

if __name__ == "__main__":
    run_tests()