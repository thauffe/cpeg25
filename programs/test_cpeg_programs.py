import subprocess

def test_installation():

    # PyRate
    try:
        import PyRate
        print("PyRate found")
    except:
        print("PyRate not found")

    # R
    try:
        subprocess.run(["Rscript", "-e", "print(\"Rscript is working\")"])
    except:
        print("Rscript not working. Please check system path")

    # DeepDive
    try:
        import PyRate
        print("deepdive found")
    except:
        print("deepdive not found")

    # DeepDiveR
    try:
        subprocess.run(["Rscript", "-e", "if(requireNamespace(\"DeepDiveR\", quietly = TRUE)) {print(\"DeepDiveR R package installed\")}"])
    except:
        print("DeepDiveR for R not installed.")


if __name__ == "__main__":
    test_installation()
