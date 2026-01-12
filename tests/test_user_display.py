"""Comprehensive tests for optimized user display functions."""

import time
import logging
import pytest
from typing import List, Dict, Any

# Import functions to test
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string
)


class TestDisplayUsers:
    """Test suite for display_users function."""
    
    def test_display_users_basic(self, sample_users):
        """Test basic functionality with sample users."""
        result = display_users(sample_users)
        
        assert result is not None
        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "Bob Johnson" in result
        assert "[INFO] Processed 3 users" in result
    
    def test_display_users_empty_list(self, empty_users):
        """Test handling of empty user list."""
        result = display_users(empty_users)
        assert result == ""
    
    def test_display_users_missing_keys(self, users_with_missing_keys):
        """Test handling of users with missing keys."""
        result = display_users(users_with_missing_keys)
        
        # Should handle gracefully with N/A values
        assert "N/A" in result
        assert result is not None
    
    def test_display_users_no_summary(self, sample_users):
        """Test display without summary information."""
        result = display_users(sample_users, show_all=False)
        
        assert "[INFO] Processed" not in result
        assert "John Doe" in result
    
    def test_display_users_verbose_logging(self, sample_users, caplog):
        """Test verbose logging functionality."""
        with caplog.at_level(logging.INFO):
            display_users(sample_users, verbose=True)
        
        # Check for logging markers
        assert any("[MARKER]" in record.message for record in caplog.records)
    
    def test_display_users_performance_100(self, large_user_dataset_100):
        """Test performance with 100 users (target: <50ms)."""
        start_time = time.perf_counter()
        result = display_users(large_user_dataset_100, verbose=False)
        end_time = time.perf_counter()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        assert result is not None
        assert execution_time_ms < 50, f"Execution took {execution_time_ms:.2f}ms, target is <50ms"
        assert "[INFO] Processed 100 users" in result
    
    def test_display_users_performance_1000(self, large_user_dataset_1000):
        """Test performance with 1000 users (target: <100ms)."""
        start_time = time.perf_counter()
        result = display_users(large_user_dataset_1000, verbose=False)
        end_time = time.perf_counter()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        assert result is not None
        assert execution_time_ms < 100, f"Execution took {execution_time_ms:.2f}ms, target is <100ms"
        assert "[INFO] Processed 1000 users" in result
    
    def test_display_users_logging_markers(self, sample_users, caplog):
        """Test that logging includes proper markers."""
        with caplog.at_level(logging.INFO):
            display_users(sample_users)
        
        marker_messages = [record.message for record in caplog.records if "[MARKER]" in record.message]
        assert len(marker_messages) > 0


class TestGetUserById:
    """Test suite for get_user_by_id function."""
    
    def test_get_user_by_id_found(self, sample_users):
        """Test finding existing user by ID."""
        user = get_user_by_id(sample_users, 2)
        
        assert user is not None
        assert user['id'] == 2
        assert user['name'] == 'Jane Smith'
    
    def test_get_user_by_id_not_found(self, sample_users):
        """Test searching for non-existent user ID."""
        user = get_user_by_id(sample_users, 999)
        
        assert user is None
    
    def test_get_user_by_id_empty_list(self, empty_users):
        """Test searching in empty user list."""
        user = get_user_by_id(empty_users, 1)
        
        assert user is None
    
    def test_get_user_by_id_missing_id_field(self, users_with_missing_keys):
        """Test with users missing ID field."""
        user = get_user_by_id(users_with_missing_keys, 1)
        
        assert user is not None
        assert user['id'] == 1
    
    def test_get_user_by_id_performance(self, large_user_dataset_1000):
        """Test O(1) lookup performance (target: <1ms per lookup)."""
        # Warm-up
        get_user_by_id(large_user_dataset_1000, 500)
        
        # Test multiple lookups
        start_time = time.perf_counter()
        for _ in range(10):
            user = get_user_by_id(large_user_dataset_1000, 500)
        end_time = time.perf_counter()
        
        avg_time_ms = ((end_time - start_time) / 10) * 1000
        
        assert user is not None
        assert avg_time_ms < 1, f"Average lookup took {avg_time_ms:.2f}ms, target is <1ms"
    
    def test_get_user_by_id_logging(self, sample_users, caplog):
        """Test that function logs with markers."""
        with caplog.at_level(logging.INFO):
            get_user_by_id(sample_users, 1)
        
        assert any("[MARKER]" in record.message for record in caplog.records)


class TestFilterUsers:
    """Test suite for filter_users function."""
    
    def test_filter_users_by_role(self, sample_users):
        """Test filtering by role."""
        filtered = filter_users(sample_users, {'role': 'User'})
        
        assert len(filtered) == 1
        assert filtered[0]['name'] == 'Jane Smith'
    
    def test_filter_users_by_status(self, sample_users):
        """Test filtering by status."""
        filtered = filter_users(sample_users, {'status': 'Active'})
        
        assert len(filtered) == 2
        assert all(user['status'] == 'Active' for user in filtered)
    
    def test_filter_users_by_name(self, sample_users):
        """Test filtering by name (case-insensitive)."""
        filtered = filter_users(sample_users, {'name': 'john'})
        
        assert len(filtered) == 2  # John Doe and Bob Johnson
        assert any('John' in user['name'] for user in filtered)
    
    def test_filter_users_multiple_criteria(self, sample_users):
        """Test filtering with multiple criteria."""
        filtered = filter_users(sample_users, {'role': 'User', 'status': 'Inactive'})
        
        assert len(filtered) == 1
        assert filtered[0]['name'] == 'Jane Smith'
    
    def test_filter_users_no_matches(self, sample_users):
        """Test filtering with criteria that match nothing."""
        filtered = filter_users(sample_users, {'role': 'SuperAdmin'})
        
        assert len(filtered) == 0
    
    def test_filter_users_empty_list(self, empty_users):
        """Test filtering empty user list."""
        filtered = filter_users(empty_users, {'role': 'Admin'})
        
        assert len(filtered) == 0
    
    def test_filter_users_empty_criteria(self, sample_users):
        """Test filtering with no criteria (should return all)."""
        filtered = filter_users(sample_users, {})
        
        assert len(filtered) == len(sample_users)
    
    def test_filter_users_performance_100(self, large_user_dataset_100):
        """Test filter performance with 100 users (target: <10ms)."""
        start_time = time.perf_counter()
        filtered = filter_users(large_user_dataset_100, {'role': 'Admin', 'status': 'Active'})
        end_time = time.perf_counter()
        
        execution_time_ms = (end_time - start_time) * 1000
        
        assert len(filtered) > 0
        assert execution_time_ms < 10, f"Execution took {execution_time_ms:.2f}ms, target is <10ms"
    
    def test_filter_users_logging(self, sample_users, caplog):
        """Test that function logs with markers."""
        with caplog.at_level(logging.INFO):
            filter_users(sample_users, {'role': 'Admin'})
        
        assert any("[MARKER]" in record.message for record in caplog.records)


class TestExportUsersToString:
    """Test suite for export_users_to_string function."""
    
    def test_export_users_basic(self, sample_users):
        """Test basic export functionality."""
        result = export_users_to_string(sample_users)
        
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "Bob Johnson" in result
    
    def test_export_users_format(self, sample_users):
        """Test export format structure."""
        result = export_users_to_string(sample_users)
        
        # Check for proper formatting
        assert "User ID:" in result
        assert "Name:" in result
        assert "Email:" in result
        assert "Role:" in result
        assert "Status:" in result
        assert "=" * 100 in result
        assert "-" * 100 in result
    
    def test_export_users_empty_list(self, empty_users):
        """Test exporting empty user list."""
        result = export_users_to_string(empty_users)
        
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
    
    def test_export_users_missing_keys(self, users_with_missing_keys):
        """Test export with users having missing keys."""
        result = export_users_to_string(users_with_missing_keys)
        
        # Should handle gracefully with N/A values
        assert "N/A" in result
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result
    
    def test_export_users_logging(self, sample_users, caplog):
        """Test that function logs with markers."""
        with caplog.at_level(logging.INFO):
            export_users_to_string(sample_users)
        
        assert any("[MARKER]" in record.message for record in caplog.records)


class TestErrorHandling:
    """Test suite for error handling across all functions."""
    
    def test_display_users_handles_exceptions(self, caplog):
        """Test that display_users handles exceptions gracefully."""
        # Invalid input
        with caplog.at_level(logging.ERROR):
            result = display_users([{'id': 1, 'name': None}])
        
        # Should not crash, should return something
        assert result is not None
    
    def test_display_users_exception_in_loop(self, caplog):
        """Test that display_users handles exception in processing loop."""
        # Create a problematic user that might cause issues
        class BadDict(dict):
            def get(self, key, default=None):
                if key == 'name':
                    raise ValueError("Test exception")
                return super().get(key, default)
        
        bad_user = BadDict({'id': 999})
        with caplog.at_level(logging.ERROR):
            result = display_users([bad_user])
        
        # Should continue processing despite error
        assert result is not None
    
    def test_get_user_by_id_handles_exceptions(self):
        """Test that get_user_by_id handles exceptions gracefully."""
        # Should not crash with malformed data
        result = get_user_by_id([{'invalid': 'data'}], 1)
        assert result is None
    
    def test_get_user_by_id_exception_in_indexing(self, caplog):
        """Test that get_user_by_id handles exception during indexing."""
        # Create problematic data
        class BadDict(dict):
            def get(self, key, default=None):
                raise RuntimeError("Test error")
        
        with caplog.at_level(logging.ERROR):
            result = get_user_by_id([BadDict()], 1)
        
        assert result is None
    
    def test_filter_users_handles_exceptions(self):
        """Test that filter_users handles exceptions gracefully."""
        # Should not crash with malformed data
        result = filter_users([{'id': 1}], {'role': 'Admin'})
        assert isinstance(result, list)
    
    def test_filter_users_exception_in_filter(self, caplog):
        """Test that filter_users handles exception during filtering."""
        # Create data that causes exception
        class BadDict(dict):
            def get(self, key, default=None):
                raise TypeError("Test error")
        
        with caplog.at_level(logging.ERROR):
            result = filter_users([BadDict()], {'role': 'Admin'})
        
        assert isinstance(result, list)
    
    def test_export_users_handles_exceptions(self, caplog):
        """Test that export_users_to_string handles exceptions gracefully."""
        # Invalid input
        with caplog.at_level(logging.ERROR):
            result = export_users_to_string([{'id': 1, 'name': None}])
        
        # Should not crash
        assert result is not None
        assert "USER_EXPORT_START" in result
    
    def test_export_users_exception_in_loop(self, caplog):
        """Test that export_users_to_string handles exception in loop."""
        class BadDict(dict):
            def get(self, key, default=None):
                if key == 'email':
                    raise ValueError("Test exception")
                return super().get(key, default)
        
        bad_user = BadDict({'id': 999, 'name': 'Test'})
        with caplog.at_level(logging.ERROR):
            result = export_users_to_string([bad_user])
        
        assert "USER_EXPORT_START" in result
        assert "USER_EXPORT_END" in result


class TestLoggingMarkers:
    """Test suite for logging marker presence."""
    
    def test_all_functions_use_markers(self, sample_users, caplog):
        """Test that all functions use [MARKER] in their logs."""
        with caplog.at_level(logging.INFO):
            display_users(sample_users)
            get_user_by_id(sample_users, 1)
            filter_users(sample_users, {'role': 'Admin'})
            export_users_to_string(sample_users)
        
        marker_count = sum(1 for record in caplog.records if "[MARKER]" in record.message)
        assert marker_count > 0, "No logging markers found"


# Performance summary test
def test_performance_summary(large_user_dataset_100, large_user_dataset_1000):
    """Summary performance test with all operations."""
    print("\n" + "=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    
    # Display 100 users
    start = time.perf_counter()
    display_users(large_user_dataset_100, verbose=False)
    time_100 = (time.perf_counter() - start) * 1000
    print(f"Display 100 users: {time_100:.2f}ms (target: <50ms)")
    
    # Display 1000 users
    start = time.perf_counter()
    display_users(large_user_dataset_1000, verbose=False)
    time_1000 = (time.perf_counter() - start) * 1000
    print(f"Display 1000 users: {time_1000:.2f}ms (target: <100ms)")
    
    # Filter 100 users
    start = time.perf_counter()
    filter_users(large_user_dataset_100, {'role': 'Admin', 'status': 'Active'})
    time_filter = (time.perf_counter() - start) * 1000
    print(f"Filter 100 users: {time_filter:.2f}ms (target: <10ms)")
    
    # Get user by ID
    start = time.perf_counter()
    get_user_by_id(large_user_dataset_1000, 500)
    time_get = (time.perf_counter() - start) * 1000
    print(f"Get user by ID: {time_get:.2f}ms (target: <1ms)")
    
    print("=" * 80)
    
    assert time_100 < 50
    assert time_1000 < 100
    assert time_filter < 10
    assert time_get < 1
