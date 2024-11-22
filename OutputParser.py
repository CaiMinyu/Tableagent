import ast
def Queue_OutputParser(text):
    pattern1 = r'^\d+(-\d+)*\..+'
    try:
        import re
        # 按行分割字符串
        lines = text.split('\n')
        result = True
        new_list = list()
        label = list()
        for line in lines:
            if re.match(pattern1, line):
                new_list.append(line)
                if len(new_list) > 1:
                    label = line.split('.', 1)[0]
                    digits_now = re.findall(r'\d', label)
                    digits_now = ''.join(digits_now)
                    digits_last = re.findall(r'\d+', new_list[-1].split('.', 1)[0])
                    digits_last = ''.join(digits_last)
                    max_length = max(len(digits_now), len(digits_last))
                    digit_last = int(digits_last.ljust(max_length, '0'))
                    digit_now = int(digits_now.ljust(max_length, '0'))
                    if digit_now < digit_last:
                        return "Last conversation generate wrong output format"
        return new_list
    except:
        return "Last conversation generate wrong output format."

def DictParser(text):
    try:
        result = ast.literal_eval(text)
        if isinstance(result, dict):
            return result
    except (ValueError, SyntaxError):
        return False