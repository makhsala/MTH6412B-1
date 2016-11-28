class Stack(object):

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __repr__(self):
        return repr(self.items)

def eval_postfix(expr):
    import re
    token_list = re.split("([^0-9.])", expr)
    stack = Stack()
    for token in token_list:
        if token == '' or token == ' ':
            continue
        if token == '+':
            sum = stack.pop() + stack.pop()
            stack.push(sum)
        elif token == '*':
            product = stack.pop() * stack.pop()
            stack.push(product)
        else:
            stack.push(float(token))
    return stack.pop()


evale = False
if evale :
    print eval_postfix (" 56.2 47.5 + 2 *")