def getResponse(input_string):
    return "Response: " + input_string

def main():
    input_string = "Your question here"
    result = getResponse(input_string)
    print(result)

if __name__ == "__main__":
    main()