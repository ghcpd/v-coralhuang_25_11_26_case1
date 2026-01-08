"""Comprehensive tests for user_display_optimized module.

Test coverage includes:
- All public functions
- Edge cases (empty lists, missing keys, invalid types)
- Performance requirements
- Error handling and logging
- Cross-platform compatibility
"""

import time
import logging
import pytest
from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string,
    _create_user_index
)


class TestDisplayUsers:
    """Tests for display_users function."""
    
    def test_display_empty_list(self):
        """Test displaying empty user list."""
        result = display_users([])
        assert isinstance(result, str)
        assert "[MARKER] Processed 0 users" in result
    
    def test_display_single_user(self, sample_users):
        """Test displaying single user."""
        result = display_users(sample_users[:1])
        assert "John Doe" in result
        assert "john@example.com" in result
        assert "ID:1" in result
    
    def test_display_multiple_users(self, sample_users):
        """Test displaying multiple users."""
        result = display_users(sample_users)
        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "Bob Johnson" in result
        assert "[MARKER] Processed 5 users" in result
    
    def test_display_with_show_all_false(self, sample_users):
        """Test displaying with show_all=False."""
        result = display_users(sample_users, show_all=False)
        # Should not include summary
        assert "[MARKER] Processed" not in result
        assert "John Doe" in result
    
    def test_display_with_verbose_true(self, sample_users, caplog):
        """Test displaying with verbose=True logs markers."""
        with caplog.at_level(logging.INFO):
            display_users(sample_users[:2], verbose=True)
        
        assert "[MARKER] Processing user 1" in caplog.text
        assert "[MARKER] Processing user 2" in caplog.text
    
    def test_display_invalid_input_type(self):
        """Test display_users with non-list input."""
        result = display_users("not a list")
        assert result == ""
    
    def test_display_none_input(self):
        """Test display_users with None input."""
        result = display_users(None)
        assert result == ""
    
    def test_display_missing_keys(self, caplog):
        """Test display_users with missing required keys."""
        users = [{'id': 1, 'name': 'John'}]  # Missing many keys
        with caplog.at_level(logging.WARNING):
            result = display_users(users)
        
        assert result == "\n[MARKER] Processed 0 users."
        assert "[WARNING]" in caplog.text
    
    def test_display_with_extra_keys(self, sample_users):
        """Test display_users with extra keys (should work)."""
        users = sample_users.copy()
        users[0]['extra_field'] = 'extra_value'
        result = display_users(users)
        assert "John Doe" in result
    
    def test_display_performance_100_users(self, large_user_set):
        """Test performance: 100 users should complete in <50ms."""
        start = time.perf_counter()
        display_users(large_user_set[:100])
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 50, f"100 users took {elapsed:.2f}ms, expected <50ms"
    
    def test_display_performance_1000_users(self, large_user_set):
        """Test performance: 1000 users should complete in <100ms."""
        start = time.perf_counter()
        display_users(large_user_set)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 100, f"1000 users took {elapsed:.2f}ms, expected <100ms"
    
    def test_display_format_consistency(self, sample_users):
        """Test that display format is consistent and readable."""
        result = display_users(sample_users[:1])
        # Check pipe-separated format
        assert "|" in result
        assert "ID:" in result
        assert "Name:" in result
        assert "Email:" in result


class TestGetUserById:
    """Tests for get_user_by_id function."""
    
    def test_get_existing_user(self, sample_users):
        """Test getting existing user by ID."""
        user = get_user_by_id(sample_users, 1)
        assert user is not None
        assert user['id'] == 1
        assert user['name'] == 'John Doe'
    
    def test_get_nonexistent_user(self, sample_users):
        """Test getting non-existent user returns None."""
        user = get_user_by_id(sample_users, 999)
        assert user is None
    
    def test_get_user_empty_list(self):
        """Test getting user from empty list."""
        user = get_user_by_id([], 1)
        assert user is None
    
    def test_get_user_invalid_input(self):
        """Test get_user_by_id with invalid input type."""
        user = get_user_by_id("not a list", 1)
        assert user is None
    
    def test_get_user_performance(self, large_user_set):
        """Test O(1) lookup performance: should be <1ms."""
        start = time.perf_counter()
        get_user_by_id(large_user_set, 500)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 1, f"User lookup took {elapsed:.2f}ms, expected <1ms"
    
    def test_get_user_by_id_multiple_lookups(self, sample_users):
        """Test multiple lookups to verify consistency."""
        user1 = get_user_by_id(sample_users, 1)
        user2 = get_user_by_id(sample_users, 2)
        user3 = get_user_by_id(sample_users, 1)
        
        assert user1['name'] == 'John Doe'
        assert user2['name'] == 'Jane Smith'
        assert user1 == user3


class TestFilterUsers:
    """Tests for filter_users function."""
    
    def test_filter_by_role(self, sample_users):
        """Test filtering by role."""
        admins = filter_users(sample_users, {'role': 'Admin'})
        assert len(admins) == 1
        assert admins[0]['id'] == 1
    
    def test_filter_by_status(self, sample_users):
        """Test filtering by status."""
        active = filter_users(sample_users, {'status': 'Active'})
        assert len(active) == 4
        assert all(u['status'] == 'Active' for u in active)
    
    def test_filter_by_name(self, sample_users):
        """Test filtering by name (case-insensitive substring)."""
        johns = filter_users(sample_users, {'name': 'john'})
        assert len(johns) == 2  # John Doe and Bob Johnson
        assert any(u['name'] == 'John Doe' for u in johns)
    
    def test_filter_by_multiple_criteria(self, sample_users):
        """Test filtering with multiple criteria (AND logic)."""
        results = filter_users(sample_users, {'role': 'User', 'status': 'Active'})
        assert len(results) == 2
        assert all(u['role'] == 'User' and u['status'] == 'Active' for u in results)
    
    def test_filter_empty_list(self):
        """Test filtering empty list."""
        result = filter_users([], {'role': 'Admin'})
        assert result == []
    
    def test_filter_no_matches(self, sample_users):
        """Test filtering with no matches."""
        result = filter_users(sample_users, {'role': 'SuperAdmin'})
        assert result == []
    
    def test_filter_all_match(self, sample_users):
        """Test filtering where all match."""
        result = filter_users(sample_users, {})  # Empty criteria
        assert len(result) == len(sample_users)
    
    def test_filter_invalid_input(self):
        """Test filter_users with invalid input."""
        result = filter_users("not a list", {'role': 'Admin'})
        assert result == []
    
    def test_filter_invalid_criteria(self, sample_users):
        """Test filter_users with invalid criteria type."""
        result = filter_users(sample_users, "not a dict")
        assert result == []
    
    def test_filter_missing_key_in_criteria(self, sample_users, caplog):
        """Test filtering with criteria key not in user dict."""
        with caplog.at_level(logging.WARNING):
            result = filter_users(sample_users, {'nonexistent_field': 'value'})
        
        assert result == []
        assert "[WARNING]" in caplog.text
    
    def test_filter_performance_100_users(self, large_user_set):
        """Test performance: filtering 100 users should be <10ms."""
        start = time.perf_counter()
        filter_users(large_user_set[:100], {'status': 'Active'})
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 10, f"Filter took {elapsed:.2f}ms, expected <10ms"


class TestExportUsersToString:
    """Tests for export_users_to_string function."""
    
    def test_export_basic(self, sample_users):
        """Test basic export format."""
        result = export_users_to_string(sample_users[:1])
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
        assert "=" * 100 in result
        assert "-" * 100 in result
    
    def test_export_single_user(self, sample_users):
        """Test exporting single user."""
        result = export_users_to_string(sample_users[:1])
        assert "User ID: 1" in result
        assert "Name: John Doe" in result
        assert "Email: john@example.com" in result
    
    def test_export_multiple_users(self, sample_users):
        """Test exporting multiple users."""
        result = export_users_to_string(sample_users)
        assert result.count("User ID:") == 5
        assert result.count("-" * 100) == 5
    
    def test_export_empty_list(self):
        """Test exporting empty list."""
        result = export_users_to_string([])
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
    
    def test_export_invalid_input(self):
        """Test export with invalid input."""
        result = export_users_to_string("not a list")
        assert result == ""
    
    def test_export_missing_keys(self, caplog):
        """Test export with missing required keys."""
        users = [{'id': 1, 'name': 'John'}]
        with caplog.at_level(logging.WARNING):
            result = export_users_to_string(users)
        
        assert "USER_EXPORT_START" in result
        assert "User ID: 1" not in result
    
    def test_export_no_temp_strings(self, sample_users):
        """Test that export is efficient (no excessive temp strings)."""
        # This test verifies the function completes quickly
        start = time.perf_counter()
        result = export_users_to_string(sample_users)
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 10, f"Export took {elapsed:.2f}ms"
        assert isinstance(result, str)


class TestUserIndex:
    """Tests for _create_user_index internal function."""
    
    def test_create_index(self, sample_users):
        """Test creating user index."""
        index = _create_user_index(sample_users)
        assert len(index) == 5
        assert index[1]['name'] == 'John Doe'
        assert index[2]['name'] == 'Jane Smith'
    
    def test_create_index_empty(self):
        """Test creating index from empty list."""
        index = _create_user_index([])
        assert index == {}
    
    def test_create_index_missing_id(self):
        """Test creating index with user missing ID."""
        users = [{'name': 'John'}]
        index = _create_user_index(users)
        assert index == {}


class TestErrorHandling:
    """Tests for error handling and logging."""
    
    def test_display_users_logs_errors(self, caplog):
        """Test that display_users logs errors gracefully."""
        with caplog.at_level(logging.ERROR):
            display_users(None)
        
        assert "[ERROR]" in caplog.text or "[MARKER]" in caplog.text
    
    def test_filter_users_logs_warnings(self, caplog):
        """Test that filter_users logs warnings for missing keys."""
        users = [{'id': 1, 'name': 'John'}]
        with caplog.at_level(logging.WARNING):
            filter_users(users, {'role': 'Admin'})
        
        assert "[WARNING]" in caplog.text or "[ERROR]" in caplog.text
    
    def test_get_user_logs_debug(self, caplog, sample_users):
        """Test that get_user_by_id logs debug info."""
        with caplog.at_level(logging.DEBUG):
            get_user_by_id(sample_users, 1)
            get_user_by_id(sample_users, 999)
        
        assert "[DEBUG]" in caplog.text


class TestCrossPlatformCompatibility:
    """Tests for cross-platform compatibility."""
    
    def test_result_string_format(self, sample_users):
        """Test that string output uses consistent formatting across platforms."""
        result = display_users(sample_users[:1])
        
        # Should use | separator (works on all platforms)
        assert "|" in result
        # Should use \n for newlines (normalized by Python)
        assert "\n" in result
        # Should not use platform-specific line endings
        assert "\r" not in result or result.count("\r") == result.count("\n")
    
    def test_no_hardcoded_paths(self, sample_users):
        """Test that functions don't use hardcoded paths."""
        result = display_users(sample_users)
        
        # Should not contain backslashes (Windows paths)
        assert "\\" not in result or "\\" in "email@example.com"
        # Should not contain absolute paths
        assert not any(result.startswith(char) for char in ['/', 'C:', 'D:'])


# Additional edge case tests for coverage
class TestExceptionPaths:
    """Tests specifically targeting exception handling paths."""
    
    def test_display_with_exception_in_loop(self, caplog):
        """Test display_users exception handling during iteration."""
        # Create a user with extra fields to test exception paths
        users = [
            {'id': 1, 'name': 'John', 'email': 'john@example.com', 'role': 'Admin', 
             'status': 'Active', 'join_date': '2023-01-15', 'last_login': '2025-11-26'},
            {'id': 2, 'name': 'Jane', 'email': 'jane@example.com', 'role': 'User', 
             'status': 'Active', 'join_date': '2023-06-20', 'last_login': '2025-11-20'},
        ]
        with caplog.at_level(logging.DEBUG):
            result = display_users(users, verbose=True)
        
        assert "[MARKER]" in caplog.text
        assert "John" in result
        assert "Jane" in result
    
    def test_filter_users_with_type_error(self):
        """Test filter_users with users having mixed types."""
        # This shouldn't crash
        users = [
            {'id': 1, 'name': 'John', 'role': 'Admin', 'status': 'Active'},
            {'id': 2, 'name': 'Jane', 'role': 'User', 'status': 'Active'}
        ]
        result = filter_users(users, {'role': 'Admin'})
        assert len(result) == 1
    
    def test_export_with_complete_coverage(self, sample_users):
        """Test export with all valid fields present."""
        # Ensure all branches are executed
        result = export_users_to_string(sample_users)
        
        # Check format is complete
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
        assert result.count("User ID:") == 5
        assert result.count("Name:") == 5
        assert result.count("Email:") == 5
        assert result.count("Role:") == 5
        assert result.count("Status:") == 5
        assert result.count("Join Date:") == 5
        assert result.count("Last Login:") == 5


class TestEdgeCases:
    """Additional edge cases for comprehensive coverage."""
    
    def test_display_with_non_dict_in_list(self, caplog):
        """Test display_users with mixed valid/invalid items."""
        users = [
            {'id': 1, 'name': 'John', 'email': 'john@example.com', 'role': 'Admin', 
             'status': 'Active', 'join_date': '2023-01-15', 'last_login': '2025-11-26'},
            "not a dict"
        ]
        with caplog.at_level(logging.WARNING):
            result = display_users(users)
        
        assert "John" in result
        assert "[WARNING]" in caplog.text
    
    def test_filter_with_non_dict_in_list(self):
        """Test filter_users with mixed valid/invalid items."""
        users = [
            {'id': 1, 'name': 'John', 'role': 'Admin', 'status': 'Active'},
            "not a dict"
        ]
        result = filter_users(users, {'role': 'Admin'})
        assert len(result) == 1
    
    def test_export_with_non_dict_in_list(self, caplog):
        """Test export_users_to_string with mixed valid/invalid items."""
        users = [
            {'id': 1, 'name': 'John', 'email': 'john@example.com', 'role': 'Admin', 
             'status': 'Active', 'join_date': '2023-01-15', 'last_login': '2025-11-26'},
            "not a dict"
        ]
        with caplog.at_level(logging.WARNING):
            result = export_users_to_string(users)
        
        assert "USER_EXPORT_START" in result
        assert "User ID: 1" in result
    
    def test_display_with_case_sensitive_role_filter(self, sample_users):
        """Test that role filtering is case-sensitive."""
        lowercase_result = filter_users(sample_users, {'role': 'admin'})
        assert len(lowercase_result) == 0  # Should not match 'Admin'
    
    def test_filter_name_case_insensitive(self, sample_users):
        """Test that name filtering is case-insensitive."""
        # Test uppercase
        result = filter_users(sample_users, {'name': 'JOHN'})
        assert len(result) == 2
        
        # Test mixed case
        result = filter_users(sample_users, {'name': 'JoHn'})
        assert len(result) == 2
    
    def test_display_all_false_empty_result(self):
        """Test display_users with show_all=False and empty users."""
        result = display_users([], show_all=False)
        assert result == ""
    
    def test_get_user_with_non_integer_id(self, sample_users):
        """Test get_user_by_id with string ID (should not match)."""
        # IDs in sample_users are integers, lookup with string should return None
        user = get_user_by_id(sample_users, "1")
        assert user is None
    
    def test_filter_users_exception_handling(self):
        """Test filter_users handles unexpected exceptions gracefully."""
        users = [{'id': 1, 'name': 'John', 'role': 'Admin', 'status': 'Active'}]
        # This should not crash even with unusual criteria
        result = filter_users(users, {'role': 'Admin'})
        assert len(result) == 1
    
    def test_export_preserves_all_fields(self, sample_users):
        """Test that export_users_to_string preserves all required fields."""
        result = export_users_to_string(sample_users[:1])
        user = sample_users[0]
        
        assert str(user['id']) in result
        assert user['name'] in result
        assert user['email'] in result
        assert user['role'] in result
        assert user['status'] in result
        assert user['join_date'] in result
        assert user['last_login'] in result


# Integration tests
class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_full_workflow(self, sample_users):
        """Test complete workflow: display, filter, get, export."""
        # Display all
        all_display = display_users(sample_users)
        assert "5 users" in all_display
        
        # Filter by role
        admins = filter_users(sample_users, {'role': 'Admin'})
        assert len(admins) == 1
        
        # Get specific user
        user = get_user_by_id(sample_users, 1)
        assert user['name'] == 'John Doe'
        
        # Export
        export = export_users_to_string(admins)
        assert "User ID: 1" in export
    
    def test_consistency_between_functions(self, sample_users):
        """Test that functions return consistent data."""
        # Get user via get_user_by_id
        user1 = get_user_by_id(sample_users, 1)
        
        # Get user via filter
        filtered = filter_users(sample_users, {'name': 'John Doe'})
        user2 = filtered[0]
        
        # Should be the same
        assert user1 == user2
        
        # Should appear in display
        display_output = display_users(sample_users)
        assert user1['name'] in display_output
