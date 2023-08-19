def getResponse(prompt):
    return "Response: " + prompt

def main():
    prompt = "Your question here"
    result = getResponse(prompt)
    print(result)

if __name__ == "__main__":
    main()