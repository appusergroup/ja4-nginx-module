#!/usr/bin/env python3
"""
Test script for ECH and ALPS TLS extensions using curl_cffi.

This script uses curl_cffi to impersonate modern browsers (Chrome 117+)
which natively support ECH and ALPS extensions. It sends HTTPS requests
to the local nginx server and captures the JA4 fingerprint response.
"""

import sys

def test_with_curl_cffi(test_name: str, browser_version: str = "chrome117") -> str:
    """
    Use curl_cffi to send request with modern browser fingerprint.
    
    Args:
        test_name: Name of the test (for logging)
        browser_version: Browser to impersonate (default: chrome117)
    
    Returns:
        HTTP response body containing JA4 fingerprint
    """
    try:
        import curl_cffi.requests as requests
        
        # Make HTTPS request with browser impersonation
        # Modern Chrome versions (117+) include ECH and ALPS extensions
        response = requests.get(
            "https://localhost",
            impersonate=browser_version,
            verify=False,  # Skip certificate verification for self-signed cert
            timeout=10
        )
        
        return response.text
        
    except ImportError:
        print("ERROR: curl_cffi not installed. Install with: pip install curl_cffi", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: test_ech_alps.py <test_type>", file=sys.stderr)
        print("  test_type: 'ech' or 'alps'", file=sys.stderr)
        sys.exit(1)
    
    test_type = sys.argv[1]
    
    # Both ECH and ALPS are present in Chrome 117+
    # We use the same browser version for both tests
    output = test_with_curl_cffi(test_type, "chrome136")
    
    print(output, end='')
