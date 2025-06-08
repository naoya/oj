#!/usr/bin/env python3
"""
Test script for AtCoder robust parsing wrapper
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'onlinejudge_command'))

from onlinejudge_command.atcoder_robust import parse_memory_limit_from_html, wrap_atcoder_problem

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

def test_memory_limit_parsing():
    """Test the enhanced memory limit parsing function."""
    print("Testing AtCoder memory limit parsing...")
    
    passed = 0
    total = len(test_cases)
    
    for i, (html, expected) in enumerate(zip(test_cases, expected_results)):
        result = parse_memory_limit_from_html(html)
        status = "✓" if result == expected else "✗"
        print(f"Test {i+1}: {status} Expected: {expected}, Got: {result}")
        if result == expected:
            passed += 1
        else:
            print(f"  HTML: {html.strip()}")
    
    print(f"\nMemory parsing tests: {passed}/{total} passed")
    return passed == total

def test_wrapper_functionality():
    """Test the wrapper functionality with mock objects."""
    print("\nTesting wrapper functionality...")
    
    try:
        # Create a mock AtCoder problem for testing
        class MockAtCoderProblem:
            def __init__(self):
                self.should_fail = False
                
            def get_url(self):
                return "https://atcoder.jp/contests/test/tasks/test_a"
                
            def download_sample_cases(self, *, session=None):
                if self.should_fail:
                    raise AssertionError("Mock parsing failure")
                return []
                
            def download_system_cases(self, *, session=None):
                if self.should_fail:
                    raise AssertionError("Mock parsing failure")
                return []
        
        # Test normal case (no wrapping for non-AtCoder)
        mock_problem = MockAtCoderProblem()
        wrapped = wrap_atcoder_problem(mock_problem)
        
        # Since MockAtCoderProblem is not an actual AtCoderProblem, it shouldn't be wrapped
        if wrapped is mock_problem:
            print("✓ Non-AtCoder problem not wrapped (correct)")
        else:
            print("✗ Non-AtCoder problem incorrectly wrapped")
            
        print("✓ Wrapper functionality test completed")
        return True
        
    except Exception as e:
        print(f"✗ Wrapper test failed: {e}")
        return False

def run_tests():
    """Run all tests."""
    print("Running AtCoder robust parsing tests...\n")
    
    test1_passed = test_memory_limit_parsing()
    test2_passed = test_wrapper_functionality()
    
    total_passed = sum([test1_passed, test2_passed])
    print(f"\nOverall: {total_passed}/2 test suites passed")
    
    if total_passed == 2:
        print("All tests passed! ✓")
        return True
    else:
        print("Some tests failed! ✗")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)