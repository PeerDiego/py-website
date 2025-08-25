"""
Cookie Data Persistence Test
Tests the save/load functionality with browser cookies
"""

import time

def test_basic_save_load():
    """Test 1: Basic save and load functionality"""
    print("=== Test 1: Basic Save/Load ===")
    
    # Test data
    test_data = {
        "user_name": "TestUser",
        "score": 42,
        "level": 3,
        "completed_tasks": ["task1", "task2", "task3"]
    }
    
    print(f"Saving test data: {test_data}")
    save_data(test_data, "basic_test")
    
    print("Loading saved data...")
    loaded_data = load_data("basic_test")
    
    if loaded_data:
        print(f"Successfully loaded: {loaded_data}")
        print("☑️ Test 1 PASSED")
    else:
        print("❌ Test 1 FAILED - no data loaded")
    
    return loaded_data

def test_multiple_keys():
    """Test 2: Saving multiple different datasets with different keys"""
    print("\n=== Test 2: Multiple Keys ===")
    
    # Save different types of data with different keys
    user_prefs = {"theme": "dark", "language": "en", "notifications": True}
    game_stats = {"games_played": 15, "wins": 8, "losses": 7}
    app_settings = {"auto_save": True, "debug_mode": False, "version": "1.0"}
    
    print("Saving user preferences...")
    save_data(user_prefs, "user_preferences")
    
    print("Saving game statistics...")
    save_data(game_stats, "game_statistics")
    
    print("Saving app settings...")
    save_data(app_settings, "app_settings")
    
    # Load them back
    print("\nLoading all saved data...")
    loaded_prefs = load_data("user_preferences")
    loaded_stats = load_data("game_statistics")
    loaded_settings = load_data("app_settings")
    
    print(f"User preferences: {loaded_prefs}")
    print(f"Game statistics: {loaded_stats}")
    print(f"App settings: {loaded_settings}")
    
    # Verify all data was saved and loaded correctly
    if loaded_prefs and loaded_stats and loaded_settings:
        print("☑️ Test 2 PASSED")
    else:
        print("❌ Test 2 FAILED")
    
    return all((loaded_prefs, loaded_stats, loaded_settings))

def test_data_persistence():
    """Test 3: Data persists across 'sessions' (simulated with wait)"""
    print("\n=== Test 3: Data Persistence ===")

    session_id = "session_123"
    session_data = {
        "session_id": session_id,
        "start_time": "2025-08-04 10:30:00",
        "user_actions": ["login", "view_dashboard", "edit_profile"]
    }
    
    print("Saving session data...")
    save_data(session_data, "session_data")
    
    print("Simulating time passage (waiting 2 seconds)...")
    time.sleep(2)
    
    print("Loading session data after time passage...")
    loaded_session = load_data("session_data")
    
    if loaded_session and loaded_session.get("session_id") == session_id:
        print(f"Session data persisted: {loaded_session}")
        print("☑️ Test 3 PASSED")
    else:
        print("❌ Test 3 FAILED")
    
    return loaded_session

def test_data_modification():
    """Test 4: Modifying and re-saving data"""
    print("\n=== Test 4: Data Modification ===")
    
    # Start with initial data
    progress_data = {
        "current_level": 1,
        "experience": 0,
        "achievements": []
    }
    
    print(f"Initial data: {progress_data}")
    save_data(progress_data, "progress")
    
    # Simulate some progress
    print("Simulating game progress...")
    progress_data["current_level"] = 2
    progress_data["experience"] = 150
    progress_data["achievements"].append("First Level Complete")
    
    print(f"Updated data: {progress_data}")
    save_data(progress_data, "progress")
    
    # Load and verify the updates
    loaded_progress = load_data("progress")
    print(f"Loaded updated data: {loaded_progress}")
    
    if (loaded_progress and 
        loaded_progress.get("current_level") == 2 and 
        loaded_progress.get("experience") == 150 and
        "First Level Complete" in loaded_progress.get("achievements", [])):
        print("☑️ Test 4 PASSED")
    else:
        print("❌ Test 4 FAILED")
    
    return loaded_progress

def test_clear_data():
    """Test 5: Clearing specific data"""
    print("\n=== Test 5: Clear Data ===")
    
    # Save some temporary data
    temp_data = {"temp_value": "delete_me"}
    print(f"Saving temporary data: {temp_data}")
    save_data(temp_data, "temp_data")
    
    # Verify it was saved
    loaded_temp = load_data("temp_data")
    print(f"Loaded temporary data: {loaded_temp}")
    
    # Clear it
    print("Clearing temporary data...")
    clear_data("temp_data")
    
    # Try to load it again
    cleared_data = load_data("temp_data")
    print(f"Data after clearing: {cleared_data}")
    
    if cleared_data is None:
        print("☑️ Test 5 PASSED")
    else:
        print("❌ Test 5 FAILED - data still exists")
    
    return cleared_data

def test_default_key():
    """Test 6: Using the default key parameter"""
    print("\n=== Test 6: Default Key ===")
    
    default_data = {"using_default_key": True, "value": 999}
    
    print(f"Saving with default key: {default_data}")
    save_data(default_data)  # No key specified, should use 'app_data'
    
    print("Loading with default key...")
    loaded_default = load_data()  # No key specified, should load 'app_data'
    
    print(f"Loaded with default key: {loaded_default}")
    
    if loaded_default and loaded_default.get("using_default_key") == True:
        print("☑️ Test 6 PASSED")
    else:
        print("❌ Test 6 FAILED")
    
    return loaded_default

def run_all_tests():
    """Run all cookie persistence tests"""
    print("🍪 COOKIE DATA PERSISTENCE TESTS 🍪")
    print("=" * 50)
    
    # Check if the cookie functions are available
    try:
        # Test if the functions exist
        save_data
        load_data
        clear_data
        print("☑️ Cookie functions are available!")
    except NameError:
        print("❌ Cookie functions not available - make sure app.js is properly set up")
        return
    
    # Run all tests
    results = {}
    
    results['basic'] = test_basic_save_load()
    results['multiple'] = test_multiple_keys()
    results['persistence'] = test_data_persistence()
    results['modification'] = test_data_modification()
    results['clear'] = test_clear_data()
    results['default'] = test_default_key()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = 6
    
    if results['basic']: passed += 1
    if results['multiple']: passed += 1  # Check if first item loaded successfully
    if results['persistence']: passed += 1
    if results['modification']: passed += 1
    if results['clear'] is None: passed += 1  # None means it was cleared successfully
    if results['default']: passed += 1
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Cookie persistence is working correctly!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\nYou can now use save_data(), load_data(), and clear_data()")
    print("in your Python programs to persist data in browser cookies!")

# Run the tests
if __name__ == "__main__":
    run_all_tests()
else:
    # If imported, just run the tests
    run_all_tests()
