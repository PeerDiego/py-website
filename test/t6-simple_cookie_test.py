"""
Simple Cookie Test
Basic test to troubleshoot save/load functionality
"""

def simple_cookie_test():
    """Very simple test to see what's happening with cookies"""
    print("🔧 SIMPLE COOKIE TEST - TROUBLESHOOTING 🔧")
    print("=" * 50)
    
    # Test 1: Check if functions exist
    print("Step 1: Checking if functions are available...")
    try:
        print(f"save_data function: {save_data}")
        print(f"load_data function: {load_data}")
        print(f"clear_data function: {clear_data}")
        print("✅ All functions are available!")
    except NameError as e:
        print(f"❌ Function not available: {e}")
        return
    
    # Test 2: Try saving a simple value
    print("\nStep 2: Testing save operation...")
    test_value = {"simple": "test", "number": 123}
    print(f"Saving: {test_value}")
    
    try:
        result = save_data(test_value, "simple_test")
        print(f"Save result: {result}")
        print("✅ Save operation completed")
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return
    
    # Test 3: Try loading the value
    print("\nStep 3: Testing load operation...")
    try:
        loaded_value = load_data("simple_test")
        print(f"Loaded value: {loaded_value}")
        print(f"Type of loaded value: {type(loaded_value)}")
        
        if loaded_value is None:
            print("❌ Load returned None")
        elif loaded_value:
            print("✅ Load returned something")
            
            # Test 4: Check if we can access the data
            print("\nStep 4: Testing data access...")
            try:
                if isinstance(loaded_value, dict):
                    simple_val = loaded_value.get('simple')
                    number_val = loaded_value.get('number')
                    print(f"Retrieved 'simple': {simple_val}")
                    print(f"Retrieved 'number': {number_val}")
                    if simple_val == "test" and number_val == 123:
                        print("✅ Data access successful - values match!")
                    else:
                        print("❌ Data values don't match expected")
                else:
                    print(f"❌ Loaded value is not a dict, it's: {type(loaded_value)}")
                    print(f"Available attributes: {dir(loaded_value)}")
            except Exception as e:
                print(f"❌ Data access failed: {e}")
        else:
            print("❌ Load returned falsy value")
            
    except Exception as e:
        print(f"❌ Load failed: {e}")
    
    # Test 5: Test raw JavaScript functions to see the difference
    print("\nStep 5: Testing raw JavaScript functions...")
    try:
        print("Testing js_save_data...")
        js_result = js_save_data({"raw": "test"}, "raw_test")
        print(f"js_save_data result: {js_result}")
        
        print("Testing js_load_data...")
        js_loaded = js_load_data("raw_test")
        print(f"js_load_data result: {js_loaded}")
        print(f"Type: {type(js_loaded)}")
        
        # Test manual conversion
        print("Testing manual .to_py() conversion...")
        if hasattr(js_loaded, 'to_py'):
            converted = js_loaded.to_py()
            print(f"Converted result: {converted}")
            print(f"Converted type: {type(converted)}")
        else:
            print("No .to_py() method available")
        
    except Exception as e:
        print(f"❌ Raw JS functions failed: {e}")

# Run the simple test
simple_cookie_test()
