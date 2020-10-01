'''
A string is said to be palindrome if the reverse of the string is the same as string. For example, “madam” is a palindrome, but “abcd” is not a palindrome.
'''

def checkPalindrome(s):
    return "Palindrome" if s==s[::-1] else "Not Palindrome"

print(checkPalindrome("madam"))
print(checkPalindrome("abcd"))
