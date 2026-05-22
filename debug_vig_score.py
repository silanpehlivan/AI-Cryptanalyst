import sys
sys.path.append(r'.')
from solvers import score_text

def test_scores():
    candidate_bad = "Ties e seni arii!"
    candidate_good = "Keep a code safe!"
    
    print(f"--- Debugging Scores ---")
    
    score_bad = score_text(candidate_bad)
    score_good = score_text(candidate_good)
    
    print(f"Bad Candidate ('{candidate_bad}'): {score_bad}")
    print(f"Good Candidate ('{candidate_good}'): {score_good}")
    
    if score_good < score_bad:
        print("PASS: Good candidate has lower (better) score.")
    else:
        print("FAIL: Good candidate has higher (worse) score.")
        print("Need to adjust scoring to favor the good candidate.")

if __name__ == "__main__":
    test_scores()
