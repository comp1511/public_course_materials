#!/usr/bin/env python3.5

import difflib
from  termcolor import colored as termcolor_colored
from  collections import defaultdict

def explain_output_differences(name, expected, canonical_expected, canonical_expected_plus_newlines, actual, canonical_actual, canonical_actual_plus_newlines, show_expected=True, show_actual=True, show_diff=True, max_lines_shown=32, max_line_length_shown=1024, colorize=False, debug=False, **extra_kwargs):
    colored = termcolor_colored if colorize else lambda x,*a,**kw: x
    if canonical_expected and not actual:
        return colored("Your program produced no output\n", 'red')
    if debug: print("explain_output_differences(%s, '%s', '%s')" % (name, expected, actual))

    # check if output is correct but just missing a character
    # but don't use this for short outputs
    if canonical_expected[0:-1] == canonical_actual and (len(canonical_actual) > 8 or (canonical_actual and canonical_actual[-1] in ". \n")):
        missing_char = colored(repr(canonical_expected[-1]), 'red')
        return "Your program's %s was correct except it was missing a %s character on the end.\n" % (name, missing_char)

    # check if output is correct but has an extra character
    # but don't use this for short outputs
    if canonical_actual[0:-1] == canonical_expected and (len(canonical_actual) > 8 or (canonical_actual and canonical_actual[-1] in ". \n")):
        extra_char = colored(repr(canonical_actual[-1]), 'red')
        suffix = ''
        if '\ufffd' == canonical_actual[-1]:
            extra_char = colored("\'\\xff'", 'red')
            suffix = 'This can result from printing the EOF value returned by getchar.\n'
        return "Your program's %s was correct except it had an extra %s character on the end.\n%s" % (name, extra_char,suffix)
    actual_line_color = defaultdict(lambda:'green')
    explanation = ""
    actual_lines = actual.splitlines()
    n_actual_lines = len(actual_lines)
    expected_lines = expected.splitlines()
    canonical_actual_lines = canonical_actual_plus_newlines.splitlines()
    canonical_expected_lines = canonical_expected_plus_newlines.splitlines()
    n_canonical_expected_lines = len(canonical_expected_lines)

    if len(canonical_expected_lines) == len(canonical_actual_lines) and 2 < len(canonical_actual_lines) < 1000 and sorted(canonical_expected_lines) == sorted(canonical_actual_lines):
        explanation += colored("\nYour program produced the correct %s lines but in the wrong order.\n" % name, 'red')

    # FIXME changes  canonical_actual_lines, canonical_expected_lines, actual_lines, expected_lines
    diff_explanation = create_diff(canonical_actual_lines, canonical_expected_lines, actual_lines, expected_lines, name, colored, max_lines_shown, debug, actual_line_color)
    if not colorize:
        actual_line_color = defaultdict(lambda:'')

    if show_actual:
        if actual_lines:
            explanation += "Your program produced these %d lines of %s:\n" % (n_actual_lines, name)
            explanation += sanitize_string(actual, max_lines_shown=max_lines_shown,max_line_length_shown=max_line_length_shown, line_color=actual_line_color)
        if expected and actual and actual[-1] != '\n' and expected[-1] == '\n':
             explanation += "Last line of output above was not terminated with a newline('\\n') character\n"
        if show_expected and canonical_expected_lines:
            explanation += "\nThe correct %d lines of %s for this test were:\n" % (n_canonical_expected_lines, name)
            explanation += colored(sanitize_string(expected, max_lines_shown=max_lines_shown,max_line_length_shown=max_line_length_shown), 'green')


    if not actual_lines or not show_diff:
        return explanation

    # check if the difference is a simple character transliteration
    if 8 < len(canonical_expected)  < 1000:
        actual_chars = set(canonical_actual)
        expected_chars = set(canonical_expected)
        actual_not_expected = actual_chars - expected_chars
        expected_not_actual = expected_chars - actual_chars
        if len(actual_not_expected) == 1 and len(expected_not_actual) == 1:
            actual_char = actual_not_expected.pop()
            expected_char = expected_not_actual.pop()
            if canonical_actual.replace(actual_char, expected_char) == canonical_expected:
                n = canonical_actual.count(actual_char)
                if n == 1:
                    format = "a '%s' with a '%s' character."
                else:
                    format = "all '%s' characters with '%s' characters."
                explanation += "\nYour program's %s would be correct if you replaced " % name
                explanation += format % (colored(actual_char, 'red'), colored(expected_char, 'green'))
                explanation += "\n"
                return explanation
        if len(actual_not_expected) == 1 and len(expected_not_actual) == 0:
            actual_char = actual_not_expected.pop()
            if canonical_actual.replace(actual_char, '') == canonical_expected:
                n = canonical_actual.count(actual_char)
                if n == 1:
                    format = "a '%s' character."
                else:
                    format = "all '%s' characters."
                explanation += "Your program's %s would be correct if you removed " % name
                explanation += format % (colored(actual_char, 'red'))
                explanation += "\n"
                return explanation
    if diff_explanation:
        explanation +=  "\n" + "\n".join(diff_explanation[0:max_lines_shown]) + "\n"
    return explanation

def create_diff(canonical_actual_lines, canonical_expected_lines, actual_lines, expected_lines, name, colored, max_lines_shown, debug, actual_line_color):
    prefix_removed = 0
    # difflib.ndiff is horrendously slow so clear matching prefix & suffix
    # but leave 1 line of matching prefix and suffix for context
    if canonical_actual_lines and canonical_expected_lines and canonical_actual_lines[0] == canonical_expected_lines[0]:
            while len(canonical_actual_lines) > 1 and len(canonical_expected_lines) > 1 and canonical_actual_lines[1] == canonical_expected_lines[1]:
                actual_lines.pop(0)
                expected_lines.pop(0)
                canonical_actual_lines.pop(0)
                canonical_expected_lines.pop(0)
                prefix_removed += 1

    suffix_removed = 0
    if canonical_actual_lines and canonical_expected_lines and canonical_actual_lines[-1] == canonical_expected_lines[-1]:
            while len(canonical_actual_lines) > 1 and len(canonical_expected_lines) > 1 and canonical_actual_lines[-2] == canonical_expected_lines[-2]:
                actual_lines.pop()
                expected_lines.pop()
                canonical_actual_lines.pop()
                canonical_expected_lines.pop()
                suffix_removed += 1

    maximum_len_for_diff = 128
    diff_truncated = False
    if len(canonical_expected_lines) > maximum_len_for_diff or len(canonical_actual_lines) > maximum_len_for_diff:
        actual_lines = actual_lines[0:maximum_len_for_diff]
        expected_lines = expected_lines[0:maximum_len_for_diff]
        canonical_actual_lines = canonical_actual_lines[0:maximum_len_for_diff]
        canonical_expected_lines = canonical_expected_lines[0:maximum_len_for_diff]
        diff_truncated = True

    expected_line_number = 0
    actual_line_number = 0
    diff = difflib.ndiff(canonical_actual_lines, canonical_expected_lines)
    diff_explanation = ["The difference between your %s(%s) and the correct %s(%s) is:" % (name, colored("-", 'red'), name, colored("+", 'green'))]
    if prefix_removed:
        diff_explanation.append('...')
    try:
        d = ''
        last_line_in_diff = False
        context_line = None
        dotdotdot_added = False
        for diff_line in diff:
            diff_line = diff_line.rstrip()
            if not diff_line:
                continue
            last_d = d
            d = diff_line[0]
            if d in "-+" and diff_explanation and context_line and diff_explanation[-1] == '...':
                diff_explanation[-1] = context_line
            context_line = None
            if d == '-':
                diff_explanation.append(colored('- ' + actual_lines[actual_line_number], 'red'))
                actual_line_color[prefix_removed+actual_line_number] = 'red'
                actual_line_number += 1
            elif d == "+":
                diff_explanation.append(colored('+ ' + expected_lines[expected_line_number], 'green'))
                expected_line_number += 1
            elif d == "?":
                # include column marker only if line has not been changed before diff
                if last_d == '+':
                    if canonical_expected_lines[expected_line_number - 1] == expected_lines[expected_line_number - 1]:
                        diff_explanation.append(diff_line)
                elif last_d == '-':
                    if canonical_actual_lines[actual_line_number - 1] == actual_lines[actual_line_number - 1]:
                        diff_explanation.append(diff_line)
            elif d == " ":
                context_line = '  ' + actual_lines[actual_line_number]
                if last_line_in_diff:
                    diff_explanation.append(context_line)
                elif not dotdotdot_added:
                    diff_explanation.append('...')
                    dotdotdot_added = True
                actual_line_number += 1
                expected_line_number += 1
            if d in "-+":
                dotdotdot_added = False
                last_line_in_diff = True
            else:
                last_line_in_diff = False
            if len(diff_explanation) > 2*max_lines_shown:
                    break
        if (diff_truncated or suffix_removed) and diff_explanation[-1] != '...':
            diff_explanation.append('...')
    except IndexError:
        if debug: print("IndexError: unexpected diff output")
        # unexpected diff output might break above code
        pass
    return diff_explanation

def sanitize_string(str, leave_tabs=False, leave_colorization=False, max_lines_shown=32, max_line_length_shown=1024, line_color=defaultdict(lambda:''), colorize=False, **extra_kwargs):
    lines = str.splitlines()
    append_repeat_message = False
    if len(lines) >= max_lines_shown:
        last_line_index = len(lines) - 1
        last_line = lines[last_line_index]
        repeats = 1
        while repeats <= last_line_index and lines[last_line_index - repeats] == last_line:
            repeats += 1
        if repeats > max_lines_shown/2  and len(lines) - repeats < max_lines_shown - 1:
            append_repeat_message = True
            lines = lines[0:last_line_index+2-repeats]

    sanitized_lines = []
    for (line_number, line) in enumerate(lines):
        if line_number >= max_lines_shown:
            sanitized_lines.append('...\n')
            break
        if len(line) > max_line_length_shown:
            line = line[0:max_line_length_shown] + ' ...'
        line = line.encode('unicode_escape').decode('ascii')
        if leave_colorization:
            line = line.replace('\\x1b', '\x1b') # yuk FIXME
        if leave_tabs:
            line = line.replace('\\t', '\t') # yuk FIXME
            line = line.replace('\\\\', '\\') # yuk FIXME
        color = line_color[line_number]
        if color:
            line = termcolor_colored(line, color)
        sanitized_lines.append(line)

    if append_repeat_message:
        repeat_message = '<last line repeated %d times>' % repeats
        if colorize:
            repeat_message = termcolor_colored(repeat_message, 'red')
        sanitized_lines.append(repeat_message)
    return '\n'.join(sanitized_lines) + '\n'

