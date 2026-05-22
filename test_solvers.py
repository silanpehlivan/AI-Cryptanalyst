from solvers import solve_caesar, solve_vigenere, solve_base64, solve_xor
import base64

def test_solvers():
    print("Testing Solvers...")
    
    # 1. Caesar Test
    # "HELLO" (shift 1) -> "IFMMP"
    res, info = solve_caesar("IFMMP")
    print(f"Caesar Test: Predicted: {res} ({info}) - Expected: HELLO")
    
    # 2. Base64 Test
    # "Hello World" -> "SGVsbG8gV29ybGQ="
    res, info = solve_base64("SGVsbG8gV29ybGQ=")
    print(f"Base64 Test: Predicted: {res} ({info}) - Expected: Hello World")
    
    # 3. XOR Test
    # "A" (0x41) ^ ' ' (0x20) -> 'a' (0x61) ... wait, Space is 0x20. 
    # Let's use a clear hex example. 
    # 'Cat' (43 61 74) ^ 0x01 -> 42 60 75 ('B`u')
    # Let's use the function's own logic reversed or a known hex.
    # Text: "TEST" (54 45 53 54) ^ Key 'A' (0x41)
    # T(54)^A(41) = 15
    # E(45)^A(41) = 04
    # S(53)^A(41) = 12
    # T(54)^A(41) = 15
    # Hex: 15041215
    res, info = solve_xor("15041215") 
    print(f"XOR Test: Predicted: {res} ({info}) - Expected: TEST")
    
    # 4. Vigenere Test
    # "HELLO" key "ABC" (0, 1, 2)
    # H+0=H, E+1=F, L+2=N, L+0=L, O+1=P -> "HFNLP"
    res, info = solve_vigenere("HFNLP")
    print(f"Vigenere Test: Predicted: {res} ({info}) - Expected: HELLO")
    
    # Complex Vigenere
    # "THEQUICKBROWNFOX" key "KEY"
    # Plain: THEQUICKBROWNFOX
    # Key:   KEYKEYKEYKEYKEYK
    # Cipher: DLC...
    # Let's use a known pair just to trust the logic
    # Plain: "ATTACKATDAWN" Key: "LEMON" -> "LXFOPVEFRNHR"
    res, info = solve_vigenere("LXFOPVEFRNHR")
    print(f"Vigenere Complex: Predicted: {res} ({info}) - Expected: ATTACKATDAWN")

if __name__ == "__main__":
    test_solvers()
