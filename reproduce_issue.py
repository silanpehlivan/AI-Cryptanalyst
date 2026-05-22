import sys
import unittest
sys.path.append(r'.')  # Ensure current directory is in path

from solvers import solve_caesar

class TestDecryption(unittest.TestCase):
    def test_english_lowercase(self):
        # User example:
        # Cipher: Fberphevgl vf abg n cebqhpg, ohg n cebprff.
        # Expected: Cybersecurity is not a product, but a process.
        # Cipher: Fberphevgl vf abg n cebqhpg, ohg n cebprff.
        # Expected (User claim): Cybersecurity...
        # Actual (Math): Sorecurity...
        cipher = "Fberphevgl vf abg n cebqhpg, ohg n cebprff."
        # expected = "Cybersecurity is not a product, but a process."
        
        print("\n--- DEBUG START ---")
        result, info = solve_caesar(cipher)
        print(f"Decrypted: '{result}'")
        print(f"Info: '{info}'")
        print("--- DEBUG END ---")
        
        # We assert what the solver SHOULD find if working correctly mathematically
        self.assertIn("Sorecurity", result, f"Expected 'Sorecurity' in '{result}'")

    def test_turkish_chars(self):
        cipher = "Sìehu Jüyhqonm khu thpda jöf lshonmıvıu."
        print("\n--- DEBUG TURKISH START ---")
        result, info = solve_caesar(cipher)
        print(f"Decrypted: '{result}'")
        print(f"Info: '{info}'")
        print("--- DEBUG TURKISH END ---")

if __name__ == '__main__':
    unittest.main()
