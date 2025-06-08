"""
AtCoder Memory Limit Parsing Patch

This module patches the AtCoder parsing logic in online-judge-api-client
to handle changes in AtCoder's HTML structure that cause parsed_memory_limit
to be None, resulting in AssertionError.

Issue: https://github.com/naoya/oj/issues/2
"""

import re
from typing import Optional
from logging import getLogger

logger = getLogger(__name__)


def _patched_parse_memory_limit_from_html(html: str) -> Optional[str]:
    """
    Enhanced memory limit parser that tries multiple strategies
    to extract memory limit from AtCoder problem pages.
    
    Args:
        html: HTML content of the AtCoder problem page
        
    Returns:
        Memory limit string (e.g., "1024 MB") or None if not found
    """
    # Strategy 1: Original pattern - look for "Memory Limit" in table
    patterns = [
        # Original format: Memory Limit: XXX MB
        r'Memory\s+Limit[:\s]*(\d+(?:\.\d+)?\s*[KMGT]?B)',
        # Alternative format: メモリ制限: XXX MB  
        r'メモリ制限[:\s]*(\d+(?:\.\d+)?\s*[KMGT]?B)',
        # Table row format: <th>Memory Limit</th><td>XXX MB</td>
        r'<th[^>]*>Memory\s+Limit</th>\s*<td[^>]*>([^<]*[KMGT]?B[^<]*)</td>',
        # Table row format: <th>メモリ制限</th><td>XXX MB</td>
        r'<th[^>]*>メモリ制限</th>\s*<td[^>]*>([^<]*[KMGT]?B[^<]*)</td>',
        # Generic memory pattern in problem statement
        r'(\d+(?:\.\d+)?\s*[KMGT]?B)\s*memory',
        # More flexible pattern for various HTML structures
        r'limit[^>]*>([^<]*\d+[^<]*[KMGT]?B)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            memory_limit = match.group(1).strip()
            logger.debug(f"Found memory limit using pattern '{pattern}': {memory_limit}")
            return memory_limit
    
    # Strategy 2: Look for common memory values in any context
    common_memory_values = re.findall(r'\b(\d+(?:\.\d+)?\s*[KMGT]?B)\b', html, re.IGNORECASE)
    memory_candidates = []
    
    for value in common_memory_values:
        # Filter for reasonable memory limit values (typically 64MB to 8GB)
        match = re.match(r'(\d+(?:\.\d+)?)\s*([KMGT]?)B', value, re.IGNORECASE)
        if match:
            number, unit = match.groups()
            number = float(number)
            unit = unit.upper()
            
            # Convert to MB for comparison
            mb_value = number
            if unit == 'KB':
                mb_value = number / 1024
            elif unit == 'GB':
                mb_value = number * 1024
            elif unit == 'TB':
                mb_value = number * 1024 * 1024
            
            # Reasonable memory limits for competitive programming (64MB to 8GB)
            if 64 <= mb_value <= 8192:
                memory_candidates.append(value)
    
    if memory_candidates:
        # Take the first reasonable candidate
        memory_limit = memory_candidates[0]
        logger.debug(f"Found memory limit candidate: {memory_limit}")
        return memory_limit
    
    logger.warning("Could not parse memory limit from AtCoder HTML")
    return None


def apply_atcoder_memory_limit_patch():
    """
    Apply monkey patch to fix AtCoder memory limit parsing issue.
    """
    try:
        from onlinejudge.service.atcoder import AtCoderProblemData
        
        # Save original method if it exists
        original_from_html = getattr(AtCoderProblemData, '_from_html', None)
        
        if original_from_html is None:
            logger.warning("Could not find AtCoderProblemData._from_html method to patch")
            return
        
        def patched_from_html(html, problem=None, session=None, response=None, timestamp=None):
            """
            Patched version of AtCoderProblemData._from_html that handles
            memory limit parsing failures gracefully.
            """
            try:
                # Try the original implementation first
                return original_from_html(html, problem=problem, session=session, response=response, timestamp=timestamp)
            except AssertionError as e:
                # If assertion failed, it's likely the parsed_memory_limit issue
                logger.warning(f"Original AtCoder parsing failed with AssertionError: {e}")
                logger.info("Attempting to parse with patched memory limit parser...")
                
                # Create a minimal fallback that extracts what we can
                # This is a simplified version that focuses on memory limit parsing
                try:
                    # Parse memory limit with our enhanced parser
                    parsed_memory_limit = _patched_parse_memory_limit_from_html(html)
                    
                    if parsed_memory_limit:
                        logger.info(f"Successfully parsed memory limit: {parsed_memory_limit}")
                        
                        # For now, we'll create a minimal data object with just the memory limit
                        # The actual implementation would need more parsing, but this focuses on the issue
                        
                        # Instead of fully reimplementing the parser, let's try a different approach:
                        # modify the HTML to include a memory limit that the original parser can find
                        if "Memory Limit" not in html and "メモリ制限" not in html:
                            # Inject a memory limit that the original parser can find
                            memory_section = f'<tr><th>Memory Limit</th><td>{parsed_memory_limit}</td></tr>'
                            # Try to insert it into an existing table
                            if '</table>' in html:
                                html = html.replace('</table>', memory_section + '</table>', 1)
                            else:
                                # Fallback: add a simple table at the beginning
                                html = f'<table>{memory_section}</table>' + html
                            
                            # Try original parser again with modified HTML
                            return original_from_html(html, problem=problem, session=session, response=response, timestamp=timestamp)
                    
                    # If we still can't parse, provide a minimal fallback
                    logger.warning("Could not parse memory limit, using default fallback")
                    # For now, just re-raise to maintain compatibility
                    # In a full implementation, we'd return a minimal data object
                    raise
                    
                except Exception as patch_error:
                    logger.error(f"Patched parser also failed: {patch_error}")
                    raise e  # Re-raise original error
        
        # Apply the patch
        AtCoderProblemData._from_html = staticmethod(patched_from_html)
        logger.info("Applied AtCoder memory limit parsing patch")
        
    except ImportError:
        logger.warning("Could not import AtCoderProblemData - patch not applied")
    except Exception as e:
        logger.error(f"Failed to apply AtCoder memory limit patch: {e}")


# Apply the patch when this module is imported
apply_atcoder_memory_limit_patch()