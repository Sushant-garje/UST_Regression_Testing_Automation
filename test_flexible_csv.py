"""
Test script to demonstrate flexible CSV loading.
Tests the system with different CSV formats.
"""

import pandas as pd
from regression_manager.data_loader import DataLoader

def test_csv_format(csv_path):
    """Test loading and normalizing a CSV file."""
    print(f"\n{'='*80}")
    print(f"Testing: {csv_path}")
    print('='*80)
    
    try:
        # Load CSV
        loader = DataLoader(csv_path)
        df = loader.load_csv()
        
        print(f"\n✅ Loaded successfully!")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        
        # Normalize
        df_normalized = loader.normalize_data(df)
        
        print(f"\n✅ Normalized successfully!")
        print(f"   Standard columns: {list(df_normalized.columns)}")
        
        # Show sample
        print(f"\n📊 Sample data (first 3 rows):")
        print(df_normalized[['testcase_id', 'module_name', 'pass_fail', 'coverage', 'runtime_seconds']].head(3).to_string(index=False))
        
        # Show statistics
        print(f"\n📈 Statistics:")
        print(f"   Total tests: {len(df_normalized)}")
        print(f"   Pass rate: {df_normalized['pass_fail'].mean()*100:.1f}%")
        print(f"   Avg coverage: {df_normalized['coverage'].mean():.2f}%")
        print(f"   Avg runtime: {df_normalized['runtime_seconds'].mean():.2f}s")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    """Test multiple CSV formats."""
    print("\n" + "="*80)
    print("FLEXIBLE CSV LOADING TEST")
    print("="*80)
    
    # Test files
    test_files = [
        'rag_training_data.csv',
        '8bitadder.csv'
    ]
    
    results = {}
    for csv_file in test_files:
        results[csv_file] = test_csv_format(csv_file)
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print('='*80)
    
    for file, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {file}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All CSV formats handled successfully!")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")


if __name__ == '__main__':
    main()
