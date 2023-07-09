def isNoneOrEmpty(text: str) -> bool:
    return text == '' or text == None

if __name__ == "__main__":
    a = ""
    print(isNoneOrEmpty(a))
    a = None
    print(isNoneOrEmpty(a))
    a = "a"
    print(isNoneOrEmpty(a))