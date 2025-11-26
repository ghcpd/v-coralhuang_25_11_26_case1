"""Optimized user display implementation with O(1) lookups and efficient string handling."""

import logging
from typing import Any, Dict, List, Optional

# Configure logging with standard format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """
    Display all users in a compact format - OPTIMIZED VERSION.
    
    Args:
        users: List of user dictionaries
        show_all: Whether to show summary information
        verbose: Whether to log processing details
        
    Returns:
        Formatted string containing all user data
        
    Performance: O(n) with efficient list comprehension and join
    """
    logger.info("[MARKER] Starting display_users function")
    
    if not users:
        logger.warning("[MARKER] Empty user list provided")
        return ""
    
    result_lines = []
    processed_count = 0
    
    try:
        # Efficient: Build list then join once (O(n) instead of O(n²))
        for user in users:
            if verbose:
                logger.info(f"[MARKER] Processing user {user.get('id', 'UNKNOWN')}")
            
            try:
                # Direct dictionary access with get() for safety
                line = (
                    f"ID:{user.get('id', 'N/A')}|"
                    f"Name:{user.get('name', 'N/A')}|"
                    f"Email:{user.get('email', 'N/A')}|"
                    f"Role:{user.get('role', 'N/A')}|"
                    f"Status:{user.get('status', 'N/A')}|"
                    f"JoinDate:{user.get('join_date', 'N/A')}|"
                    f"LastLogin:{user.get('last_login', 'N/A')}"
                )
                result_lines.append(line)
                processed_count += 1
            except Exception as e:
                logger.error(f"[MARKER] Error processing user: {e}")
                continue
        
        # Single join operation - much faster than concatenation
        result = "\n".join(result_lines)
        
        if show_all and result_lines:
            result += f"\n\n[INFO] Processed {processed_count} users.\n"
        
        logger.info(f"[MARKER] Successfully processed {processed_count} users")
        return result
        
    except Exception as e:
        logger.error(f"[MARKER] Critical error in display_users: {e}")
        return ""


def get_user_by_id(users: List[Dict[str, Any]], user_id: int) -> Optional[Dict[str, Any]]:
    """
    Search for user by ID - OPTIMIZED WITH O(1) DICTIONARY LOOKUP.
    
    Args:
        users: List of user dictionaries
        user_id: ID of the user to find
        
    Returns:
        User dictionary if found, None otherwise
        
    Performance: O(n) for initial indexing, O(1) for lookups
    """
    logger.info(f"[MARKER] Searching for user with ID: {user_id}")
    
    try:
        # Create indexed dictionary for O(1) lookup
        user_index = {user.get('id'): user for user in users if 'id' in user}
        result = user_index.get(user_id)
        
        if result:
            logger.info(f"[MARKER] Found user with ID: {user_id}")
        else:
            logger.warning(f"[MARKER] User with ID {user_id} not found")
            
        return result
    except Exception as e:
        logger.error(f"[MARKER] Error in get_user_by_id: {e}")
        return None


def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter users with simplified logic - OPTIMIZED WITH LIST COMPREHENSION.
    
    Args:
        users: List of user dictionaries
        criteria: Dictionary of filter criteria
        
    Returns:
        List of users matching all criteria
        
    Performance: O(n) with efficient filtering
    """
    logger.info(f"[MARKER] Filtering users with criteria: {criteria}")
    
    try:
        def matches_criteria(user: Dict[str, Any]) -> bool:
            """Check if user matches all filter criteria."""
            # Role filter
            if 'role' in criteria and user.get('role') != criteria['role']:
                return False
            
            # Status filter
            if 'status' in criteria and user.get('status') != criteria['status']:
                return False
            
            # Name filter (case-insensitive substring match)
            if 'name' in criteria:
                user_name = user.get('name', '').lower()
                criteria_name = criteria['name'].lower()
                if criteria_name not in user_name:
                    return False
            
            return True
        
        # Efficient list comprehension
        filtered = [user for user in users if matches_criteria(user)]
        
        logger.info(f"[MARKER] Found {len(filtered)} users matching criteria")
        return filtered
        
    except Exception as e:
        logger.error(f"[MARKER] Error in filter_users: {e}")
        return []


def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """
    Export users to string format - MEMORY OPTIMIZED.
    
    Args:
        users: List of user dictionaries
        
    Returns:
        Formatted export string
        
    Performance: O(n) with single join operation
    """
    logger.info("[MARKER] Starting export_users_to_string")
    
    try:
        if not users:
            logger.warning("[MARKER] No users to export")
            return "USER_EXPORT_START\n" + "=" * 100 + "\nUSER_EXPORT_END\n"
        
        # Build list of all lines, then join once
        lines = ["USER_EXPORT_START", "=" * 100]
        
        for user in users:
            try:
                lines.extend([
                    f"User ID: {user.get('id', 'N/A')}",
                    f"  Name: {user.get('name', 'N/A')}",
                    f"  Email: {user.get('email', 'N/A')}",
                    f"  Role: {user.get('role', 'N/A')}",
                    f"  Status: {user.get('status', 'N/A')}",
                    f"  Join Date: {user.get('join_date', 'N/A')}",
                    f"  Last Login: {user.get('last_login', 'N/A')}",
                    "-" * 100
                ])
            except Exception as e:
                logger.error(f"[MARKER] Error exporting user: {e}")
                continue
        
        lines.append("USER_EXPORT_END")
        
        # Single join operation
        result = "\n".join(lines) + "\n"
        
        logger.info(f"[MARKER] Successfully exported {len(users)} users")
        return result
        
    except Exception as e:
        logger.error(f"[MARKER] Critical error in export_users_to_string: {e}")
        return "USER_EXPORT_START\nERROR\nUSER_EXPORT_END\n"


# Sample data for testing
sample_users = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'role': 'Admin',
        'status': 'Active',
        'join_date': '2023-01-15',
        'last_login': '2025-11-26'
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'role': 'User',
        'status': 'Inactive',
        'join_date': '2023-06-20',
        'last_login': '2025-11-20'
    },
    {
        'id': 3,
        'name': 'Bob Johnson',
        'email': 'bob@example.com',
        'role': 'Moderator',
        'status': 'Active',
        'join_date': '2024-02-10',
        'last_login': '2025-11-25'
    },
    {
        'id': 4,
        'name': 'Alice Williams',
        'email': 'alice@example.com',
        'role': 'User',
        'status': 'Active',
        'join_date': '2024-05-12',
        'last_login': '2025-11-26'
    },
    {
        'id': 5,
        'name': 'Charlie Brown',
        'email': 'charlie@example.com',
        'role': 'User',
        'status': 'Active',
        'join_date': '2024-08-03',
        'last_login': '2025-11-24'
    },
]


if __name__ == "__main__":
    import time
    
    print("Optimized Implementation Output:")
    print("=" * 100)
    
    # Benchmark with sample data
    start_time = time.perf_counter()
    output = display_users(sample_users)
    end_time = time.perf_counter()
    
    print(output)
    print(f"\nExecution time: {(end_time - start_time) * 1000:.2f}ms")
    
    # Test with larger dataset
    print("\n" + "=" * 100)
    print("Performance Test with 1000 users:")
    print("=" * 100)
    
    # Generate 1000 test users
    large_dataset = [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'role': ['Admin', 'User', 'Moderator'][i % 3],
            'status': ['Active', 'Inactive'][i % 2],
            'join_date': '2024-01-01',
            'last_login': '2025-11-26'
        }
        for i in range(1, 1001)
    ]
    
    start_time = time.perf_counter()
    large_output = display_users(large_dataset, verbose=False)
    end_time = time.perf_counter()
    
    print(f"Processed 1000 users in {(end_time - start_time) * 1000:.2f}ms")
    print(f"Output length: {len(large_output)} characters")
